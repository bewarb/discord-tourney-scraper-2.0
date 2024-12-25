#!/bin/bash

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Run Python script
python scraper.py
