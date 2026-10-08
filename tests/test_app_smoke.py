from pathlib import Path

import app


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "processed" / "tourism_arrivals_app_ready.csv"


def test_data_file_exists():
    assert DATA_FILE.exists(), f"Missing dataset: {DATA_FILE}"


def test_load_data_returns_expected_columns():
    df = app.load_data()

    assert not df.empty
    required_columns = {
        "Year",
        "Month",
        "Country",
        "Date",
        "Tourist_Arrivals",
        "Standard_Country",
        "Continent",
    }
    assert required_columns.issubset(set(df.columns))
    assert df["Tourist_Arrivals"].ge(0).all()
