import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def generate_report(summary: dict) -> str:
    """Send analysis summary to Claude and get an executive report back"""
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Format the summary into a readable prompt
    prompt = f"""You are a senior business analyst. Based on the following sales data summary, 
write a concise executive report with:
1. A 2-3 sentence overall performance summary
2. Top 3 insights from the data
3. 3 concrete, actionable recommendations

Here is the data:

Total Revenue: ${summary['total_revenue']:,.2f}
Total Orders: {summary['total_orders']}
Average Order Value: ${summary['average_order_value']:,.2f}

Top Products by Revenue:
{chr(10).join([f"  - {k}: ${v:,.2f}" for k, v in summary['top_products'].items()])}

Revenue by Region:
{chr(10).join([f"  - {k}: ${v:,.2f}" for k, v in summary['revenue_by_region'].items()])}

Last 6 Months Revenue Trend:
{chr(10).join([f"  - {k}: ${v:,.2f}" for k, v in summary['last_6_months'].items()])}

Write the report in a clear, professional tone suitable for a non-technical executive audience."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def save_report(report_text: str, summary: dict):
    """Save the report and summary CSV to the output folder"""
    import json
    from pathlib import Path

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Save text report
    with open(output_dir / "executive_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
        f.flush()

    # Save summary as JSON
    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("✅ Report saved to output/executive_report.txt")
    print("✅ Summary saved to output/summary.json")