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

an excellent idea...