# SmartBench Prompt Drafts

These prompt drafts are written to strictly match the JSON schemas that are currently public in this repository.

They are designed for no-leak evaluation on the released benchmark files.

## Public Benchmark Schemas

### Context-Independent samples

Every public context-independent sample contains these top-level fields:

- `scenario`
- `device_states`
- `environment_context`
- `reasoning`
- `label`
- `evidence_devices`
- `anomaly_info`
- `pair_id`
- `id`

For model input, the released context-independent prompt uses:

- `environment_context`
- `device_states`

The public field `scenario` is also available in the released files, but the current prompt text omits it to stay closer to the original evaluation prompt structure.

The released `environment_context` object currently contains these keys for all public context-independent samples:

- `time`
- `time_of_day`
- `day_of_week`
- `is_weekend`
- `season`
- `weather`
- `outdoor_temperature`
- `natural_light_level`
- `occupants_at_home`

### Context-Dependent samples

Every public context-dependent sample in `argus_prime/` and `tdcs_rbe/` contains these top-level fields:

- `description`
- `context`
- `events`
- `reasoning`
- `label`
- `evidence_devices`
- `anomaly_types`
- `anomaly_details`
- `metadata`
- `pair_id`
- `paired_id`
- `id`

For model input, only the following fields should be visible:

- `description`
- `context`
- `events`

The released `context` object currently contains these keys for all public `argus_prime/` and `tdcs_rbe/` samples:

- `occupancy_type`
- `duration_days`

The released `events` objects always contain:

- `timestamp`
- `device`
- `status`

Some files also include optional event-level fields such as `room` or `location`.

## Recommended Sanitization Before Inference

Because the released benchmark files contain ground-truth annotations, remove annotation-only fields before sending a sample to an LLM.

### Context-Independent

Remove:

- `reasoning`
- `label`
- `evidence_devices`
- `anomaly_info`
- `pair_id`
- `id`

### Context-Dependent

Remove:

- `reasoning`
- `label`
- `evidence_devices`
- `anomaly_types`
- `anomaly_details`
- `metadata`
- `pair_id`
- `paired_id`
- `id`

## Prompt Files

- `context-independent_prompt.txt`
- `context-dependent_prompt.txt`

These prompts use output fields that match the public benchmark naming:

- `label`
- `reasoning`
- `evidence_devices`
