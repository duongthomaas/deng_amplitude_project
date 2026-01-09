# Amplitude Data Extraction & Processing

This project contains a pipeline of Python scripts designed to extract raw event data from the Amplitude API and process the compressed archives into clean, usable JSON files ready for cloud storage (AWS S3).

## Scripts Overview

### 1. Data Extractor (`extract_amplitude.py`)

Connects to the Amplitude Export API to download event data for a specific date range.

- **Input:** Amplitude API Key and Secret.
- **Output:** A raw compressed archive named `data.zip`.

### 2. Data Unzipper (`unzip_amplitude.py`)

Handles the "Russian Doll" compression structure of Amplitude exports (a `.zip` file containing nested folders of `.gz` files).

- **Input:** The `data.zip` file.
- **Process:**
  1.  Extracts `data.zip` to a temporary workspace.
  2.  Goes through the extracted folders to find all `.gz` files.
  3.  Decompresses each `.gz` file into a clean `.json` file.
  4.  Consolidates all `.json` files into a single `data/` directory.
  5.  Cleans up temporary files.
- **Output:** A `data/` folder containing raw JSON event logs.

## Prerequisites

- Python 3.x
- No external libraries required for the unzip script (uses standard library `zipfile`, `gzip`, `shutil`, `os`).
- `requests` library required for the extractor script.
