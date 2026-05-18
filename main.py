from pathlib import Path

from dotenv import load_dotenv
from app.core.config import (
    DATA_FILE_PATH,
    REPORTS_DIR,
    LLM_REPORT_FILE,
)

from app.services.calculations import calculate_engineering_metrics, print_engineering_results
from app.services.data_loader import (
    load_wastewater_data,
    validate_wastewater_columns,
    validate_numeric_columns,
)
from app.services.plotting import generate_charts
from app.reports.markdown_report import generate_markdown_report
from app.reports.html_report import generate_html_report
from app.reports.llm_report import generate_llm_engineering_report


# -------------------------------------------------
# Main Project Workflow
# -------------------------------------------------


def main():
    """Run the wastewater engineering report generation workflow."""

    file_path = DATA_FILE_PATH

    # Load and validate data
    df = load_wastewater_data(file_path)

    validate_wastewater_columns(df)
    validate_numeric_columns(df)

    # Show basic dataset information
    print("\nCleaned Column Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nStatistics:")
    print(df.describe())

    # Run engineering calculations
    df, results = calculate_engineering_metrics(df)
    print_engineering_results(results)

    # Generate charts
    chart_paths = generate_charts(df)

    print("\nCharts saved to the charts folder:")
    for chart_path in chart_paths:
        print(f"- {chart_path}")

    # Generate markdown report
    report_path = generate_markdown_report(results, chart_paths)

    print("\nReport saved:")
    print(f"- {report_path}")

    # Generate HTML report for browser-based demo viewing
    html_report_path = generate_html_report(results, chart_paths)

    print("\nHTML report saved:")
    print(f"- {html_report_path}")

    # Generate AI-written engineering report
    try:
        llm_report_text = generate_llm_engineering_report(results)

        llm_report_path = (
            Path(REPORTS_DIR) / LLM_REPORT_FILE
        )

        llm_report_path.write_text(llm_report_text)

        print("\nLLM report saved:")
        print(f"- {llm_report_path}")

    except Exception as error:
        print("\nLLM report skipped:")
        print(f"- {error}")


if __name__ == "__main__":
    load_dotenv()
    main()