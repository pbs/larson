import boto3


def _get_boto_client(region):
    return boto3.client("ssm", region_name=region)


def read(parameter_store_path, region="us-east-1"):
    boto_client = _get_boto_client(region)
    paginating = True
    next_token = None
    results = {}
    while paginating:
        kwargs = {"Path": parameter_store_path, "WithDecryption": True}
        if next_token:
            kwargs["NextToken"] = next_token
        response = boto_client.get_parameters_by_path(**kwargs)
        if response.get("NextToken"):
            next_token = response["NextToken"]
        else:
            paginating = False
        for param in response["Parameters"]:
            variable_name = param["Name"].split("/")[-1].strip()
            variable_value = param["Value"].strip()
            results[variable_name] = variable_value
    return results


def write(parameter_store_path, parameters, region="us-east-1"):
    boto_client = _get_boto_client(region)
    for key, value in parameters.items():
        boto_client.put_parameter(
            Name="{}{}".format(parameter_store_path, key),
            Value=value,
            Type="SecureString",
            Overwrite=True,
            KeyId="alias/aws/ssm",
        )
