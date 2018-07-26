import json
import os
import sys

import click

from . import (
    dict_to_bash,
    parameter_store,
    print_to_stderr,
    validate_parameter_store_path,
)


@click.command(
    name="generate-bash",
    help="generate a bash script from a json file of key/value pairs, for setting environment variables",
)
@click.argument("input_file")
def generate_bash(input_file):
    try:
        with open(input_file) as f:
            parameters = json.load(f)
    except FileNotFoundError:
        print_to_stderr("file not found: {p}".format(p=input_file))
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        if os.stat(input_file).st_size == 0:
            error_message = "input file is empty: {p}".format(p=input_file)
        else:
            error_message = "could not parse json in {p}".format(p=input_file)
        print_to_stderr(error_message)
        sys.exit(1)

    bash_lines = dict_to_bash(parameters)
    for line in bash_lines:
        print(line)


@click.command(
    name="get-parameters",
    help="read parameter store values under a given path (outputs json to stdout)",
)
@click.argument("parameter_store_path")
@click.option(
    "--region", default="us-east-1", help="AWS region name, such as us-east-1"
)
def get_parameters(parameter_store_path, region):
    validate_parameter_store_path(parameter_store_path)
    parameters = parameter_store.read(parameter_store_path, region)
    formatted = json.dumps(parameters, sort_keys=True, indent=4)
    print(formatted)


@click.command(
    name="put-parameters",
    help="write a json file of key/value pairs to parameter store under a given path",
)
@click.argument("parameter_store_path")
@click.option("--input-file")
@click.option(
    "--region", default="us-east-1", help="AWS region name, such as us-east-1"
)
def put_parameters(parameter_store_path, input_file, region="us-east-1"):
    validate_parameter_store_path(parameter_store_path)
    try:
        with open(input_file) as f:
            parameters = json.load(f)
    except json.JSONDecodeError:
        print_to_stderr("unreadable file {}".format(input_file))
        sys.exit(1)

    parameter_store.write(parameter_store_path, parameters, region)

    for key in parameters.keys():
        print_to_stderr("wrote {}{}".format(parameter_store_path, key))


@click.group()
def main():
    pass


for func in [generate_bash, put_parameters, get_parameters]:
    main.add_command(func)


if __name__ == "__main__":
    main()
