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

## Configuration

MyCLIApp can be configured using environment variables or a configuration file.

### Environment Variables

- `MYCLIAPP_CONFIG`: Path to the configuration file

### Configuration File

By default, MyCLIApp looks for a configuration file at `~/.mycliapp/config.yaml`. You can specify a different configuration file using the `MYCLIAPP_CONFIG` environment variable.

```yaml
# config.yaml
setting1: value1
setting2: value2
```

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please open an issue on GitHub or contact [your email].

---

*This README.md template is generated for MyCLIApp, a CLI application built with Python and Click.*
```

Feel free to customize the template according to your specific application's details and requirements.