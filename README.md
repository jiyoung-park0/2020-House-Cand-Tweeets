# Identity Appeal Classifier

This project uses OpenAI's GPT-4 to classify U.S. House candidate tweet replies as racial or gender identity appeals.

## Structure

- `identity_appeal_classifier.R`: Core R script using `httr` and `jsonlite` to call GPT-4.
- `replies_data_processed.xlsx`: Input dataset (cleaned replies).
- `reply_with_gpt_output_progress.csv`: Output with GPT-labeled identity appeals.

## Codebook

- `1`: Racial identity appeal
- `2`: Gender identity appeal
- `0`: Neither
