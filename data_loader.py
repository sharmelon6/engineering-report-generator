# data loader

import pandas as pd
from pathlib import Path


def load_wastewater_data(file_path: str) -> pd.DataFrame:
    """Load wastewater data from an Excel file and clean column names."""

    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(
            f"Wastewater data file not found: {file_path}"
        )

    try:
        df = pd.read_excel(file)
    except Exception as error:
        raise ValueError(
            f"Failed to read Excel file: {error}"
        ) from error

    if df.empty:
        raise ValueError("The uploaded Excel file is empty.")

    # Clean column names
    df.columns = df.columns.str.strip()

    return df


def validate_wastewater_columns(df: pd.DataFrame) -> None:
    """Confirm that the uploaded dataset contains all required columns."""
    required_columns = [
        "time_hr",
        "flow_m3_hr",
        "ammonia_in_mg_L",
        "ammonia_out_mg_L",
        "dissolved_oxygen_mg_L",
        "pH",
        "temp_C",
        "nitrate_mg_L",
        "energy_kWh",
    ]

    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: {missing_columns}\n"
            f"Columns found in Excel file: {df.columns.tolist()}"
        )


def validate_numeric_columns(df: pd.DataFrame) -> None:
    """Validate that key wastewater columns contain numeric data."""

    numeric_columns = [
        "time_hr",
        "flow_m3_hr",
        "ammonia_in_mg_L",
        "ammonia_out_mg_L",
        "dissolved_oxygen_mg_L",
        "pH",
        "temp_C",
        "nitrate_mg_L",
        "energy_kWh",
    ]

    for column in numeric_columns:
        try:
            pd.to_numeric(df[column])
        except Exception as error:
            raise ValueError(
                f"Column '{column}' contains non-numeric data."
            ) from error