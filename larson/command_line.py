import json
import sys
import os

import fire

from . import dict_to_bash, get_parameters, put_parameters


def print_to_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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
        parameters = get_parameters(parameter_store_path, region)
        formatted = json.dumps(parameters, sort_keys=True, indent=4)
        print(formatted)

    def put_parameters(self, parameter_store_path, input_file, region="us-east-1"):
        with open(input_file) as f:
            parameters = json.load(f)

        put_parameters(parameter_store_path, parameters, region)

        for key in parameters.keys():
            print_to_stderr("wrote {}{}".format(parameter_store_path, key))


def main():
    fire.Fire(LarsonCLI)


if __name__ == "__main__":
    main()
