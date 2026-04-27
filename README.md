# Sales Performance Analyzer

An AI-powered data pipeline that automatically analyzes sales data and generates 
a plain-English executive report using Python, Pandas, and the Claude API.

## The Problem It Solves

Most companies have more sales data than they have time to look at. A sales 
manager running a team ends their week with a CSV export and a Tuesday morning 
meeting to prepare for. The analysis that should take an afternoon gets 
compressed into twenty minutes of gut-feel summary.

The insights are in the data. They're just not surfaced.

This pipeline does the analysis automatically — loading the data, running the 
numbers across categories, regions, and trends, then sending a structured 
summary to Claude, which returns a plain-English executive report with 
actionable recommendations. The whole thing runs in seconds.

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

sales-performance-analyzer/
├── data/               # Input dataset
├── output/             # Generated reports
├── analyzer.py         # Data fetching and Pandas analysis
├── report.py           # Claude API integration and file output
├── main.py             # Pipeline entry point
├── .env                # API key (not committed)
└── .gitignore

## Setup & Usage

1. Clone the repo
2. Create a virtual environment and activate it:
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
```
3. Install dependencies:
```bash
   python -m pip install pandas anthropic python-dotenv requests
```
4. Add your Anthropic API key to a `.env` file:

ANTHROPIC_API_KEY=your-key-here

5. Run the pipeline:
```bash
   python main.py
```

## Sample Output

The pipeline generates a structured executive report including:
- Overall revenue summary and average order value
- Top performing product categories
- Regional revenue breakdown
- Monthly trend analysis with anomaly flagging
- 3 concrete, actionable business recommendations

## Author

Peter Christopher Chester
[LinkedIn](https://www.linkedin.com/in/peter-christopher-chester-8b262353/) | 
[Portfolio](https://yourportfolio.com)
