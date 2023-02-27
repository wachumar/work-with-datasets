import pytest

from processing import (
    CLIENT_INFO_NAME,
    CLIENT_FINANCIAL_NAME,
    DEFAULT_FILTER_COUNTRY,
    add_extension_missed,
    get_settings_from_config,
)


@pytest.fixture()
def config():
    return {
        "client_info_path": "first_dataset_name.csv",
        "client_financial_path": "second_dataset_name.csv",
        "countries": ["Poland"],
        "default": False,
    }


def test_set_params_default_chosen(config):
    config["default"] = True
    ci, cf, co = get_settings_from_config(config)
    assert ci == CLIENT_INFO_NAME
    assert cf == CLIENT_FINANCIAL_NAME
    assert co == DEFAULT_FILTER_COUNTRY


def test_set_params_from_chosen(config):
    ci, cf, co = get_settings_from_config(config)
    assert ci == config["client_info_path"]
    assert cf == config["client_financial_path"]
    assert co == config["countries"]


@pytest.mark.parametrize(
    "input_path, expected_path",
    [("some_path", "some_path.csv"), ("some_path.csv", "some_path.csv")],
)
def test_add_csv_extension_if_its_not_there(input_path, expected_path):
    new_path = add_extension_missed(input_path)
    assert new_path == expected_path
