# Pipeline

This directory contains all the necessary code and documentation for the Extract Transform Load (ETL) pipeline used to collect, clean and upload the data collected from LNMH's Plant Monitoring array.

## Files Explained
- `extract.py` - this file connects to the Heroku API to extract the relevant plant metrics produced each minute.
- `transform.py` - this file cleans the data by removing null values, setting data types and enforcing consistent rounding. 
- `test_transform.py` - this test file tests the 

## Secrets Management

