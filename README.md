# Engineering Report Generator

## Overview

Engineering Report Generator is an AI-assisted wastewater process analytics application built with Python. The project automates the workflow of:

1. Loading operational wastewater treatment data from Excel
2. Cleaning and validating process data
3. Performing engineering calculations
4. Detecting operational events and threshold violations
5. Generating engineering charts
6. Creating rule-based engineering summaries
7. Generating AI-assisted engineering reports using a large language model (LLM)

The project was designed as a portfolio-quality engineering analytics pipeline that combines:

- Process engineering
- Data analysis
- Python automation
- AI integration
- Modular software architecture
- Report generation

The primary engineering focus of the current version is nitrification system performance analysis.

The application now supports:

- Markdown engineering report generation
- AI-assisted engineering narrative generation
- HTML engineering report generation
- Embedded chart rendering inside HTML reports
- PDF export through browser print workflows
- Threshold-based operational diagnostics
- Process monitoring visualization
- Event flagging and engineering interpretation
- Configurable engineering constants
- Modular expansion for future FastAPI deployment

The current implementation simulates a lightweight industrial analytics pipeline that could later evolve into a production engineering monitoring platform.

The project was intentionally structured as both an engineering analytics demonstration and a software engineering portfolio project focused on AI-assisted technical reporting.

---

# Project Goals

The project was created to simulate a realistic engineering reporting workflow similar to what might exist in:

- Wastewater treatment plants
- Environmental consulting firms
- Industrial process monitoring systems
- Smart manufacturing analytics platforms
- AI-assisted engineering software

The long-term goal is to evolve the application into a production-style analytics platform using:

- FastAPI
- Real-time data ingestion
- Automated PDF reporting
- Historical trend analysis
- Frontend dashboards
- AI engineering copilots

---

# Technologies Used

## Core Technologies

- Python 3.13
- Modular Python architecture
- UV package manager
- Pandas
- Matplotlib
- OpenAI-compatible SDK
- Gemini API
- Markdown reporting
- HTML/CSS report generation

## Python Libraries

### Data Processing

- pandas
- openpyxl

### Visualization

- matplotlib

### AI Integration

- openai
- python-dotenv

---

# Why UV Was Used Instead of Pip

The project uses UV instead of traditional pip workflows.

UV was selected because it:

- Creates virtual environments automatically
- Installs packages significantly faster
- Simplifies dependency management
- Improves reproducibility
- Reduces environment setup friction

Example commands used during development:

```bash
uv init
uv venv
uv add pandas matplotlib openpyxl
uv add openai python-dotenv
uv run main.py
```

---

# Project Structure

```text
Engineering-Report-Generator/
│
├── charts/
│   ├── ammonia_over_time.png
│   ├── dissolved_oxygen_over_time.png
│   ├── flow_over_time.png
│   └── ammonia_removal_efficiency.png
│
├── reports/
│   ├── wastewater_performance_report.md
│   ├── wastewater_performance_report.html
│   └── llm_wastewater_performance_report.md
│
├── sample_wastewater_data.xlsx
│
├── data_loader.py
├── calculations.py
├── plotting.py
├── report_generator.py
├── html_report_generator.py
├── llm_report_generator.py
├── config.py
├── main.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# System Workflow

The application follows a modular engineering workflow.

## Step 1 — Load Data

The system imports wastewater operational data from an Excel spreadsheet.

Handled in:

```text
data_loader.py
```

Responsibilities:

- Load Excel files using pandas
- Clean column names
- Validate required process variables
- Print dataset previews
- Generate descriptive statistics

Example variables:

- Flow rate
- Influent ammonia
- Effluent ammonia
- Dissolved oxygen
- pH
- Temperature
- Nitrate concentration
- Energy usage

---

## Step 2 — Perform Engineering Calculations

Handled in:

```text
calculations.py
```

Engineering metrics currently calculated:

### Ammonia Removal Efficiency

Formula:

```text
((Influent Ammonia - Effluent Ammonia) / Influent Ammonia) × 100
```

### Statistical Metrics

- Average flow rate
- Average dissolved oxygen
- Average effluent ammonia
- Average removal efficiency
- Maximum flow
- Minimum dissolved oxygen
- Maximum effluent ammonia

### Event Detection

The application identifies:

- Low dissolved oxygen events
- High effluent ammonia events

Current thresholds:

```python
DO < 2.0 mg/L
Effluent ammonia > 10.0 mg/L
```

These thresholds were intentionally hardcoded for the proof-of-concept version.

Future versions will support configurable plant settings.

---

## Step 3 — Generate Charts

Handled in:

```text
plotting.py
```

The application automatically generates engineering trend charts.

Current charts:

1. Ammonia concentration over time
2. Dissolved oxygen over time
3. Flow rate over time
4. Ammonia removal efficiency over time

Charts are saved automatically into:

```text
charts/
```

The visualization layer was designed to simulate engineering reporting software used in industrial operations.

---

## Step 4 — Generate Rule-Based Engineering Report

Handled in:

```text
report_generator.py
```

This module creates a deterministic engineering summary using:

- Calculated metrics
- Event detection
- Fixed engineering logic

The generated report includes:

- Executive summary
- Key metrics
- Event detection
- Engineering interpretation
- Recommended operational checks
- System limitations

Output:

```text
reports/wastewater_performance_report.md
```

---

## Step 5 — Generate HTML Engineering Report

Handled in:

```text
html_report_generator.py
```

This module converts engineering results into a styled HTML engineering report.

The HTML reporting layer was added to simulate modern engineering dashboard and reporting systems used in:

- Industrial analytics platforms
- Manufacturing reporting tools
- Environmental compliance systems
- SCADA-adjacent monitoring software
- Operations intelligence dashboards

The HTML report includes:

- Responsive styling
- Structured engineering sections
- Embedded engineering charts
- Metric tables
- Event summaries
- Engineering interpretation
- Operational conclusions
- System limitations

Charts are embedded directly into the HTML file using base64 encoding.

This approach was selected because it:

- Prevents broken image references
- Allows standalone report portability
- Improves PDF export reliability
- Simplifies browser rendering
- Eliminates dependency on external chart files

The HTML report can be:

- Viewed directly in a browser
- Shared as a standalone file
- Printed to PDF
- Embedded into future web applications

Generated output:

```text
reports/wastewater_performance_report.html
```

---

## Step 6 — Generate AI-Assisted Engineering Report

Handled in:

```text
llm_report_generator.py
```

This module integrates a large language model to generate a more natural engineering interpretation.

The system currently uses:

```text
Gemini 2.5 Flash
```

through Google's OpenAI-compatible API endpoint.

The implementation uses the official OpenAI Python SDK configured against Google's Gemini-compatible endpoint.

The AI receives:

- Engineering metrics
- Detected operational events
- Threshold results
- Process performance information

The LLM then generates:

- Engineering observations
- Root cause discussion
- Operational concerns
- Recommended actions
- Final assessment

---

# AI Prompt Engineering Methodology

A significant part of the project involved refining LLM behavior.

Early versions of the AI report incorrectly invented:

- Fake dates
- Fake operators
- Fake plant names
- Overconfident conclusions
- Memo headers

The prompt was refined to:

- Prevent hallucinated details
- Require cautious engineering wording
- Limit conclusions to supplied metrics
- Avoid unsupported causation claims
- Use professional engineering language

Example guidance added to the prompt:

```text
- the data suggests
- may indicate
- likely contributor
- cannot be confirmed without additional data
```

This stage demonstrated practical prompt engineering and AI output control.

Additional methodology improvements included:

- Restricting unsupported certainty statements
- Preventing fabricated operational history
- Preventing fabricated maintenance recommendations
- Limiting assumptions about root cause
- Structuring AI outputs similarly to engineering consulting summaries
- Separating deterministic calculations from probabilistic AI interpretation

The final architecture intentionally keeps engineering calculations deterministic while allowing the LLM to assist with narrative interpretation.

This separation helps reduce engineering risk and improves explainability.

---

# AI Integration Process

The project originally attempted to use older Gemini models and required debugging of:

- API configuration
- Billing setup
- Model compatibility
- OpenAI-compatible endpoints
- SDK integration
- Environment variable loading

Final working configuration:

```python
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
```

Model used:

```python
model="gemini-2.5-flash"
```

---

# HTML Report Generation Methodology

The HTML reporting layer was designed to simulate how industrial engineering software platforms generate executive-ready process reports.

The implementation uses:

- Pure Python HTML generation
- Embedded CSS styling
- Base64 image embedding
- Dynamic chart insertion
- Section-based layout architecture

The charts are generated using Matplotlib and then converted into embedded base64 images.

This design decision solved several common engineering reporting issues:

## Problem: Broken Relative Image Paths

Early HTML versions referenced external PNG files directly.

When exported to PDF or shared externally, charts could fail to render.

## Solution: Base64 Embedded Charts

Charts are now encoded directly into the HTML document.

Advantages:

- Fully self-contained reports
- Portable HTML output
- Reliable PDF export
- Browser compatibility
- Easier deployment in future APIs

This methodology mirrors techniques commonly used in:

- Automated reporting systems
- Enterprise dashboards
- Analytics software
- Industrial reporting tools
- Email-generated reports

---

# Lessons Learned During Development

## Software Engineering

- Modular architecture design
- Separating concerns across files
- Environment management with UV
- Dependency management
- Debugging package issues
- API integration workflows

## Data Engineering

- Cleaning column names
- Data validation
- Statistical analysis
- Threshold logic
- Event detection

## AI Engineering

- LLM API integration
- Prompt engineering
- Hallucination reduction
- Response formatting
- Engineering-safe language generation

## Process Engineering

- Nitrification monitoring
- Dissolved oxygen limitations
- Ammonia removal performance
- Operational diagnostics
- Engineering interpretation

---


# Future Improvements

## Future Product Direction — Generalized Engineering Analytics Platform

The current implementation is intentionally scoped to wastewater nitrification analysis.

This design decision allows the engineering calculations, threshold logic, and operational interpretation to remain deterministic and explainable.

A future version of the platform could evolve into a generalized engineering analytics system capable of processing many different engineering datasets.

Potential future workflow:

```text
Excel Upload
    ↓
Dataset Profiling
    ↓
Template Detection
    ↓
Engineering Calculations
    ↓
Automatic Chart Generation
    ↓
AI-Assisted Interpretation
    ↓
HTML/PDF Report Export
```

Future generalized capabilities may include:

### Dataset Profiling

The system could automatically inspect uploaded datasets and identify:

- Numeric columns
- Time-series columns
- Missing values
- Potential process variables
- Units embedded in column names
- Input/output relationships

### Template-Based Engineering Logic

Future versions may support reusable engineering templates such as:

```text
templates/
├── wastewater.py
├── heat_exchanger.py
├── batch_reactor.py
├── distillation.py
└── generic.py
```

Each template could define:

- Engineering equations
- Process thresholds
- Recommended visualizations
- Operational diagnostics
- Domain-specific report logic

### Automatic Visualization Selection

The platform could dynamically generate charts based on detected data structures.

Examples:

- Time-series trend plots
- Scatter plots
- Correlation heatmaps
- Distribution plots
- Process performance dashboards
- Anomaly visualization

### Generic AI-Assisted Reporting

When no engineering template exists, the AI layer could still generate:

- Statistical summaries
- Trend interpretations
- Operational observations
- Potential anomalies
- Suggested investigation areas

### Long-Term Vision

The long-term vision is to evolve the project into a modular AI-assisted engineering analytics platform capable of supporting:

- Environmental systems
- Manufacturing systems
- Chemical process operations
- Industrial IoT analytics
- Smart plant monitoring
- Engineering consulting workflows
- Automated technical reporting

## Backend Development

Planned FastAPI integration:

```text
POST /analyze
```

Potential API functionality:

- Upload Excel files
- Return metrics as JSON
- Generate downloadable reports
- Trigger AI analysis
- Serve generated charts

---

## Planned Engineering Features

### Advanced Analytics

- Rolling averages
- Historical baselines
- Trend analysis
- Anomaly detection
- Energy efficiency metrics
- Aeration efficiency calculations

### Reporting

- PDF export
- Automated email reports
- Executive dashboards
- Historical comparisons
- Browser-based HTML dashboards
- Interactive engineering charts
- Multi-page engineering report templates
- Automatic PDF generation
- Client-ready branded reports

### Configuration System

Future versions may support:

```json
{
  "low_do_threshold": 2.0,
  "high_ammonia_threshold": 10.0
}
```

---

# How To Run The Project

## 1. Clone Repository

```bash
git clone <repository-url>
cd Engineering-Report-Generator
```

## 2. Create Environment

```bash
uv venv
```

## 3. Install Dependencies

```bash
uv add pandas matplotlib openpyxl openai python-dotenv
```

## 4. Create Environment File

Create:

```text
.env
```

Add:

```text
GEMINI_API_KEY=your_api_key_here
```

---

## 5. Run Application

```bash
uv run main.py
```

### Optional: Open HTML Report Automatically

After the application finishes running, open the generated HTML report in your browser:

```bash
open reports/wastewater_performance_report.html
```

This launches the fully formatted engineering report with embedded charts.

---

# Generated Outputs

## Charts

Saved to:

```text
charts/
```

## Rule-Based Report

Saved to:

```text
reports/wastewater_performance_report.md
```

## HTML Engineering Report

Saved to:

```text
reports/wastewater_performance_report.html
```

## AI-Assisted Report

Saved to:

```text
reports/llm_wastewater_performance_report.md
```

---

# Current Status

The project currently functions as a fully operational proof-of-concept engineering analytics pipeline.

Completed capabilities:

- Excel ingestion
- Data validation
- Engineering calculations
- Event detection
- Chart generation
- Rule-based reporting
- AI-assisted reporting
- Gemini API integration
- Modular software structure

---

# Engineering and Software Design Philosophy

The project was intentionally designed using modular engineering software principles.

Each major responsibility was isolated into its own module:

| Module | Responsibility |
|---|---|
| `data_loader.py` | Data ingestion and validation |
| `calculations.py` | Engineering calculations and event detection |
| `plotting.py` | Engineering visualization generation |
| `report_generator.py` | Deterministic engineering report generation |
| `html_report_generator.py` | Styled HTML report generation |
| `llm_report_generator.py` | AI-assisted engineering interpretation |
| `main.py` | System orchestration |
| `config.py` | Centralized configuration |

This architecture improves:

- Maintainability
- Scalability
- Testing capability
- Future API integration
- Future frontend integration
- Explainability
- Engineering traceability

The project intentionally separates:

- Engineering calculations
- Visualization logic
- AI interpretation
- File generation
- Configuration management

This makes the system easier to debug, extend, and productionize.

The current implementation acts as a proof-of-concept for a larger AI-assisted engineering analytics platform.

---

# Author

Shivank Sharma

Chemical Engineering Student

AI + Engineering Analytics Project