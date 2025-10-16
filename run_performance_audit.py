#!/usr/bin/env python3
"""
Automated YouTube Performance Auditor Runner
Automatically finds and analyzes your CSV files from Downloads folder.
"""

import os
from pathlib import Path
from youtube_performance_auditor import YouTubePerformanceAuditor


def find_csv_files():
    """Automatically find the CSV files in Downloads folder."""
    downloads = Path.home() / "Downloads"
    
    totals_file = None
    chart_file = None
    
    # Look for the CSV files
    for file in downloads.glob("*.csv"):
        filename = file.name.lower()
        if "totals" in filename:
            totals_file = str(file)
        elif "chart" in filename:
            chart_file = str(file)
    
    return totals_file, chart_file


def main():
    """Main execution function."""
    print("\n🔍 Searching for your YouTube Analytics CSV files...\n")
    
    totals_path, chart_path = find_csv_files()
    
    if totals_path:
        print(f"✅ Found Totals CSV: {os.path.basename(totals_path)}")
    else:
        print("⚠️  Totals CSV not found in Downloads folder")
    
    if chart_path:
        print(f"✅ Found Chart Data CSV: {os.path.basename(chart_path)}")
    else:
        print("⚠️  Chart Data CSV not found in Downloads folder")
    
    if not totals_path and not chart_path:
        print("\n❌ No CSV files found. Please download them from YouTube Analytics first.")
        print("\n📥 How to get your data:")
        print("   1. Go to YouTube Studio > Analytics")
        print("   2. Export your data as CSV")
        print("   3. Save to your Downloads folder")
        print("   4. Run this script again")
        return
    
    print()
    
    # Create auditor and run analysis
    auditor = YouTubePerformanceAuditor(totals_path, chart_path)
    auditor.run_audit()


if __name__ == "__main__":
    main()
