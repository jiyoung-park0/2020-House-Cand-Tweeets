# Demand Side of Identity-Based Appeals in Electoral Campaigns

**Authors:** Young Seok Kim & Jiyoung Park  

This repository contains the full code and data-processing workflow for the paper _"Demand Side of Identity-Based Appeals in Electoral Campaigns."_ The project explores how voters respond to identity-based political messages—specifically racial and gender identity appeals—by analyzing replies to tweets by U.S. House candidates using large language models.

---

## 🔍 Overview

This project implements an identity appeal classifier using OpenAI's GPT models (GPT-4, GPT-4o) to detect racial and gender identity appeals in electoral campaign discourse. The classifier is applied to tweet replies and original tweets from U.S. House candidates in the 2020 election.

---

## 📁 File Structure

```text
.
├── identity_appeal_classifier.R           # R code for batch processing of replies using GPT-4 API
├── gpt_identity_classifier.py             # Python code for original tweet classification and cleaning
├── replies_data_processed.xlsx            # Cleaned reply-level dataset
├── reply_with_gpt_output_progress.csv     # Intermediate classification results (reply-level)
├── GPT_TextClassification_origin_3.csv    # Final classification results (original tweets)
├── New_Tweets_candidate_info.csv          # Raw original tweet data (cleaned in Python)
└── README.md                              # You're reading it!
