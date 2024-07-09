# Performance CLI

## Overview

**Performance CLI** is a command-line interface (CLI) application built with Python and Click. It is designed to test the performance of inserting JSON into postgres using different methods. 

## Usage

### Basic Commands

To use MyCLIApp, simply type:

```bash
perf_test [command] [options]
```

### Available Commands

- `test-connect`: Test that the CLI can connect to the database configured in the .env file

  ```bash
  perf_test test_connect
  ```
- `create-table`: Create the target json table to insert data

  ```bash
  perf_test create-table --table TABLE_NAME
  ```
- `drop-table`: Drop the specified table

  ```bash
  perf_test drop-table --table TABLE_NAME
  ```


### Examples

- Example 1:
  ```bash
  mycliapp command1 --option1 value1
  ```
- Example 2:
  ```bash
  mycliapp command2 --option2 value2
  ```

## Profiling 

```
> python -m cProfile -o mt.prof  perf_test.py test-multithread --table processes --nrows 100000 --json-kbs 10 --batch-size 1000  
# To view 
> snakeviz mt.prof


```
