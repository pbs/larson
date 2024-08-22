# Usage

`larson` loads parameters from [AWS ssm parameter store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html), and adds them as shell environment variables.

## Download parameters as a json file

```
$ larson get-parameters /a/parameter/store/path/ > ./example.json
```

```
$ cat ./example.json

{
    "alpha": "the_alpha_value",
    "beta": "the_beta_value",
    "delta": "the_delta_value"
}
```

## Load json parameters as environment variables

```
source larson_json_to_vars ./example.json
```

```
$ env | grep 'alpha\|beta\|delta'
alpha=the_alpha_value
delta=the_delta_value
beta=the_beta_value
```

## Upload parameters to parameter store

```
$ larson put-parameters /a/parameter/store/path/ --input-file=./new-values.json
```

# Installation

`pip install larson`

# Tests

`pytest`

# Release
Larson is available via PyPI. To cut a new release, do the following:
1. Edit `setup.py` such that it contains the new release version number.
1. python -m pip install build
1. python -m build --wheel
1. If you see `Successfully built larson-<new-version-number>-py3-none-any.whl` then proceed. If
   not, troubleshoot.  
1. Get your PyPI API token by logging into the Ops PBS PyPI account.
1. After successfully building the wheel, upload with `twine`: `twine upload dist/<the filename of your
   newly built wheel>. When prompted, enter your API token.
