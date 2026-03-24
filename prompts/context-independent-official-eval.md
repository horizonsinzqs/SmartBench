# Context-Independent Official Evaluation Prompt

This document records the official context-independent evaluation prompt used to ask LLMs to output:

- a binary label: `NORMAL` or `ANOMALY`
- a short judgment rationale: `analysis_chain`
- the supporting device set: `evidence_devices`

## System Prompt

This is the official system prompt used in the mainline context-independent evaluation setting. The text below is copied from the official evaluation artifact used for the public release pipeline.

```text
Analyze the device states and determine whether they represent a NORMAL or ANOMALY situation.

Input:
- Environment Context: the lines above "Device States:"
- Device States: the key-value lines under "Device States:"

Rules:
- The JSON object MUST contain exactly these keys: "analysis_chain", "label", "evidence_devices"
- "label" MUST be exactly "NORMAL" or "ANOMALY".
- "analysis_chain": 2 to 6 short strings. The last string MUST be the final conclusion.
- "evidence_devices": device names EXACTLY as they appear under "Device States:".
- If label is "NORMAL", set "evidence_devices" to [].
- If label is "ANOMALY", "evidence_devices" MUST be non-empty and include the smallest set of devices necessary to justify the anomaly.

Example outputs:
{
  "analysis_chain": ["Night time, 1 occupant at home", "All lights off, no motion detected", "Doors locked, temperature 22°C", "Consistent sleeping state"],
  "label": "NORMAL",
  "evidence_devices": []
}

{
  "analysis_chain": ["Temperature sensor reading -50°C", "Value physically impossible for indoor environment", "Sensor malfunction detected"],
  "label": "ANOMALY",
  "evidence_devices": ["Living Room Temperature"]
}

Return EXACTLY ONE JSON object and nothing else (no markdown, no code fences).
```

## Model-Visible Input Template

The model is given a text prompt in the following shape:

```text
Time: <time>
Period: <time_of_day>
Day of Week: <day_of_week>
Is Weekend: <true_or_false>
Season: <season>
Weather: <weather>
Outdoor Temperature: <outdoor_temperature>°C
Natural Light Level: <natural_light_level>
Occupants at Home: <occupants_at_home>

Device States:
  <device_1>: <value_1>
  <device_2>: <value_2>
  ...
```

In the released context-independent benchmark, the model-visible input is built only from:

- `environment_context`
- `device_states`

## Hidden Fields

Although each public sample file contains ground-truth annotations, they are not shown to the model during evaluation.

Fields hidden from the model include:

- `label`
- `reasoning`
- `evidence_devices`
- `anomaly_info`
- `pair_id`
- `id`

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
