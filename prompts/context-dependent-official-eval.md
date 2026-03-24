# Context-Dependent Official Evaluation Prompt

This document records the default official context-dependent evaluation prompt used to ask LLMs to output:

- a binary label: `NORMAL` or `ANOMALY`
- a short judgment rationale: `analysis_chain`
- the supporting event-level device set: `evidence_devices`

This is the default public evaluation setting for context-dependent samples.

## System Prompt

The text below is the default official context-dependent evaluation prompt with `evidence_devices` enabled.

```text
Analyze the time-series sensor events and determine whether they represent a NORMAL or ANOMALY situation.

Input:
- Description (if present): the lines under "=== Description ==="
- Context: the lines under "=== Context ==="
- Sensor Events: the time-ordered lines under "=== Sensor Events (Time-Ordered) ==="

Rules:
- The JSON object MUST contain exactly these keys: "analysis_chain", "label", "evidence_devices".
- "label" MUST be exactly "NORMAL" or "ANOMALY".
- "analysis_chain": 2 to 6 short strings. The last string MUST be the final conclusion.
- "evidence_devices": device/entity names EXACTLY as they appear in Sensor Events (the `device` field); at most 8 items.
- If label is "NORMAL", set "evidence_devices" to [].
- If label is "ANOMALY", "evidence_devices" MUST be non-empty and include the smallest set of devices necessary to justify the anomaly.
- Do NOT restate the full event list; summarize minimally.

Example outputs:
{
  "analysis_chain": ["Night time", "No unusual activity", "Conclusion: NORMAL"],
  "label": "NORMAL",
  "evidence_devices": []
}

{
  "analysis_chain": ["Temp sensor -50°C", "Impossible indoors", "Conclusion: ANOMALY"],
  "label": "ANOMALY",
  "evidence_devices": ["sensor.living_room_temperature"]
}

Return EXACTLY ONE JSON object and nothing else (no markdown, no code fences).
```

## Model-Visible Input Template

The default official input format is plain text rather than raw JSON. The model sees a prompt shaped like this:

```text
=== Description ===
<description>

=== Context ===
Date: <date>
Day: <day_of_week>
Day Type: <day_type>
Time of Day: <time_of_day>
Occupancy: <occupancy_or_occupancy_type_or_occupancy_status>
Special Event: <calendar_event>
Duration Days: <duration_days>
Duration Minutes: <duration_minutes>
Window Start: <window_start>
Window End: <window_end>
Weekend: <Yes_or_No>

=== Statistical Reference ===
metric: <metric>
historical_mean: <historical_mean>
historical_std: <historical_std>
current_value: <current_value>
z_score: <z_score>
threshold: <threshold>

=== Sensor Events (Time-Ordered) ===
<timestamp> | <device> (<room>): <status>
<timestamp> | <device>: <status>
...
```

Notes:

- `=== Description ===` is included only when a sample has a description field.
- `=== Statistical Reference ===` appears only for samples that carry statistical reference fields.
- Only fields present in a sample are rendered.

## Hidden Fields

Before formatting the prompt, ground-truth and leak-prone fields are stripped from the public sample JSON.

Fields hidden from the model include:

- `label`
- `reasoning`
- `evidence_devices`
- `anomaly_types`
- `anomaly_details`
- `pair_id`
- `gt_evidence_devices`
- `source_home`
- internal metadata keys not needed for public evaluation

For ARGUS-style samples, only a safe subset of metadata is surfaced as context.
For TDCS-style samples, shortcut-prone or unstable context keys such as some weather or season fields may be removed from model-visible input.

## Output Schema

The expected output is exactly one JSON object:

```json
{
  "analysis_chain": ["observation 1", "observation 2", "Conclusion: NORMAL or ANOMALY"],
  "label": "NORMAL or ANOMALY",
  "evidence_devices": ["device1", "device2"]
}
```

`analysis_chain` is the short judgment rationale. The final element must be the conclusion.
