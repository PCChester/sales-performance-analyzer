from analyzer import fetch_data, analyze
from report import generate_report, save_report

def main():
    print("📦 Fetching sales data...")
    df = fetch_data()
    print(f"✅ Loaded {len(df)} records\n")

    print("🔍 Analyzing data...")
    summary = analyze(df)
    print("✅ Analysis complete\n")

    print("🤖 Sending to Claude for executive report...")
    report = generate_report(summary)
    print("✅ Report generated\n")

    print("=" * 50)
    print(report)
    print("=" * 50)

    save_report(report, summary)

if __name__ == "__main__":
    main()