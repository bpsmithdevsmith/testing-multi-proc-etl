import click
import csv
from io import StringIO
import concurrent.futures
import os
import json
import timeit
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv, find_dotenv
import boto3
from botocore.exceptions import ClientError


load_dotenv(find_dotenv())


CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS {table} (
        fake_id text NOT NULL,
        json_data jsonb
    );
"""

DROP_TABLE_SQL = "DROP TABLE IF EXISTS {table}"

INSERT_SQL = "INSERT INTO {table} (fake_id, json_data) VALUES (%s, %s);"


def get_credentials():
    secret_name = "rds!cluster-59c83da8-c841-4e45-aa32-98d302cd8daa"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)

    os.environ["PGUSER"] = secret["username"]
    os.environ["PGPASS"] = secret["password"]
    return secret


credentials = get_credentials()


class DBManager:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PGHOST"),
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASS"),
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()


def _do_insert_batch(table, nparams, json_kbs):
    # This function is called by each process so it needs to establish its own connection. 
    # This is not very efficient, but it is the simplest way to parallelize the inserts.
    # In a real-world scenario, you would re-use the connection, but this would require more complex code.
    myjson = {"data": "x" * json_kbs * 1024}
    params = [(f"fake_id_{i}", json.dumps(myjson)) for i in range(nparams)]
    with DBManager() as db:
        cur = db.conn.cursor()
        execute_batch(cur, INSERT_SQL.format(table=table), params)
        db.conn.commit()
        cur.close()


def _do_insert_copy_from(table, nparams, json_kbs):
    # This function is called by each process so it needs to establish its own connection. 
    # This is not very efficient, but it is the simplest way to parallelize the inserts.
    # In a real-world scenario, you would re-use the connection, but this would require more complex code.
    myjson = {"data": "x" * json_kbs * 1024}
    params = [(f"fake_id_{i}", json.dumps(myjson)) for i in range(nparams)]
    with DBManager() as db:
        cur = db.conn.cursor()
        bfr = StringIO()
        writer = csv.writer(bfr, delimiter="\t", lineterminator="\n", escapechar="\\", quoting=csv.QUOTE_NONE)
        writer.writerows(params)
        bfr.seek(0)
        cur.copy_from(bfr, table, columns=("fake_id", "json_data"), sep="\t")
        db.conn.commit()
        cur.close()



@click.group()
def cli():
    pass


@cli.command()
def test_connect():
    with DBManager() as db:
        cursor = db.conn.cursor()
        cursor.execute("SELECT version();")
        print(cursor.fetchone())
        cursor.close()
        print("successfully connected to database")


@cli.command()
@click.option("--table", default="test_json_inserts", help="test table to crete")
def create_table(table):
    with DBManager() as db:
        cur = db.conn.cursor()
        cur.execute(CREATE_TABLE_SQL.format(table=table))
        db.conn.commit()
        cur.close()
        print(f"successfully created table {table}")


@cli.command()
@click.option("--table", default="test_json_inserts", help="drop test table")
def drop_table(table):
    with DBManager() as db:
        cur = db.conn.cursor()
        cur.execute(DROP_TABLE_SQL.format(table=table))
        db.conn.commit()
        cur.close()
        print(f"successfully dropped table {table}")


@cli.command()
@click.option("--table", default="test_json_inserts", help="target table to insert")
@click.option("--nworkers", help="number of processes to use", type=int)
@click.option("--nrows", default=10**6, help="number of rows to insert")
@click.option("--batch-size", default=1000, help="batch insert size")
@click.option("--json-kbs", default=10, help="size of json file in kilobytes")
@click.option("--method", default='batch', help="batch or copy")
def test_multiprocess(table, nworkers, nrows, batch_size, json_kbs, method):
    nworkers = nworkers or os.cpu_count()

    t0 = timeit.default_timer()
    with concurrent.futures.ProcessPoolExecutor(max_workers=nworkers) as executor:
        # a little lazy here on the math. We could be light on the last batch.
        ntasks = nrows // batch_size
        fct = {'batch': _do_insert_batch, 'copy': _do_insert_copy_from}[method]

        futures = [
            executor.submit(fct, table, batch_size, json_kbs)
            for i in range(ntasks)
        ]

    for future in concurrent.futures.as_completed(futures):
        future.result()

    t1 = timeit.default_timer()
    print(f"inserts {t1-t0} seconds")



@cli.command()
@click.option("--table", default="test_json_inserts", help="target table to insert")
@click.option("--nworkers", default=4, help="number of processes to use")
@click.option("--nrows", default=10**6, help="number of rows to insert")
@click.option("--batch-size", default=1000, help="batch insert size")
@click.option("--json-kbs", default=10, help="size of json file in kilobytes")
@click.option("--method", default='batch', help="batch or copy")
def test_multithread(table, nworkers, nrows, batch_size, json_kbs, method):

    t0 = timeit.default_timer()
    with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
        # a little lazy here on the math. We could be light on the last batch.
        ntasks = nrows // batch_size
        fct = {'batch': _do_insert_batch, 'copy': _do_insert_copy_from}[method]
        futures = [
            executor.submit(fct, table, batch_size, json_kbs)
            for i in range(ntasks)
        ]

    for future in concurrent.futures.as_completed(futures):
        future.result()

    t1 = timeit.default_timer()
    print(f"inserts {t1-t0} seconds")


@cli.command()
def test_credentials():
    secret = get_credentials()
    print(secret)





if __name__ == "__main__":
    cli() 