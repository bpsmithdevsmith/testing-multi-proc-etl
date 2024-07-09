# README

## Overview

This command-line interface (CLI) tool is designed to test inserting large amounts of JSON data using various methods. It supports both multiprocessing and multithreading for parallel data insertion.

## Prerequisites

- Python 3.7+
- PostgreSQL
- AWS CLI configured with necessary permissions
- Environment variables set up in a `.env` file

## Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```
ENV=<LOCAL|DEV>
AWS_SECRET_NAME=<your_aws_secret_name if DEV>
AWS_REGION=<your_aws_region if DEV>
PGHOST=<your_postgres_host>
PGDATABASE=<your_postgres_database>
PGUSER=<your username if LOCAL
PGPASS=<your password if LOCAL>
```

## Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Commands

### 1. Test Connection

Tests the connection to the PostgreSQL database.

```sh
python cli.py test-connect
```

### 2. Create Table

Creates a table in the PostgreSQL database.

```sh
python cli.py create-table --table <table_name>
```

### 3. Drop Table

Drops a table from the PostgreSQL database.

```sh
python cli.py drop-table --table <table_name>
```

### 4. Test Multiprocess Insertion

Inserts data using multiple processes.

```sh
python cli.py test-multiprocess --table <table_name> --nworkers <number_of_workers> --nrows <number_of_rows> --batch-size <batch_size> --json-kbs <json_size_in_kilobytes> --method <batch_or_copy>
```

### 5. Test Multithread Insertion

Inserts data using multiple threads.

```sh
python cli.py test-multithread --table <table_name> --nworkers <number_of_workers> --nrows <number_of_rows> --batch-size <batch_size> --json-kbs <json_size_in_kilobytes> --method <batch_or_copy>
```

### 6. Test Temporary Table Insertion

Inserts data into a temporary table and then copies it to the target table.

```sh
python cli.py test-temptable --table <table_name> --nrows <number_of_rows> --batch-size <batch_size> --json-kbs <json_size_in_kilobytes> --method <batch_or_copy>
```

### 7. Test AWS Credentials

Fetches and prints the credentials from AWS Secrets Manager.

```sh
python cli.py test-credentials
```

## Notes

- Ensure that AWS Secrets Manager is set up with the appropriate secrets containing the PostgreSQL credentials.
- Modify the environment variables in the `.env` file according to your configuration.


## Profiling 
If you want to have a deeper look at the function timings, then do the following. 

```sh
python -m cProfile -o mt.prof  perf_test.py test-multithread --table processes --nrows 100000 --json-kbs 10 --batch-size 1000  

# visualize the results
snakeviz mt.prof

```
