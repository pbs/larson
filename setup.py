from setuptools import setup

DEPENDENCIES = ["boto3>=1.5.0,<2.0.0", "click>=6.0.0,<7.0.0"]
DEV_DEPENDENCIES = ["black", "isort", "twine", "pytest"]

setup(
    name="larson",
    version="2.0.1",
    description="Library for managing secrets",
    url="https://github.com/pbs/larson",
    author="PBS",
    author_email="",
    packages=["larson"],
    scripts=["bin/larson", "bin/larson_json_to_vars"],
    zip_safe=False,
    install_requires=DEPENDENCIES,
    extras_require={"dev": DEV_DEPENDENCIES},
    python_requires=">=3.3",
)
