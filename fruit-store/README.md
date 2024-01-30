# Fruit Store Exercise

Application that recieves messages such as:

```json
{
    "item": "apple",
	"quantity": 15,
    "price": 2.5,
	"date": "2020-03-20T01:30:08.180856"
}
```

And generates reports such as:


```json
{
    "apple": {
        "total_quantity": 600,
        "average_per_sale": 2,
        "total_revenue": 234534,
        "monthly": {
            "2023-01": {
                "total_quantity": 8,
                "average_per_sale": 2,
                "total_revenue": 234534,
            }
            ...
        }
    },
    "banana": {
        "total_quantity": 400,
        "average_per_sale": 6,
        "total_revenue": 456870,
        "monthly": {
            ...
        }
}
```

## TODO:

- [ ] Documentation:
    - [X] Include some Readme
    - [ ] Incldue Sphinx documentation

- [ ] Data and reporting backends:
    - [X] In-memory backend.
    - [ ] SQL Backend.
    - [ ] InfluxDB Backend.

- [ ] Devops:
    - [X] Dockerize
    - [ ] Include integrated testing for grpc.
    - [ ] Include integrated testing for SQL.
    - [ ] Include integrated testing for InfluxDB.

- [ ] Refactor:
    - [ ] Move GRPC auto-generated code away from default-packages.
    - [ ] Automate grpc code generation in docker-build process.

## Getting started

Simply run `make` to list all available development options.

## Development environment

Python dependencies based on PDM. To install dependencies:

```bash
pdm sync
```

To run the server:

```bash
make up
```

To run the client do:

```bash
pdm run python -m "fruit_store.cli.app" client [ARGS...]
```

Available client commands are:

```bash
Usage: python -m fruit_store.cli.app client [OPTIONS] COMMAND [ARGS]...

Options:
  --host TEXT  [default: localhost:50051]
  --help       Show this message and exit.

Commands:
  healthcheck          Pings the server.
  purchase-event       Send a purchase event directly from the cli
  purchase-event-json  Convenience method that inputs multiple json files...
  request-report       Prints out a report per item and per month
```

Use `--help` option on each command for more information.

## Docker

To build docker images use `make docker`. Default names are `fruit-store-client` and `fruit-store-server`


