# Demand Side of Identity-Based Appeals in Election Campaigns

**Authors:** Young Seok Kim & Jiyoung Park & Jeong Hyun Kim

This repository contains the full code and data-processing workflow for the paper _"What Do You Want Me To Talk About? Voter Demands for Identity-Based Appeals in Election Campaigns."_ The project explores how voters respond to identity-based political messages—specifically racial and gender identity appeals—by analyzing replies to and original tweets from 2020 U.S. House candidates using large language models.

---

## Overview

This project implements an identity appeal classifier using OpenAI's GPT models (GPT-4, GPT-4o) to detect racial and gender identity appeals in electoral campaign discourse. The classifier is applied to tweet replies and original tweets from U.S. House candidates in the 2020 election.

---

## File Structure

```text
.
├── code for replies processing.R          # R code for batch processing of replies using GPT-4 API
├── code for cand tweets processing.py     # Python code for original tweet classification and cleaning
├── replies_data_processed.xlsx            # GPT-labeled reply data (voter replies)
├── original_tweets_processed.xlsx         # GPT-labeled original candidate tweets
└── README.md                              # You're reading it!
```

---
## Citation


If you use this code or data in your work, please cite:  

> Young Seok Kim, Jiyoung Park and Jeong Hyun Kim (2025). *What Do You Want Me To Talk About? Voter Demands for Identity-Based Appeals in Election Campaigns*. [Working Paper].

