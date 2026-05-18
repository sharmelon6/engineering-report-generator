import pandas as pd
from app.core.config import (
    LOW_DO_THRESHOLD_MG_L,
    HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L,
    MIN_PH,
    MAX_PH,
    MIN_TEMP_C,
    MAX_TEMP_C,
)


# -------------------------------------------------
# Engineering Calculations
# -------------------------------------------------


def calculate_engineering_metrics(df: pd.DataFrame):
    """Run wastewater engineering calculations and event detection."""

    # Ammonia removal efficiency
    df["ammonia_removal_percent"] = (
        (df["ammonia_in_mg_L"] - df["ammonia_out_mg_L"])
        / df["ammonia_in_mg_L"]
    ) * 100

    # Average values
    avg_flow = df["flow_m3_hr"].mean()
    avg_do = df["dissolved_oxygen_mg_L"].mean()
    avg_effluent_ammonia = df["ammonia_out_mg_L"].mean()
    avg_removal = df["ammonia_removal_percent"].mean()

    # Maximum and minimum values
    max_flow = df["flow_m3_hr"].max()
    min_do = df["dissolved_oxygen_mg_L"].min()
    max_effluent_ammonia = df["ammonia_out_mg_L"].max()

    # Threshold checks
    low_do_events = df[
        df["dissolved_oxygen_mg_L"] < LOW_DO_THRESHOLD_MG_L
    ]

    high_ammonia_events = df[
        df["ammonia_out_mg_L"] > HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L
    ]

    ph_out_of_range_events = df[
        (df["pH"] < MIN_PH) | (df["pH"] > MAX_PH)
    ]

    temp_out_of_range_events = df[
        (df["temp_C"] < MIN_TEMP_C) | (df["temp_C"] > MAX_TEMP_C)
    ]

    results = {
        "avg_flow": avg_flow,
        "avg_do": avg_do,
        "avg_effluent_ammonia": avg_effluent_ammonia,
        "avg_removal": avg_removal,
        "max_flow": max_flow,
        "min_do": min_do,
        "max_effluent_ammonia": max_effluent_ammonia,
        "low_do_events": low_do_events,
        "high_ammonia_events": high_ammonia_events,
        "ph_out_of_range_events": ph_out_of_range_events,
        "temp_out_of_range_events": temp_out_of_range_events,
    }

    return df, results


# -------------------------------------------------
# Console Output
# -------------------------------------------------


def print_engineering_results(results: dict):
    """Print engineering metrics to terminal."""

    print("\nEngineering Results")
    print("-" * 40)

    print(f"Average Flow Rate: {results['avg_flow']:.2f} m^3/hr")
    print(f"Average Dissolved Oxygen: {results['avg_do']:.2f} mg/L")
    print(
        f"Average Effluent Ammonia: "
        f"{results['avg_effluent_ammonia']:.2f} mg/L"
    )
    print(f"Average Ammonia Removal: {results['avg_removal']:.2f}%")

    print(f"\nMaximum Flow Rate: {results['max_flow']} m^3/hr")
    print(f"Minimum Dissolved Oxygen: {results['min_do']} mg/L")
    print(
        f"Maximum Effluent Ammonia: "
        f"{results['max_effluent_ammonia']} mg/L"
    )

    print(
        f"\nLow Dissolved Oxygen Events "
        f"(<{LOW_DO_THRESHOLD_MG_L} mg/L):"
    )
    print(results["low_do_events"][["time_hr", "dissolved_oxygen_mg_L"]])

    print(
        f"\nHigh Effluent Ammonia Events "
        f"(>{HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L} mg/L):"
    )
    print(results["high_ammonia_events"][["time_hr", "ammonia_out_mg_L"]])

    print(
        f"\npH Out-of-Range Events "
        f"(<{MIN_PH} or >{MAX_PH}):"
    )
    print(results["ph_out_of_range_events"][["time_hr", "pH"]])

    print(
        f"\nTemperature Out-of-Range Events "
        f"(<{MIN_TEMP_C}°C or >{MAX_TEMP_C}°C):"
    )
    print(results["temp_out_of_range_events"][["time_hr", "temp_C"]])
