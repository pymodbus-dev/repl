# Pymodbus-REPL

Pymodbus-REPL is a REPL (Read-Eval-Print Loop) tool for working with Modbus devices using the Pymodbus library.

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry (installed globally or within a virtual environment)

### Installation

1. Clone the repository:

   `git clone https://github.com/pymodbus-dev/repl.git`

2. Navigate to the project directory:

    `cd repl`

3. Install dependencies using Poetry: 

    `poetry install`

### Running Tests
To run tests, use the following command: 

`poetry run pytest`

### Building Distribution
To build the distribution package, use the following command: 

`poetry build`

This will create distribution packages in the dist/ directory.

## Usage

### Pymodbus Client
Refer [REPL Client](./pymodbus/repl/client/README.rst)

### Pymodbus Server
Refer [REPL Server](./pymodbus/repl/server/README.rst)

## Contributing
* Fork the repository.
* Create a new branch (git checkout -b feature-name).
* Make your changes and commit them (git commit -am 'Add feature').
* Push to the branch (git push origin feature-name).
* Create a new Pull Request.

## License
This project is licensed under the MIT License.