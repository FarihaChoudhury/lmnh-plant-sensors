"""Test file: transform.py"""
# pylint: disable=line-too-long

from io import StringIO
import pytest
import pandas as pd
from transform import (load_data, convert_datatypes,
                       round_floats, verify_emails, check_for_null_vals)


EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"""


class TestTransformCleaning():
    """Class containing tests for the transform.py file."""
    @pytest.fixture
    def sample_csv_data(self):
        """Fixture returning a sample csv data."""
        sample_csv = "name,email,longitude,latitude,plant_name,temperature,soil_moisture,recording_taken,last_watered\nCarl Linnaeus,carl.linnaeus@lnhm.co.uk,Epipremnum Aureum,13.187142311466939,31.71289323910939,2024-11-26 09:38:44,'Mon, 25 Nov 2024 14:03:04 GMT'"
        test_data = StringIO(sample_csv)
        return test_data

    @pytest.fixture
    def sample_pd(self):
        """Fixture returning a sample dataframe."""
        test_data = pd.DataFrame({
            "email": "test@test.com",
            "longitude": 12.23,
            "latitude": 60.21234567,
            "temperature": 23.2123454353,
            "soil_moisture": 54,
            "recording_taken": ["2024-11-25 10:00:00"],
            "last_watered": ["Mon, 25 Nov 2024 14:03:04 GMT"]
        })
        return test_data

    def test_successful_load_data(self, sample_csv_data):
        """Test csv data is loaded into df successfully."""
        df = load_data(sample_csv_data)
        assert df.shape == (1, 9)
        assert "last_watered" in df.columns

    def test_recording_taken_data_type(self, sample_pd):
        """Test that the recording_taken data type is datetime after."""
        df = convert_datatypes(sample_pd)
        assert df["recording_taken"].dtype == "datetime64[ns]"

    def test_last_watered_data_type(self, sample_pd):
        """Test the datatype of last_watered is datetime."""
        df = convert_datatypes(sample_pd)
        assert df["last_watered"].dtype == "datetime64[ns]"

    def test_floats_rounded(self, sample_pd):
        """Test any column with float dtype are given to 2dp."""
        len_temp_decimals = len(str(round_floats(sample_pd, 2)[
            "temperature"].iloc[0]).split(".")[1])
        len_soil_decimals = len(str(round_floats(sample_pd, 2)[
            "soil_moisture"].iloc[0]).split(".")[1])
        assert len_temp_decimals == 2
        assert len_soil_decimals == 2

    def test_email_valid(self, sample_pd):
        """Function successfully verifies email."""
        df = verify_emails(sample_pd, EMAIL_REGEX)
        assert df["email"].iloc[0] == "test@test.com"

    def test_invalid_email(self):
        """Function tests invalid email results in None in dataframe."""
        test_data = pd.DataFrame({"email": ["invalid-email.com"]})
        df = verify_emails(test_data, EMAIL_REGEX)
        assert df["email"].iloc[0] is None

    def test_null_value_discard_row(self):
        """Function tests discarding of row with null temperature value."""
        test_data = {
            "plant_id": [1, 2],
            "name": ["test1", "test2"],
            "temperature": [None, 45],
            "soil_moisture": [21.34, 23.65]
        }
        df = check_for_null_vals(pd.DataFrame(test_data))
        assert df.shape == (1, 4)
        assert not df.isnull().values.any()
