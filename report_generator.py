from pathlib import Path

from config import REPORTS_DIR, RULE_BASED_REPORT_FILE


# -------------------------------------------------
# Markdown Report Generator
# -------------------------------------------------


def generate_markdown_report(results: dict, chart_paths: list[str]):
    """Generate a markdown engineering report."""

    reports_dir = Path(REPORTS_DIR)
    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / RULE_BASED_REPORT_FILE

    markdown_text = f"""
# Wastewater Treatment Engineering Performance Report

## Executive Summary

This report summarizes wastewater treatment plant operational performance
using engineering calculations, threshold monitoring, and trend analysis.

---

## Key Engineering Metrics

| Metric | Value |
|---|---|
| Average Flow Rate | {results['avg_flow']:.2f} m³/hr |
| Average Dissolved Oxygen | {results['avg_do']:.2f} mg/L |
| Average Effluent Ammonia | {results['avg_effluent_ammonia']:.2f} mg/L |
| Average Ammonia Removal Efficiency | {results['avg_removal']:.2f}% |
| Maximum Flow Rate | {results['max_flow']:.2f} m³/hr |
| Minimum Dissolved Oxygen | {results['min_do']:.2f} mg/L |
| Maximum Effluent Ammonia | {results['max_effluent_ammonia']:.2f} mg/L |

---

## Process Monitoring Events

### Low Dissolved Oxygen Events

{results['low_do_events'].to_markdown(index=False)}

### High Effluent Ammonia Events

{results['high_ammonia_events'].to_markdown(index=False)}

### pH Out-of-Range Events

{results['ph_out_of_range_events'].to_markdown(index=False)}

### Temperature Out-of-Range Events

{results['temp_out_of_range_events'].to_markdown(index=False)}

---

## Process Monitoring Charts

### Chart 1

Influent and effluent ammonia concentration trends.

![Chart 1](../{chart_paths[0]})

---

### Chart 2

Dissolved oxygen concentration profile and low oxygen event window.

![Chart 2](../{chart_paths[1]})

---

### Chart 3

Flow rate trend during the operating period.

![Chart 3](../{chart_paths[2]})

---

### Chart 4

Ammonia removal efficiency performance over time.

![Chart 4](../{chart_paths[3]})

---

## Operational Conclusion

The operating data is consistent with a temporary nitrification upset associated
with increased hydraulic loading and reduced dissolved oxygen availability.

The elevated effluent ammonia concentrations observed during hours 8–16 align
with periods of depressed dissolved oxygen concentrations below the engineering
threshold of 2.0 mg/L.

No significant pH or temperature excursions were identified during the analysis
period.

---

## Limitations

This report is based solely on the provided operational dataset and does not
include laboratory verification, process modeling, or biological kinetics
simulation.
"""

    report_path.write_text(markdown_text)

    return report_path
