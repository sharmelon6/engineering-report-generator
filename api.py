from pathlib import Path
import shutil
import tempfile
import traceback
import numpy as np

from fastapi import FastAPI, File, HTTPException, UploadFile

from calculations import calculate_engineering_metrics
from data_loader import (
    load_wastewater_data,
    validate_numeric_columns,
    validate_wastewater_columns,
)
from html_report_generator import generate_html_report
from llm_report_generator import generate_llm_engineering_report
from plotting import generate_charts
from report_generator import generate_markdown_report
from config import REPORTS_DIR, LLM_REPORT_FILE


# -------------------------------------------------
# FastAPI Application
# -------------------------------------------------

app = FastAPI(
    title="Engineering Report Generator API",
    description=(
        "Upload wastewater operating data as an Excel file and generate "
        "engineering metrics, charts, markdown reports, HTML reports, "
        "and optional AI-assisted reports."
    ),
    version="1.0.0",
)


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------


def make_json_safe(value):
    """Convert NumPy and pandas values into standard Python values."""

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, dict):
        return {
            key: make_json_safe(dictionary_value)
            for key, dictionary_value in value.items()
        }

    if isinstance(value, list):
        return [make_json_safe(list_value) for list_value in value]

    return value


def dataframe_to_records(dataframe):
    """Convert a pandas DataFrame into API-safe dictionary records."""

    records = dataframe.to_dict(orient="records")
    return make_json_safe(records)


# -------------------------------------------------
# API Routes
# -------------------------------------------------


@app.get("/")
def read_root():
    """Return a basic health message for the API."""

    return {
        "message": "Engineering Report Generator API is running.",
        "docs_url": "/docs",
    }


@app.post("/generate-report")
async def generate_report(file: UploadFile = File(...)):
    """Generate engineering reports from an uploaded Excel file."""

    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Please upload an Excel file ending in .xlsx or .xls.",
        )

    temporary_file_path = None

    try:
        print("API Step 1: Saving uploaded Excel file...")
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(file.filename).suffix,
        ) as temporary_file:
            shutil.copyfileobj(file.file, temporary_file)
            temporary_file_path = temporary_file.name

        print("API Step 2: Loading dataframe...")
        dataframe = load_wastewater_data(temporary_file_path)

        print("API Step 3: Validating dataframe columns...")
        validate_wastewater_columns(dataframe)
        validate_numeric_columns(dataframe)

        print("API Step 4: Calculating engineering metrics...")
        dataframe, results = calculate_engineering_metrics(dataframe)

        print("API Step 5: Generating charts...")
        chart_paths = generate_charts(dataframe)

        print("API Step 6: Generating markdown report...")
        markdown_report_path = generate_markdown_report(results, chart_paths)

        print("API Step 7: Generating HTML report...")
        html_report_path = generate_html_report(results, chart_paths)

        llm_report_path = None
        llm_report_status = "not_generated"

        try:
            print("API Step 8: Generating LLM report...")
            llm_report_text = generate_llm_engineering_report(results)
            llm_report_path = Path(REPORTS_DIR) / LLM_REPORT_FILE
            llm_report_path.write_text(llm_report_text)
            llm_report_status = "generated"
        except Exception as llm_error:
            print("API Step 8 skipped: LLM report generation failed.")
            print(llm_error)
            llm_report_status = f"skipped: {llm_error}"

        return {
            "status": "success",
            "uploaded_file": file.filename,
            "key_metrics": make_json_safe(
                {
                    "average_flow_m3_hr": results["avg_flow"],
                    "average_dissolved_oxygen_mg_L": results["avg_do"],
                    "average_effluent_ammonia_mg_L": results[
                        "avg_effluent_ammonia"
                    ],
                    "average_ammonia_removal_percent": results["avg_removal"],
                    "maximum_flow_m3_hr": results["max_flow"],
                    "minimum_dissolved_oxygen_mg_L": results["min_do"],
                    "maximum_effluent_ammonia_mg_L": results[
                        "max_effluent_ammonia"
                    ],
                }
            ),
            "events": {
                "low_dissolved_oxygen_events": dataframe_to_records(
                    results["low_do_events"]
                ),
                "high_effluent_ammonia_events": dataframe_to_records(
                    results["high_ammonia_events"]
                ),
                "ph_out_of_range_events": dataframe_to_records(
                    results["ph_out_of_range_events"]
                ),
                "temperature_out_of_range_events": dataframe_to_records(
                    results["temp_out_of_range_events"]
                ),
            },
            "generated_files": {
                "charts": chart_paths,
                "markdown_report": str(markdown_report_path),
                "html_report": str(html_report_path),
                "llm_report": str(llm_report_path) if llm_report_path else None,
                "llm_report_status": llm_report_status,
            },
        }

    except HTTPException:
        raise
    except Exception as error:
        print("API report generation failed with this traceback:")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Report generation failed: {error}",
        ) from error
    finally:
        file.file.close()

        if temporary_file_path is not None:
            Path(temporary_file_path).unlink(missing_ok=True)
