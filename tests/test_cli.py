import json
import os
from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner

from larson.command_line import main


class CLITests(TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        self.runner = CliRunner()
        with open("./fixtures/useful-parameters.json") as fh:
            self.useful_parameters = json.load(fh)

    @patch("larson.parameter_store.read")
    def test_successful_read(self, mock_ps_read):
        mock_ps_read.return_value = self.useful_parameters
        result = self.runner.invoke(
            main, ["get-parameters", "/a/parameter/store/path/"]
        )
        assert result.exit_code == 0
        assert json.loads(result.output) == self.useful_parameters
        assert mock_ps_read.call_count == 1

    @patch("larson.parameter_store.read")
    def test_invalid_read(self, mock_ps_read):
        mock_ps_read.return_value = self.useful_parameters
        result = self.runner.invoke(main, ["get-parameters", "a/parameter/store/path/"])
        assert result.exit_code == 1
        assert (
            result.output.strip()
            == "invalid parameter store path a/parameter/store/path/"
        )
        assert mock_ps_read.call_count == 0

    @patch("larson.parameter_store.write")
    def test_successful_write(self, mock_ps_write):
        result = self.runner.invoke(
            main,
            [
                "put-parameters",
                "/a/parameter/store/path/",
                "--input-file=./fixtures/useful-parameters.json",
            ],
        )
        assert result.exit_code == 0
        assert result.output.strip() == "\n".join(
            [
                "wrote /a/parameter/store/path/alpha",
                "wrote /a/parameter/store/path/beta",
                "wrote /a/parameter/store/path/delta",
            ]
        )
        assert mock_ps_write.call_count == 1

    @patch("larson.parameter_store.write")
    def test_invalid_write(self, mock_ps_write):
        result = self.runner.invoke(
            main,
            [
                "put-parameters",
                "/a/parameter/store/path",
                "--input-file=./fixtures/useful-parameters.json",
            ],
        )
        assert result.exit_code == 1
        assert (
            result.output.strip()
            == "invalid parameter store path /a/parameter/store/path"
        )
        assert mock_ps_write.call_count == 0

    @patch("larson.parameter_store.write")
    def test_write_badly_formatted_file(self, mock_ps_write):
        result = self.runner.invoke(
            main,
            [
                "put-parameters",
                "/a/parameter/store/path/",
                "--input-file=./fixtures/badly-formatted.json",
            ],
        )
        assert result.exit_code == 1
        assert (
            result.output.strip() == "unreadable file ./fixtures/badly-formatted.json"
        )
        assert mock_ps_write.call_count == 0

    @patch("larson.parameter_store.write")
    def test_write_empty_file(self, mock_ps_write):
        result = self.runner.invoke(
            main,
            [
                "put-parameters",
                "/a/parameter/store/path/",
                "--input-file=./fixtures/empty-file.json",
            ],
        )
        assert result.exit_code == 1
        assert result.output.strip() == "unreadable file ./fixtures/empty-file.json"
        assert mock_ps_write.call_count == 0

    def test_generate_bash(self):
        result = self.runner.invoke(
            main, ["generate-bash", "./fixtures/useful-parameters.json"]
        )
        assert result.exit_code == 0
        assert result.output.strip() == "\n".join(
            [
                "export alpha=the_alpha_value",
                "export beta=the_beta_value",
                "export delta=the_delta_value",
            ]
        )
