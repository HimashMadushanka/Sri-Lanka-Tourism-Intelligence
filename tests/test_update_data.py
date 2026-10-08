from pathlib import Path
import pandas as pd
import pytest
import update_data


def test_get_current_data_status():
    status = update_data.get_current_data_status()
    assert status is not None
    assert "df" in status
    assert "total_records" in status
    assert status["total_records"] > 0
    assert status["latest_year"] >= 2025


def test_clean_and_standardize_data_transformation():
    sample_raw = pd.DataFrame({
        "Year": [2025, 2025],
        "Country": ["Russian Federation", "People's Republic of China"],
        "Month": ["january", "february"],
        "Tourist_Arrivals": ["1500", 2500]
    })
    
    cleaned = update_data.clean_and_standardize_data(sample_raw)
    
    assert len(cleaned) == 2
    assert "Standard_Country" in cleaned.columns
    assert "Continent" in cleaned.columns
    assert "Date" in cleaned.columns
    
    # Check standardization rules
    assert "Russia" in cleaned["Standard_Country"].values
    assert "China" in cleaned["Standard_Country"].values
    assert cleaned["Month_Number"].tolist() == [1, 2]
    assert cleaned["Date"].tolist() == ["2025-01-01", "2025-02-01"]
    assert cleaned["Tourist_Arrivals"].tolist() == [1500, 2500]


def test_clean_and_standardize_missing_column():
    invalid_raw = pd.DataFrame({
        "Year": [2025],
        "Country": ["India"]
        # Missing Month and Tourist_Arrivals
    })
    
    with pytest.raises(ValueError, match="Missing required column"):
        update_data.clean_and_standardize_data(invalid_raw)
