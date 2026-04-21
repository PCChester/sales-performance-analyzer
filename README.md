# Sales Performance Analyzer

An AI-powered data pipeline that automatically analyzes sales data and generates 
a plain-English executive report using Python, Pandas, and the Claude API.

## What It Does

1. Loads a sales dataset from a local CSV file
2. Analyzes key metrics using Pandas — revenue by category, region, and monthly trend
3. Sends the findings to Claude (Anthropic API) via a structured prompt
4. Receives a formatted executive report with insights and recommendations
5. Saves the report and summary to the `/output` folder

## Why It Matters

Most businesses have sales data nobody has time to properly analyze. This pipeline 
does the heavy lifting automatically — turning raw numbers into actionable insights 
in seconds. It demonstrates the core pattern behind agentic AI workflows:

**Trigger → Fetch Data → Process → Send to AI → Act on Output**

## Tech Stack

- **Python 3.14**
- **Pandas** — data loading and analysis
- **Anthropic Python SDK** — Claude API integration
- **python-dotenv** — secure API key management

## Project Structure
