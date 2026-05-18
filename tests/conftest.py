import pytest
import os
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_ACCOUNT", "test_account")
    monkeypatch.setenv("SNOWFLAKE_USER", "test_user")
    monkeypatch.setenv("SNOWFLAKE_PASSWORD", "test_password")

@pytest.fixture(autouse=True)
def mock_snowflake_client(mocker):
    mock = MagicMock()
    mocker.patch('src.analytics.snowflake_client.SnowflakeClient._get_connection', return_value=mock)
    return mock
