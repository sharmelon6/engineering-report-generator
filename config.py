# -------------------------------------------------
# Project Configuration
# -------------------------------------------------

# Input file
DATA_FILE_PATH = "sample_wastewater_data.xlsx"

# Output folders
CHARTS_DIR = "charts"
REPORTS_DIR = "reports"

# Report output files
RULE_BASED_REPORT_FILE = "wastewater_performance_report.md"
HTML_REPORT_FILE = "wastewater_performance_report.html"
LLM_REPORT_FILE = "llm_wastewater_performance_report.md"

# Wastewater process thresholds
LOW_DO_THRESHOLD_MG_L = 2.0
HIGH_EFFLUENT_AMMONIA_THRESHOLD_MG_L = 10.0
TARGET_AMMONIA_REMOVAL_PERCENT = 90.0

# Recommended operating ranges
MIN_PH = 6.5
MAX_PH = 8.5
MIN_TEMP_C = 15.0
MAX_TEMP_C = 35.0

# LLM settings
LLM_MODEL = "gemini-2.5-flash"
LLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"