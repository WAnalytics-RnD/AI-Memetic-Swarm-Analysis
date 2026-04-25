# AI-Enhanced Memetic Swarm Warfare — Research Pipeline

Computational analysis pipeline for the dissertation:
**"AI-Enhanced Memetic Swarm Warfare as a Force Multiplier in Russian Propaganda"**
POL3046, Newcastle University

## Overview

This repository contains the Python and R scripts used to conduct the empirical analysis
in the dissertation. The pipeline classifies tweets as AI-attributed or human-generated
using a three-signal composite framework, constructs a mutation network, and runs
statistical and network modelling.

## Scripts

### Python
| Script | Purpose |
| `ai_detection.py` | RoBERTa-based AI text detection (baseline, returns null results on short-form text) |
| `ai_classify.py` | Frequency-based classification signal |
| `ai_detect_v2.py` | Hello-SimpleAI/chatgpt-detector-roberta classifier |
| `ai_detect_v3.py` | Three-signal composite classifier (frequency + temporal burst + linguistic features) |
| `mutation_analysis.py` | Levenshtein distance mutation tracking |
| `network_analysis.py` | NetworkX directed network construction |
| `subnetwork_analysis.py` | AI vs human subnetwork comparison |

### R
| Script | Purpose |
| Statistical testing | Wilcoxon, Welch t-test, permutation test, effect sizes |
| ERGM modelling | Exponential Random Graph Model estimation |

## Requirements

### Python
Install required packages:
pip install pandas transformers torch networkx python-Levenshtein scikit-learn matplotlib seaborn

### R
install.packages(c("tidyverse", "ergm", "network", "rstatix", "coin"))

### Data 
The analysis uses the Ukraine War Dataset (2021-2022) available via Kaggle:
https://www.kaggle.com/datasets/fastcurious/ukraine-war-dataset

Download the dataset separately and place `file.csv` in your working directory.
Update file paths in each script before running.

## Pipeline Order

Run scripts in the following order:

1. `ai_detection.py` — baseline AI detection
2. `ai_detect_v3.py` — composite classification
3. `mutation_analysis.py` — mutation network edges
4. `network_analysis.py` — network construction
5. `subnetwork_analysis.py` — subnetwork metrics
6. R statistical testing
7. R ERGM modelling

## Methodological Notes
- AI classification uses a three-signal composite approach:
  - Frequency-based features
  - Temporal burst detection
  - Linguistic patterning
- Network construction models memetic mutation as edge formation, using edit distance thresholds.
- Statistical analysis includes both parametric and non-parametric tests, alongside permutation-based inference.

## Disclaimer
This respository is provided for research transparency and reproducibility. No claims are made regarding dataset ownership or redistribution rights.
