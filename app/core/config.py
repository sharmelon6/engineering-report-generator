import os
from dotenv import load_dotenv


# -------------------------------------------------
# Environment Configuration
# -------------------------------------------------

load_dotenv()


def get_float_env(variable_name: str, default_value: float) -> float:
    """Read a float environment variable with a safe default value."""

    raw_value = os.getenv(variable_name)

    if raw_value is None or raw_value.strip() == "":
        return default_value

    return float(raw_value)


# -------------------------------------------------
# File and Folder Paths
# -------------------------------------------------

DATA_FILE_PATH = os.getenv(
    "DATA_FILE_PATH",
    "sample_wastewater_data.xlsx",
)

CHARTS_DIR = os.getenv(
    "CHARTS_DIR",
    "charts",
)

REPORTS_DIR = os.getenv(
    "REPORTS_DIR",
    "reports",
)

RULE_BASED_REPORT_FILE = os.getenv(
    "RULE_BASED_REPORT_FILE",
    "wastewater_performance_report.md",
)

HTML_REPORT_FILE = os.getenv(
    "HTML_REPORT_FILE",
    "wastewater_performance_report.html",
)

LLM_REPORT_FILE = os.getenv(
    "LLM_REPORT_FILE",
    "llm_wastewater_performance_report.md",
)


# -------------------------------------------------
# Wastewater Engineering Thresholds
# -------------------------------------------------

LOW_DO_THRESHOLD_MG_L = get_float_env(
    "LOW_DO_THRESHOLD_MG_L",
    2.0,
)

HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L = get_float_env(
    "HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L",
    10.0,
)

TARGET_AMMONIA_REMOVAL_PERCENT = get_float_env(
    "TARGET_AMMONIA_REMOVAL_PERCENT",
    90.0,
)

MIN_PH = get_float_env(
    "MIN_PH",
    6.5,
)

MAX_PH = get_float_env(
    "MAX_PH",
    8.5,
)

MIN_TEMP_C = get_float_env(
    "MIN_TEMP_C",
    15.0,
)

MAX_TEMP_C = get_float_env(
    "MAX_TEMP_C",
    35.0,
)


# -------------------------------------------------
# LLM Configuration
# -------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gemini-2.5-flash",
)

LLM_BASE_URL = os.getenv(
    "LLM_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/",
)