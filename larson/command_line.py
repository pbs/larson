import json
import os
import sys

import fire

from . import dict_to_bash, get_parameters, put_parameters


def print_to_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def validate_parameter_store_path(input):
    try:
        assert isinstance(input, str)
        assert input[0] == "/"
        assert input[-1] == "/"
    except AssertionError:
        print_to_stderr("invalid parameter store path {}".format(input))
        sys.exit(1)

    return True


class LarsonCLI(object):
    def generate_bash(self, path):
        try:
            with open(path) as f:
                parameters = json.load(f)
        except FileNotFoundError:
            print_to_stderr("file not found: {p}".format(p=path))
            sys.exit(1)
        except json.decoder.JSONDecodeError:
            if os.stat(path).st_size == 0:
                error_message = "input file is empty: {p}".format(p=path)
            else:
                error_message = "could not parse json in {p}".format(p=path)
            print_to_stderr(error_message)
            sys.exit(1)

        bash_lines = dict_to_bash(parameters)
        for line in bash_lines:
            print(line)

    def get_parameters(self, parameter_store_path, region="us-east-1"):
        validate_parameter_store_path(parameter_store_path)
        parameters = get_parameters(parameter_store_path, region)
        formatted = json.dumps(parameters, sort_keys=True, indent=4)
        print(formatted)

    def put_parameters(self, parameter_store_path, input_file, region="us-east-1"):
        validate_parameter_store_path(parameter_store_path)
        with open(input_file) as f:
            parameters = json.load(f)

        put_parameters(parameter_store_path, parameters, region)

        for key in parameters.keys():
            print_to_stderr("wrote {}{}".format(parameter_store_path, key))


def main():
    fire.Fire(LarsonCLI)


if __name__ == "__main__":
    main()
