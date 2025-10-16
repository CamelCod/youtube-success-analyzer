# 📊 YouTube Performance Auditor

**Analyze Your Channel's Real Performance Data & Get Actionable Optimization Recommendations**

This tool complements the YouTube Success Analyzer by auditing YOUR channel's actual performance metrics from YouTube Analytics.

## 🎯 What It Does

### Analyzes Your Data
- ✅ Overall channel performance (views, growth trends, activity)
- ✅ Video-by-video performance comparison
- ✅ Success pattern identification (titles, duration, timing)
- ✅ Engagement timing patterns (best days to post)

### Provides Recommendations
- ✅ Identifies what's working and what needs improvement
- ✅ Finds underperforming videos that need attention
- ✅ Reveals optimal video length and title patterns
- ✅ Shows best days/times for posting

### Creates Action Plan
- ✅ Prioritized 30-day optimization roadmap
- ✅ CRITICAL actions for Week 1
- ✅ HIGH priority optimizations for Weeks 2-3
- ✅ MEDIUM priority fine-tuning for Week 4

## 🚀 Quick Start

### Step 1: Get Your YouTube Analytics Data

1. Go to **YouTube Studio** → **Analytics**
2. Select the date range you want to analyze
3. Export two CSV files:
   - **Totals CSV**: Daily view totals
   - **Chart Data CSV**: Video-by-video performance data
4. Save both files to your **Downloads** folder

### Step 2: Run the Auditor

```bash
python3 run_performance_audit.py
```

The script will **automatically find** your CSV files in Downloads and run the complete audit!

## 📋 What You Get

### 1. Overall Performance Analysis
- Total views and average daily views
- Days with activity vs inactive days
- Peak performance day
- Growth trend (first half vs second half)

### 2. Video Performance Rankings
- Top 5 performing videos with metrics
- Underperforming videos that need attention
- Average daily views per video
- Duration analysis

### 3. Success Pattern Identification
- Optimal title length (based on your top performer)
- Best video duration for engagement
- Title patterns that work

### 4. Timing & Engagement Patterns
- Best days of the week for views
- When your audience is most active
- Optimal posting schedule

### 5. Strategic Recommendations
Prioritized action items with:
- **CRITICAL**: Must-do actions for immediate impact
- **HIGH**: Important optimizations for growth
- **MEDIUM**: Fine-tuning for continued improvement

### 6. 30-Day Action Plan
Week-by-week roadmap with specific actions and rationale

## 💡 Example Output

```
🎯 WEEK 1 - IMMEDIATE ACTIONS (CRITICAL PRIORITY):

   1. Create follow-up to "Context Engineering..."
      Why: This format generated 21 views

   2. Experiment with new content angles
      Why: Current strategy not driving growth

📈 WEEK 2-3 - HIGH PRIORITY OPTIMIZATIONS:

   1. Increase posting frequency to 3-4x per week
      Why: Low activity hurts algorithm visibility

   2. Schedule releases for Friday
      Why: This day drives 22 views
```

## 🔄 Best Practices

### Weekly Audits
Run this audit **every week** to:
- Track improvement over time
- Identify new patterns
- Adjust strategy based on latest data
- Measure impact of optimizations

### Combine With Success Analyzer
1. **Audit YOUR channel** → Find what needs improvement
2. **Analyze successful channels** → Learn what works in your niche
3. **Apply insights** → Implement proven strategies
4. **Measure results** → Run audit again to validate

### Data Requirements
For best results:
- **Minimum**: 2-3 weeks of data
- **Optimal**: 4-6 weeks for trend analysis
- **Update regularly**: Fresh data = accurate recommendations

## 📊 Understanding Your Results

### Growth Trends
- **Positive growth**: Keep doing what you're doing
- **Stagnant/negative**: Time to experiment with new formats
- **Low activity**: Post more frequently for algorithm boost

### Video Performance
- **Top performers**: Replicate these formats/topics
- **Underperformers**: Update thumbnails/titles or remove
- **Median performers**: Potential for optimization

### Timing Patterns
- Post on your **best performing days**
- Avoid days with consistently low engagement
- Test different times within those days

## 🛠️ Manual Usage (If Auto-Find Fails)

If the automatic CSV finder doesn't work:

```bash
python3 youtube_performance_auditor.py
```

Then enter the full paths when prompted:
```
1. Path to Totals CSV: /Users/yourname/Downloads/Untitled spreadsheet - Totals.csv
2. Path to Chart Data CSV: /Users/yourname/Downloads/Untitled spreadsheet - Chart data.csv
```

## 📈 Integration With YouTube Success Analyzer

This auditor is designed to work alongside the main YouTube Success Analyzer:

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **YouTube Success Analyzer** | Learn from successful channels | Channel URL | 3 video ideas + Master Prompt |
| **Performance Auditor** | Audit YOUR channel | Your CSV data | Optimization recommendations |

**Workflow:**
1. Export your channel's data from YouTube Analytics
2. Run Performance Auditor → Get personalized recommendations
3. Run Success Analyzer on top channels → Get proven strategies
4. Combine insights → Create optimized content
5. Re-audit weekly → Track improvement

## 🎯 Key Insights You'll Discover

- ✅ Which video topics/formats drive the most views
- ✅ Optimal video length for your audience
- ✅ Best title length and patterns
- ✅ Most effective posting schedule
- ✅ Which videos need immediate attention
- ✅ Growth patterns and trajectory
- ✅ Engagement trends over time

## 💼 Requirements

- Python 3.8+
- pandas library
- YouTube Analytics CSV exports

Install dependencies:
```bash
pip install pandas
```

## 📞 Support

Run audits weekly to see continuous improvement. Combine with the YouTube Success Analyzer for maximum impact!

---

**Pro Tip**: Use this auditor BEFORE running the Success Analyzer on other channels. Knowing your own weaknesses helps you ask better questions when analyzing competitors!
