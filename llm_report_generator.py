import os

from openai import OpenAI
from config import (
    LLM_MODEL,
    LLM_BASE_URL,
    MIN_PH,
    MAX_PH,
    MIN_TEMP_C,
    MAX_TEMP_C,
)


# -------------------------------------------------
# OpenAI LLM Report Generation
# -------------------------------------------------


def generate_llm_engineering_report(results: dict) -> str:
    """Generate an AI-written wastewater engineering report."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not found.")

    client = OpenAI(
        api_key=api_key,
        base_url=LLM_BASE_URL,
    )

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

    prompt = f"""
You are an experienced wastewater process engineer.

Do not invent dates, people, facilities, operators, plant names, locations, or values.
Only use the engineering metrics and detected events explicitly provided below.
If information is unavailable, state that it is unavailable.
Do not fabricate regulatory violations, permits, equipment names, or historical events.
Write in concise professional engineering language.

Use cautious engineering wording.
Prefer phrases like:
- "the data suggests"
- "is consistent with"
- "may indicate"
- "likely contributor"
- "cannot be confirmed without additional data"

Avoid overstating certainty or claiming direct causation unless explicitly proven by the supplied metrics.

Analyze the following nitrification system performance data.

Engineering Metrics:
- Average flow rate: {results['avg_flow']:.2f} m^3/hr
- Maximum flow rate: {results['max_flow']:.2f} m^3/hr
- Average dissolved oxygen: {results['avg_do']:.2f} mg/L
- Minimum dissolved oxygen: {results['min_do']:.2f} mg/L
- Average effluent ammonia: {results['avg_effluent_ammonia']:.2f} mg/L
- Maximum effluent ammonia: {results['max_effluent_ammonia']:.2f} mg/L
- Average ammonia removal efficiency: {results['avg_removal']:.2f}%
- Configured pH operating range: {MIN_PH} to {MAX_PH}
- Configured temperature operating range: {MIN_TEMP_C}°C to {MAX_TEMP_C}°C

Detected Events:
- Low dissolved oxygen events occurred from hour {low_do_start} to hour {low_do_end}
- High effluent ammonia events occurred from hour {high_ammonia_start} to hour {high_ammonia_end}
- {ph_event_summary}
- {temp_event_summary}

Write a professional wastewater engineering report using ONLY the supplied information.

Use the following sections:
1. Executive Summary
2. Process Performance Analysis
3. Root Cause Discussion
4. pH and Temperature Screening
5. Operational Concerns
6. Recommended Actions
7. Final Assessment

Do not include memo headers, fake dates, fake names, signatures, or company branding.
Do not make assumptions beyond the supplied metrics.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
