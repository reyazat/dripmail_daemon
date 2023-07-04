# DripMailDaemon

DripMailDaemon is a Python script that runs as a daemon process and performs actions on email statuses stored in a database. It is designed to be executed as a background process and can be controlled using command-line arguments.

## Prerequisites

- Python 2.7 or above
- Required Python packages: `dripmail`, `daemonize`
- Database connection details must be configured in the `settings.py` file.

## Installation

1. Clone the repository or download the `DripMailDaemon.py` file.
2. Install the required Python packages by running the following command:
   ```
   pip install dripmail daemonize
   ```

## Usage

To control the DripMailDaemon, execute the script with the following command-line arguments:

```
python DripMailDaemon.py [command] [period] [fetch_rec_count]
```

- `command` can be one of the following:
  - `start` - Start the daemon process.
  - `stop` - Stop the daemon process.
  - `restart` - Restart the daemon process.
- `period` (optional) - Time period in seconds between each run of the daemon (default: 100 seconds).
- `fetch_rec_count` (optional) - Number of records to fetch from the database in each run (default: 1000 records).

Example usage:

```
python DripMailDaemon.py start 120 500
```

This command starts the daemon process with a period of 120 seconds and fetches 500 records in each run.

## Logging

The script logs its activities to the file `DripMailDaemon.txt` located in the `/tmp` directory. You can view the log file to monitor the execution and any errors that occur during runtime.

---

# ActDB

ActDB is a Python script that interacts with a MySQL database and performs actions on email statuses. It is designed to be used in conjunction with the DripMailDaemon script.

## Prerequisites

- Python 2.7 or above
- Required Python package: `mysql`
- Database connection details must be configured in the `settings.py` file.

## Usage

To use the ActDB script independently, execute the script with the following command-line argument:

```
python ActDB.py [fetch_rec_count]
```

- `fetch_rec_count` (optional) - Number of records to fetch from the database in each run (default: 1000 records).

Example usage:

```
python ActDB.py 500
```

This command executes the ActDB script, fetching 500 records from the database in each run.

## Logging

The script logs its activities to the file `DripMailLog.txt` located in the same directory as the script. You can view the log file to monitor the execution and any errors that occur during runtime.

---

Please note that these scripts assume the existence of certain dependencies, such as the `dripmail` package and the `settings.py` file. Make sure to install the required packages and configure the necessary settings before running the scripts.