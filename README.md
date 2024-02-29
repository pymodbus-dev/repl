# Pymodbus-REPL

Pymodbus-REPL is a REPL (Read-Eval-Print Loop) tool for working with Modbus devices using the Pymodbus library.

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry (installed globally or within a virtual environment)

### Dev instructions

1. Clone the repository:

   `git clone https://github.com/pymodbus-dev/repl.git`

2. Navigate to the project directory:

    `cd repl`

3. Install dependencies using Poetry: 

    `poetry install`

**NOTE** This repo is meant to be an helper for [pymodbus](https://github.com/pymodbus-dev/pymodbus) and the usage requires
a working version of pymodbus.

The installed `pymodbus` library for local development can also have impact on the path resolution while working locally on this repo.
To overcome that problem, please make sure to run the [client](./pymodbus/client/main.py) and [server](./pymodbus/server/main.py) files
from with in the respective working directories.

For .e.g

#### Run Server
```
(pymodbus3.8)
❯ python3 main.py --host 0.0.0.0 --verbose run --modbus-config default_config.json --modbus-server tcp --modbus-framer socket --modbus-port 5020 --unit-id 1 --unit-id 2 -u 4 -r 1 --timeout 2
2024-02-28 14:38:24,952 INFO  logging:97 Modbus server started
2024-02-28 14:38:24,952 DEBUG logging:103 Awaiting connections server_listener
2024-02-28 14:38:24,952 INFO  logging:97 Server listening.

__________                          .______.                    _________
\______   \___.__. _____   ____   __| _/\_ |__  __ __  ______  /   _____/ ______________  __ ___________
 |     ___<   |  |/     \ /  _ \ / __ |  | __ \|  |  \/  ___/  \_____  \_/ __ \_  __ \  \/ // __ \_  __ \\
 |    |    \___  |  Y Y  (  <_> ) /_/ |  | \_\ \  |  /\___ \   /        \  ___/|  | \/\   /\  ___/|  | \/
 |____|    / ____|__|_|  /\____/\____ |  |___  /____//____  > /_______  /\___  >__|    \_/  \___  >__|
           \/          \/            \/      \/           \/          \/     \/                 \/
                                                                                                v2.0.2-Pymodbus3.7.0dev


SERVER > 2024-02-28 14:39:15,352 DEBUG logging:103 Connected to server
2024-02-28 14:39:15,352 DEBUG logging:103 recv: 0x0 0x1 0x0 0x0 0x0 0x6 0x1 0x4 0x0 0x1 0x0 0x1 old_data:  addr=None
2024-02-28 14:39:15,352 DEBUG logging:103 Handling data: 0x0 0x1 0x0 0x0 0x0 0x6 0x1 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:15,352 DEBUG logging:103 Processing: 0x0 0x1 0x0 0x0 0x0 0x6 0x1 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:15,352 DEBUG logging:103 Factory Request[ReadInputRegistersRequest': 4]
2024-02-28 14:39:15,352 DEBUG logging:103 validate: fc-[4] address-1: count-1
2024-02-28 14:39:15,352 DEBUG logging:103 getValues: fc-[4] address-1: count-1
2024-02-28 14:39:15,352 DEBUG logging:103 send: 0x0 0x1 0x0 0x0 0x0 0x5 0x1 0x4 0x2 0xc5 0x7c
2024-02-28 14:39:37,029 DEBUG logging:103 recv: 0x0 0x2 0x0 0x0 0x0 0x6 0x4 0x4 0x0 0x1 0x0 0x1 old_data:  addr=None
2024-02-28 14:39:37,029 DEBUG logging:103 Handling data: 0x0 0x2 0x0 0x0 0x0 0x6 0x4 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:37,029 DEBUG logging:103 Processing: 0x0 0x2 0x0 0x0 0x0 0x6 0x4 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:37,029 DEBUG logging:103 Factory Request[ReadInputRegistersRequest': 4]
2024-02-28 14:39:37,029 DEBUG logging:103 validate: fc-[4] address-1: count-1
2024-02-28 14:39:37,029 DEBUG logging:103 getValues: fc-[4] address-1: count-1
2024-02-28 14:39:37,029 DEBUG logging:103 send: 0x0 0x2 0x0 0x0 0x0 0x5 0x4 0x4 0x2 0xc7 0xbe
2024-02-28 14:39:41,010 DEBUG logging:103 recv: 0x0 0x3 0x0 0x0 0x0 0x6 0x5 0x4 0x0 0x1 0x0 0x1 old_data:  addr=None
2024-02-28 14:39:41,010 DEBUG logging:103 Handling data: 0x0 0x3 0x0 0x0 0x0 0x6 0x5 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:41,010 DEBUG logging:103 Processing: 0x0 0x3 0x0 0x0 0x0 0x6 0x5 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:41,010 DEBUG logging:103 Not a valid slave id - 5, ignoring!!
2024-02-28 14:39:41,010 DEBUG logging:103 Resetting frame - Current Frame in buffer - 0x0 0x3 0x0 0x0 0x0 0x6 0x5 0x4 0x0 0x1 0x0 0x1
2024-02-28 14:39:44,015 DEBUG logging:103 -> transport: received eof
2024-02-28 14:39:44,015 DEBUG logging:103 Connection lost server due to None
2024-02-28 14:39:44,015 DEBUG logging:103 Handler for stream [server] has been canceled

```

#### Run client
```
pymodbus/repl/client on  repl-server-startup [!?] via 🐍 v3.8.13 (pymodbus3.8)
❯ python3 main.py tcp --port 5020 --framer tcp

----------------------------------------------------------------------------
__________          _____             .___  __________              .__
\______   \___.__. /     \   ____   __| _/  \______   \ ____ ______ |  |
 |     ___<   |  |/  \ /  \ /  _ \ / __ |    |       _// __ \\\____ \|  |
 |    |    \___  /    Y    (  <_> ) /_/ |    |    |   \  ___/|  |_> >  |__
 |____|    / ____\____|__  /\____/\____ | /\ |____|_  /\___  >   __/|____/
           \/            \/            \/ \/        \/     \/|__|
                                                v2.0.2 - Pymodbus-3.7.0dev
----------------------------------------------------------------------------

> client.read_input_registers address 1 count 1 slave 1
{
    "registers": [
        50556
    ]
}

> client.read_input_registers address 1 count 1 slave 4
{
    "registers": [
        51134
    ]
}

> client.read_input_registers address 1 count 1 slave 5
{
    "original_function_code": "4 (0x4)",
    "error": "[Input/Output] Modbus Error: [Invalid Message] No response received, expected at least 8 bytes (0 received)"
}

>

```


### Running Tests
To run tests, use the following command: 

`poetry run pytest`

### Building Distribution
To build the distribution package, use the following command: 

`poetry build`

This will create distribution packages in the dist/ directory.

## Usage

### Pymodbus Client
Refer [REPL Client](./pymodbus_repl/client/README.md)

### Pymodbus Server
Refer [REPL Server](./pymodbus_repl/server/README.md)

## Contributing
* Fork the repository.
* Create a new branch (git checkout -b feature-name).
* Make your changes and commit them (git commit -am 'Add feature').
* Push to the branch (git push origin feature-name).
* Create a new Pull Request.

## License
This project is licensed under the MIT License.