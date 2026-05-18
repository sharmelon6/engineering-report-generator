from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import (
    CHARTS_DIR,
    LOW_DO_THRESHOLD_MG_L,
    HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L,
    TARGET_AMMONIA_REMOVAL_PERCENT,
)


# -------------------------------------------------
# Chart Generation
# -------------------------------------------------


def generate_charts(df: pd.DataFrame):
    """Generate wastewater engineering charts and save them as PNG files."""

    charts_dir = Path(CHARTS_DIR)
    charts_dir.mkdir(exist_ok=True)

    chart_paths = []

    # -------------------------------------------------
    # Chart 1: Influent and Effluent Ammonia Over Time
    # -------------------------------------------------
    ammonia_chart_path = charts_dir / "ammonia_over_time.png"

    plt.figure(figsize=(10, 6))
    plt.plot(
        df["time_hr"],
        df["ammonia_in_mg_L"],
        marker="o",
        label="Influent Ammonia",
    )
    plt.plot(
        df["time_hr"],
        df["ammonia_out_mg_L"],
        marker="o",
        label="Effluent Ammonia",
    )
    plt.axhline(
        y=HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L,
        linestyle="--",
        label="Effluent Ammonia Alert Level",
    )
    plt.fill_between(
        df["time_hr"],
        df["ammonia_out_mg_L"],
        HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L,
        where=(
            df["ammonia_out_mg_L"]
            > HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L
        ),
        alpha=0.2,
        label="High Ammonia Event",
    )
    plt.title("Influent and Effluent Ammonia Over Time")
    plt.xlabel("Time (hr)")
    plt.ylabel("Ammonia (mg/L)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(ammonia_chart_path)
    plt.close()

    chart_paths.append(str(ammonia_chart_path))

    # -------------------------------------------------
    # Chart 2: Dissolved Oxygen Over Time
    # -------------------------------------------------
    do_chart_path = charts_dir / "dissolved_oxygen_over_time.png"

    plt.figure(figsize=(10, 6))
    plt.plot(
        df["time_hr"],
        df["dissolved_oxygen_mg_L"],
        marker="o",
        label="Dissolved Oxygen",
    )
    plt.axhline(
        y=LOW_DO_THRESHOLD_MG_L,
        linestyle="--",
        label="Low DO Threshold",
    )
    plt.fill_between(
        df["time_hr"],
        df["dissolved_oxygen_mg_L"],
        LOW_DO_THRESHOLD_MG_L,
        where=(
            df["dissolved_oxygen_mg_L"]
            < LOW_DO_THRESHOLD_MG_L
        ),
        alpha=0.2,
        label="Low DO Event",
    )
    plt.title("Dissolved Oxygen Over Time")
    plt.xlabel("Time (hr)")
    plt.ylabel("Dissolved Oxygen (mg/L)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(do_chart_path)
    plt.close()

    chart_paths.append(str(do_chart_path))

    # -------------------------------------------------
    # Chart 3: Flow Rate Over Time
    # -------------------------------------------------
    flow_chart_path = charts_dir / "flow_over_time.png"

    average_flow = df["flow_m3_hr"].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(
        df["time_hr"],
        df["flow_m3_hr"],
        marker="o",
        label="Flow Rate",
    )
    plt.axhline(
        y=average_flow,
        linestyle="--",
        label="Average Flow",
    )
    plt.title("Flow Rate Over Time")
    plt.xlabel("Time (hr)")
    plt.ylabel("Flow Rate (m³/hr)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(flow_chart_path)
    plt.close()

    chart_paths.append(str(flow_chart_path))

    # -------------------------------------------------
    # Chart 4: Ammonia Removal Efficiency Over Time
    # -------------------------------------------------
    removal_chart_path = charts_dir / "ammonia_removal_efficiency.png"

    plt.figure(figsize=(10, 6))
    plt.plot(
        df["time_hr"],
        df["ammonia_removal_percent"],
        marker="o",
        label="Ammonia Removal Efficiency",
    )
    plt.axhline(
        y=TARGET_AMMONIA_REMOVAL_PERCENT,
        linestyle="--",
        label="Target Removal Efficiency",
    )
    plt.title("Ammonia Removal Efficiency Over Time")
    plt.xlabel("Time (hr)")
    plt.ylabel("Removal Efficiency (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(removal_chart_path)
    plt.close()

    chart_paths.append(str(removal_chart_path))

    return chart_paths
