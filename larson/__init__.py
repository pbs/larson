import sys
from shlex import quote


def print_to_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def dict_to_bash(parameters):
    lines = []
    for key, value in parameters.items():
        variable_name = key.strip()
        variable_value = value.strip()
        lines.append("export {}={}".format(quote(variable_name), quote(variable_value)))
    return lines


def validate_parameter_store_path(input):
    try:
        assert isinstance(input, str)
        assert input[0] == "/"
        assert input[-1] == "/"
    except AssertionError:
        print_to_stderr("invalid parameter store path {}".format(input))
        sys.exit(1)

    return True
