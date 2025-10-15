# 🎯 YouTube Success Analyzer

**Turn Any YouTube Channel Into 5 Ready-to-Produce Video Ideas in Minutes**

Transform any YouTube channel URL into data-backed video concepts using AI-powered analysis. No more guessing what content will work—get proven strategies from successful channels.

## 🚀 What This Tool Does

**Single Input → Instant Video Ideas:**

1. **📊 Analyze Success Patterns** - Extract what actually works from 100+ videos
2. **🤖 Generate Video Ideas** - Get 5 ready-to-produce concepts backed by data
3. **� Get Implementation Plan** - Receive a complete roadmap with titles, hooks, and talking points
4. **� One Powerful Prompt** - No more running 5 separate analyses

Perfect for content creators who want data-driven video ideas instead of guesswork!

## 💡 Why This Approach Works

**The Old Way (Inefficient):**
- ❌ Run 5 separate analysis prompts
- ❌ Get overlapping, redundant insights  
- ❌ Spend hours synthesizing data
- ❌ Still need to manually create video ideas

**The New Way (Streamlined):**
- ✅ One Master Prompt does everything
- ✅ Directly generates 5 video ideas
- ✅ Each idea includes title, hook, talking points, and rationale
- ✅ Ready to produce within minutes

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- Mac/Linux terminal or Windows PowerShell

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/CamelCod/youtube-success-analyzer.git
   cd youtube-success-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📋 How to Use

### Step 1: Run the Analyzer
```bash
python3 youtube_success_analyzer.py
```

### Step 2: Enter Channel URL
Paste any YouTube channel URL from your niche:
- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/channel/UCxxxxxxxxx`

### Step 3: Wait for Analysis
The tool will:
- Extract metadata from all videos
- Calculate performance metrics
- Generate your Master Prompt
- Create supporting analysis reports

### Step 4: Get Your Video Ideas
All files are saved in `analysis/[channel_name]/[timestamp]/`:

```
analysis/
└── [channel_name]/
    └── [timestamp]/
        ├── MASTER_NOTEBOOKLM_PROMPT.md    # 👈 START HERE!
        ├── 00_MASTER_SUMMARY.md           # Quick overview
        ├── 01_channel_statistics.md       # Key metrics
        ├── 02_success_metrics.md          # Top performers
        ├── 03_content_themes.md           # Content analysis
        ├── 04_performance_rankings.md     # Complete rankings
        ├── detailed_video_data.csv        # Raw data
        └── video_urls_for_notebooklm.txt  # URLs for NotebookLM
```

### Step 5: Use the Master Prompt

1. Open `MASTER_NOTEBOOKLM_PROMPT.md`
2. Follow the instructions to:
   - Import video URLs into NotebookLM
   - Run the Master Prompt
   - Get your 5 video ideas
   - Use follow-up questions to refine

## 🎯 What You Get

### The Master Prompt Delivers:

**Part 1: Success Pattern Analysis**
- Content pillars & viral triggers
- Audience insights & formatting patterns
- Unique value proposition
- Monetization opportunities

**Part 2: 5 Ready-to-Produce Video Ideas**

Each idea includes:
1. ✅ **Viral-Optimized Title** - Proven title formula
2. ✅ **Compelling Hook** - First 1-2 sentences to grab attention
3. ✅ **Key Talking Points** - 5 essential points to cover
4. ✅ **Strategic Rationale** - Why this idea will work

**Part 3: Implementation Roadmap**
- Priority order for producing videos
- 30-day content calendar
- Success metrics to track
- Iteration strategy

## 📊 Supporting Reports

Beyond the Master Prompt, you also get detailed analysis reports:

- **📋 Master Summary** - Executive overview with key insights
- **📈 Success Metrics** - Top 20 performers with engagement analysis
- **🏷️ Content Themes** - Topic clusters and tag frequency analysis
- **🏆 Performance Rankings** - Complete video rankings by all metrics
- **📊 CSV Export** - Full dataset for custom analysis in Excel/Google Sheets

## 💰 Real-World Applications

### Content Creators
- **Stop Guessing**: Get 5 video ideas proven to work in your niche
- **Replicate Success**: Identify exact patterns from top performers
- **Save Time**: Skip weeks of brainstorming—get ideas in minutes
- **Data-Driven**: Every idea backed by actual performance data

### Marketing Teams
- **Competitive Intelligence**: Reverse-engineer competitor strategies
- **Campaign Planning**: Know which content formats actually work
- **Influencer Vetting**: Analyze potential partners' content strategies
- **ROI Focus**: Identify high-impact content types before investing

## 🚀 Quick Start Example

```bash
# 1. Run the analyzer
python3 youtube_success_analyzer.py

# 2. Enter a channel (example)
https://www.youtube.com/@Fireship

# 3. Wait 5-10 minutes

# 4. Open MASTER_NOTEBOOKLM_PROMPT.md

# 5. Follow instructions to get your 5 video ideas
```

---

## 📞 Support

This tool is open-source. Found a bug? Have an idea? Open an issue or submit a PR!

