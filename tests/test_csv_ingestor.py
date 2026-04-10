import os
import pytest
import sqlite3
import pandas as pd
from csv_ingestor import load_csv, create_connection, create_table, insert_data

# sends sample_df to a real csv file and returns the path
@pytest.fixture
def csv_file(tmp_path, sample_df):
    path = tmp_path / "people.csv"
    sample_df.to_csv(path, index=False)
    return str(path)

class TestLoadCSV:

    # test to make sure it returns correctly
    def test_returns_df(self):
        df = load_csv("data.csv")
        assert isinstance(df, pd.DataFrame)

    # testing missing files
    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_csv("doesnotexist.csv")

    




