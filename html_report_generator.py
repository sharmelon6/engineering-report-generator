import base64
from datetime import datetime
from pathlib import Path

from config import (
    REPORTS_DIR,
    HTML_REPORT_FILE,
    LOW_DO_THRESHOLD_MG_L,
    MIN_PH,
    MAX_PH,
    MIN_TEMP_C,
    MAX_TEMP_C,
)


# -------------------------------------------------
# HTML Report Generation
# -------------------------------------------------


def generate_html_report(results: dict, chart_paths: list):
    """Generate a browser-friendly HTML wastewater engineering report."""

    reports_dir = Path(REPORTS_DIR)
    reports_dir.mkdir(exist_ok=True)

    generated_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    low_do_events = results["low_do_events"]
    high_ammonia_events = results["high_ammonia_events"]
    ph_out_of_range_events = results["ph_out_of_range_events"]
    temp_out_of_range_events = results["temp_out_of_range_events"]

    low_do_start = (
        low_do_events["time_hr"].min()
        if not low_do_events.empty
        else "None"
    )

    low_do_end = (
        low_do_events["time_hr"].max()
        if not low_do_events.empty
        else "None"
    )

    high_ammonia_start = (
        high_ammonia_events["time_hr"].min()
        if not high_ammonia_events.empty
        else "None"
    )

    high_ammonia_end = (
        high_ammonia_events["time_hr"].max()
        if not high_ammonia_events.empty
        else "None"
    )

    ph_event_summary = (
        "No pH out-of-range events detected."
        if ph_out_of_range_events.empty
        else f"pH out-of-range events detected at hours "
        f"{ph_out_of_range_events['time_hr'].tolist()}."
    )

    temp_event_summary = (
        "No temperature out-of-range events detected."
        if temp_out_of_range_events.empty
        else f"Temperature out-of-range events detected at hours "
        f"{temp_out_of_range_events['time_hr'].tolist()}."
    )

    chart_captions = [
        "Influent and effluent ammonia concentration trends.",
        "Dissolved oxygen concentration profile and low oxygen event window.",
        "Flow rate trend during the operating period.",
        "Ammonia removal efficiency performance over time.",
    ]

    chart_cards = ""

    for i, chart_path in enumerate(chart_paths):
        chart_file = Path(chart_path)

        if chart_file.exists():
            encoded_chart = base64.b64encode(
                chart_file.read_bytes()
            ).decode("utf-8")

            chart_image_html = (
                f'<img src="data:image/png;base64,{encoded_chart}" '
                f'alt="{chart_captions[i]}">'
            )
        else:
            chart_image_html = (
                f'<p class="missing-chart">Chart image not found: '
                f'{chart_path}</p>'
            )

        chart_cards += f"""
            <section class="chart-card">
                <h3>Chart {i + 1}</h3>
                <p>{chart_captions[i]}</p>
                {chart_image_html}
            </section>
        """

    html_text = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wastewater Nitrification Performance Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            background: #f5f7fa;
            color: #1f2937;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 40px 24px;
        }}

        .header, .section {{
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }}

        h1, h2, h3 {{
            color: #111827;
        }}

        .timestamp {{
            color: #6b7280;
            font-size: 0.95rem;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }}

        th, td {{
            border: 1px solid #d1d5db;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #e5e7eb;
        }}

        .event-list li {{
            margin-bottom: 8px;
        }}

        .chart-card {{
            margin-top: 24px;
            padding-top: 12px;
            border-top: 1px solid #e5e7eb;
        }}

        .chart-card img {{
            width: 100%;
            max-width: 950px;
            display: block;
            margin: 16px auto;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background: white;
        }}

        .note {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px 16px;
            border-radius: 8px;
        }}

        .missing-chart {{
            color: #b91c1c;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <main class="container">
        <section class="header">
            <h1>Wastewater Nitrification Performance Report</h1>
            <p class="timestamp">Generated: {generated_timestamp}</p>
        </section>

        <section class="section">
            <h2>Executive Summary</h2>
            <p>The wastewater system experienced a temporary nitrification performance decline during the 24-hour operating period. The issue aligned with a flow increase, dissolved oxygen drop, and rise in effluent ammonia.</p>
        </section>

        <section class="section">
            <h2>Key Metrics</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Average Flow Rate</td><td>{results['avg_flow']:.2f} m³/hr</td></tr>
                <tr><td>Maximum Flow Rate</td><td>{results['max_flow']:.2f} m³/hr</td></tr>
                <tr><td>Average Dissolved Oxygen</td><td>{results['avg_do']:.2f} mg/L</td></tr>
                <tr><td>Minimum Dissolved Oxygen</td><td>{results['min_do']:.2f} mg/L</td></tr>
                <tr><td>Average Effluent Ammonia</td><td>{results['avg_effluent_ammonia']:.2f} mg/L</td></tr>
                <tr><td>Maximum Effluent Ammonia</td><td>{results['max_effluent_ammonia']:.2f} mg/L</td></tr>
                <tr><td>Average Ammonia Removal Efficiency</td><td>{results['avg_removal']:.2f}%</td></tr>
            </table>
        </section>

        <section class="section">
            <h2>Event Detection</h2>
            <ul class="event-list">
                <li>Low dissolved oxygen events occurred from hour {low_do_start} to hour {low_do_end}.</li>
                <li>High effluent ammonia events occurred from hour {high_ammonia_start} to hour {high_ammonia_end}.</li>
                <li>{ph_event_summary}</li>
                <li>{temp_event_summary}</li>
            </ul>
        </section>

        <section class="section">
            <h2>Engineering Interpretation</h2>
            <p>The data suggests that the flow spike likely increased loading on the system. During the same period, dissolved oxygen dropped below {LOW_DO_THRESHOLD_MG_L} mg/L, which may have limited nitrifying bacteria activity. As dissolved oxygen decreased, effluent ammonia increased and ammonia removal efficiency declined.</p>
            <p>The peak flow occurred near the same period as the lowest dissolved oxygen and highest effluent ammonia values. This suggests the system may have been aeration-limited during the loading event.</p>
        </section>

        <section class="section">
            <h2>Recommended Checks</h2>
            <ol>
                <li>Review aeration capacity during high-flow periods.</li>
                <li>Check blower performance and dissolved oxygen control settings.</li>
                <li>Review influent loading patterns during hours 8 through 16.</li>
                <li>Confirm whether pH stayed within the configured range of {MIN_PH} to {MAX_PH}.</li>
                <li>Confirm whether temperature stayed within the configured range of {MIN_TEMP_C}°C to {MAX_TEMP_C}°C.</li>
                <li>Investigate whether added aeration control logic is needed during flow spikes.</li>
            </ol>
        </section>

        <section class="section">
            <h2>Process Monitoring Charts</h2>
            {chart_cards}
        </section>

        <section class="section">
            <h2>Operational Conclusion</h2>
            <p>The operating data is consistent with a temporary nitrification upset associated with increased hydraulic loading and reduced dissolved oxygen concentration. The pH and temperature checks provide additional screening context for whether other operating conditions may have contributed to the observed performance decline.</p>
        </section>

        <section class="section">
            <h2>Limitations</h2>
            <p class="note">This report is based on a small sample dataset and rule-based calculations. A production version should include longer time windows, real plant thresholds, sensor validation, and historical baseline comparison.</p>
        </section>
    </main>
</body>
</html>
"""

    html_report_path = reports_dir / HTML_REPORT_FILE
    html_report_path.write_text(html_text)

    return html_report_path