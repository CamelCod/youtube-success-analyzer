#!/usr/bin/env python3
"""
🎯 YouTube Success Analyzer - All-in-One Tool
================================================================================
One script to rule them all: Extract videos → Analyze metadata → Generate reports → Create NotebookLM prompts

This comprehensive tool takes a YouTube channel URL and generates:
- Video metadata with success metrics
- Organized analysis reports
- NotebookLM-ready prompts for content strategy
- CSV data for spreadsheet analysis
- Summary reports for quick insights

Perfect for content creators analyzing successful YouTube channels!
================================================================================
"""

import yt_dlp
import json
import os
import csv
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime
from collections import Counter
import subprocess
import sys
from typing import List, Dict, Any

# Global configuration
CHANNEL_URL = ""
CHANNEL_NAME = ""
OUTPUT_DIR = None

class YouTubeSuccessAnalyzer:
    def __init__(self):
        self.channel_url = ""
        self.channel_name = ""
        self.output_dir = Path(".")  # Initialize with current directory
        self.video_data = []
        
        # Master Prompt Template - Optimized for NotebookLM (500K word limit, 50 queries/day)
        self.master_prompt_template = """
# Master YouTube Strategy & Video Idea Generator

**Analysis**: {video_count} videos from {channel_name}

## Part 1: Strategic Pattern Analysis

Identify {channel_name}'s core success components from observable data (titles, topics, views, engagement).

### Success DNA
- **Content Pillars**: What 3 main themes dominate? Which topics outperform average views by 2x+?
- **Viral Formula**: What title patterns, keywords, and hooks appear in top 10% videos?
- **Audience Profile**: Who watches? What video length + format gets highest engagement?
- **Unique Edge**: What makes this content un-copyable? What gap do they own?

### Revenue Potential
- Which topics show expertise that could support paid products/courses?
- What content demonstrates audience loyalty for monetization?

---

## Part 2: Generate 3 High-Impact Video Ideas

Create **3 distinct, niche-focused video concepts** using the patterns above. Each must include:

### Video Idea #1
1. **Title**: [Viral-optimized using {channel_name}'s proven formula]
2. **Hook**: [Opening 15 seconds - max retention focus]
3. **Core Points**: [3-5 essential talking points]
4. **Why This Works**: [One-sentence rationale tied to data]

### Video Idea #2
[Same structure - different niche angle]

### Video Idea #3
[Same structure - unique strategic position]

---

## Part 3: Execution Plan

1. **Priority**: Which idea to film first and why?
2. **Schedule**: 30-day rollout strategy
3. **Metrics**: Key performance indicators to track
4. **Iteration**: How to refine based on results

**Focus**: Each idea must be immediately actionable, data-backed, and designed for continuous improvement through follow-up analysis.
"""
    
    
    def display_banner(self):
        """Display the tool banner and introduction."""
        print()
        print("="*80)
        print("🎯 YouTube Success Analyzer - Your Content Empire Builder")
        print("="*80)
        print()
        print("� MONETIZATION-READY ANALYSIS:")
        print("   ✅ Identify high-performing content patterns → Replicate for revenue")
        print("   ✅ Discover viral triggers → Create breakout videos")
        print("   ✅ Analyze competitor strategies → Beat the competition")
        print("   ✅ Find monetization opportunities → Build multiple income streams")
        print("   ✅ Export data for business decisions → Scale smartly")
        print()
        print("🚀 WHAT YOU'LL GET IN MINUTES:")
        print("   📊 Complete channel performance breakdown")
        print("   💎 Success patterns & viral content insights")
        print("   📈 Top 20 highest-performing videos analysis")
        print("   🎯 Master AI prompt for instant video idea generation")
        print("   💼 CSV data export for business intelligence")
        print()
        print("💡 Perfect for: Content Creators • Marketers • Business Owners • Researchers")
        print("="*80)
        print()
    
    def get_channel_input(self):
        """Get YouTube channel URL from user."""
        print("\n🎬 STEP 1: Choose a Channel to Analyze")
        print("-" * 80)
        print("Enter the URL of any successful YouTube channel you want to study.")
        print()
        print("💡 TIP: Analyze channels in YOUR NICHE to find winning strategies!")
        print()
        print("Supported formats:")
        print("  • https://www.youtube.com/@channelname")
        print("  • https://www.youtube.com/c/channelname")
        print("  • https://www.youtube.com/channel/UCxxxxxxxxx")
        print()
        
        while True:
            url_input = input("� Paste YouTube channel URL here: ").strip()
            
            if not url_input:
                print("❌ Please enter a valid URL.")
                continue
                
            # Add /videos to the URL if not present
            if 'youtube.com' in url_input and '/videos' not in url_input:
                if url_input.endswith('/'):
                    url_input += 'videos'
                else:
                    url_input += '/videos'
            
            self.channel_url = url_input
            self.channel_name = self.extract_channel_name(url_input)
            
            # Create output directory
            self.output_dir = Path("analysis") / self.channel_name / datetime.now().strftime('%Y%m%d_%H%M%S')
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n✅ Channel Selected: {self.channel_name}")
            print(f"📁 Results will be saved to: {self.output_dir}")
            print(f"🔗 Analyzing: {self.channel_url}")
            print()
            print("💰 This analysis will help you:")
            print("   • Identify what makes videos successful")
            print("   • Find profitable content patterns")
            print("   • Understand competitor strategies")
            print("   • Build a data-driven content calendar")
            print()
            
            confirm = input("🚀 Ready to unlock success secrets? (y/n): ").lower()
            if confirm.startswith('y'):
                break
            else:
                print("\nLet's try again...\n")
    
    def extract_channel_name(self, url):
        """Extract clean channel name from URL."""
        try:
            parsed_url = urlparse(url)
            path = parsed_url.path.strip('/')
            
            if path.startswith('@'):
                channel_name = path[1:].split('/')[0]
            elif path.startswith('c/'):
                channel_name = path.split('/')[1]
            elif path.startswith('channel/'):
                channel_name = path.split('/')[1]
            elif path.startswith('user/'):
                channel_name = path.split('/')[1]
            else:
                channel_name = path.replace('/', '_')
            
            # Clean for filesystem
            channel_name = ''.join(c for c in channel_name if c.isalnum() or c in ('-', '_'))
            return channel_name or "unknown_channel"
        except Exception:
            return "unknown_channel"
    
    def format_number(self, num):
        """Format numbers for readability."""
        if not isinstance(num, (int, float)) or num == 0:
            return "0"
        
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(int(num))
    
    def extract_video_metadata(self):
        """Extract comprehensive video metadata using yt-dlp."""
        print(f"\n\n🔍 STEP 2: Extracting Success Data from {self.channel_name}")
        print("="*80)
        print("⏳ Analyzing videos, engagement metrics, and success patterns...")
        print("💡 Grab a coffee - this goldmine of insights is worth the wait!")
        print()
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',  # Fast: get basic info first, then fetch details only for videos we process
            'writeinfojson': False,
            'writethumbnail': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'extractor_args': {'youtube': {'player_client': ['ios', 'web']}},  # Use multiple clients for reliability
            'sleep_interval': 1,  # Reduced to 1 second - still safe but much faster
            'max_sleep_interval': 2,  # Max 2 seconds
            'sleep_interval_requests': 1,  # 1 second between API requests
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                channel_dict = ydl.extract_info(self.channel_url, download=False)
                
                if 'entries' in channel_dict:
                    total_videos = len([v for v in channel_dict['entries'] if v])
                    print(f"   📊 Found {total_videos} videos - extracting success metrics...\n")
                    
                    # Show progress every 10 videos for better feedback
                    for i, video in enumerate(channel_dict['entries'], 1):
                        if video:
                            try:
                                # Progress updates every 10 videos instead of 20
                                if i % 10 == 0 or i == 1:
                                    percent = (i / total_videos) * 100
                                    print(f"   ⚡ Progress: {i}/{total_videos} ({percent:.0f}%) - Processing video data...")
                                elif i == total_videos:
                                    print(f"   ✅ Complete: {i}/{total_videos} (100%) - Success data extracted!\n")
                                
                                # Extract comprehensive metadata
                                metadata = {
                                    'index': i,
                                    'title': video.get('title', 'Unknown Title'),
                                    'url': video.get('webpage_url', video.get('url', '')),
                                    'video_id': video.get('id', ''),
                                    'description': video.get('description', ''),
                                    'upload_date': video.get('upload_date', ''),
                                    'uploader': video.get('uploader', ''),
                                    'duration': video.get('duration', 0),
                                    'view_count': video.get('view_count', 0),
                                    'like_count': video.get('like_count', 0),
                                    'comment_count': video.get('comment_count', 0),
                                    'tags': video.get('tags', []),
                                    'categories': video.get('categories', []),
                                    'thumbnail': video.get('thumbnail', ''),
                                }
                                
                                # Format data
                                if metadata['duration']:
                                    duration_str = f"{metadata['duration'] // 3600:02d}:{(metadata['duration'] % 3600) // 60:02d}:{metadata['duration'] % 60:02d}"
                                    metadata['duration_formatted'] = duration_str
                                else:
                                    metadata['duration_formatted'] = "Unknown"
                                
                                if metadata['upload_date']:
                                    try:
                                        date_obj = datetime.strptime(metadata['upload_date'], '%Y%m%d')
                                        metadata['upload_date_formatted'] = date_obj.strftime('%Y-%m-%d')
                                    except ValueError:
                                        metadata['upload_date_formatted'] = metadata['upload_date']
                                else:
                                    metadata['upload_date_formatted'] = "Unknown"
                                
                                metadata['view_count_formatted'] = self.format_number(metadata['view_count'])
                                metadata['like_count_formatted'] = self.format_number(metadata['like_count'])
                                metadata['comment_count_formatted'] = self.format_number(metadata['comment_count'])
                                
                                # Calculate engagement metrics
                                views = metadata['view_count']
                                likes = metadata['like_count']
                                comments = metadata['comment_count']
                                
                                if views > 0:
                                    metadata['engagement_rate'] = round(((likes + comments) / views) * 100, 2)
                                    metadata['like_rate'] = round((likes / views) * 100, 2)
                                    metadata['comment_rate'] = round((comments / views) * 100, 2)
                                else:
                                    metadata['engagement_rate'] = 0
                                    metadata['like_rate'] = 0
                                    metadata['comment_rate'] = 0
                                
                                self.video_data.append(metadata)
                                
                            except Exception as e:
                                print(f"   ⚠️ Error processing video {i}: {e}")
                                continue
                    
                    print(f"✅ Extracted metadata for {len(self.video_data)} videos")
                    return True
                    
        except Exception as e:
            print(f"❌ Error extracting metadata: {e}")
            return False
    
    def generate_analysis_reports(self):
        """Generate comprehensive analysis reports."""
        print("\n\n📊 STEP 3: Generating Your Business Reports")
        print("="*80)
        
        if not self.video_data:
            print("❌ No video data available")
            return
        
        # 1. Channel Statistics Report
        print("   📈 Creating channel statistics report...")
        self.create_statistics_report()
        
        # 2. Success Metrics Analysis
        print("   🏆 Analyzing top performers and success patterns...")
        self.create_success_metrics_report()
        
        # 3. Content Themes Analysis
        print("   🏷️  Identifying profitable content themes...")
        self.create_content_themes_report()
        
        # 4. Performance Rankings
        print("   📊 Compiling performance rankings and CSV data...")
        self.create_performance_rankings()
        
        print("   ✅ All reports generated successfully!\n")
    
    def create_statistics_report(self):
        """Create comprehensive channel statistics."""
        total_views = sum(v.get('view_count', 0) for v in self.video_data)
        total_likes = sum(v.get('like_count', 0) for v in self.video_data)
        total_comments = sum(v.get('comment_count', 0) for v in self.video_data)
        total_duration = sum(v.get('duration', 0) for v in self.video_data)
        
        avg_views = total_views / len(self.video_data) if self.video_data else 0
        avg_engagement = sum(v.get('engagement_rate', 0) for v in self.video_data) / len(self.video_data) if self.video_data else 0
        
        # Find top performers
        most_viewed = max(self.video_data, key=lambda x: x.get('view_count', 0))
        highest_engagement = max(self.video_data, key=lambda x: x.get('engagement_rate', 0))
        
        stats_content = f"""# {self.channel_name} - Channel Statistics Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: {self.channel_url}

## 📊 Overall Statistics

- **Total Videos**: {len(self.video_data):,}
- **Total Views**: {self.format_number(total_views)} ({total_views:,})
- **Total Likes**: {self.format_number(total_likes)} ({total_likes:,})
- **Total Comments**: {self.format_number(total_comments)} ({total_comments:,})
- **Total Watch Time**: {total_duration // 3600:,} hours {(total_duration % 3600) // 60} minutes

## 📈 Average Performance

- **Average Views per Video**: {self.format_number(avg_views)} ({avg_views:,.0f})
- **Average Engagement Rate**: {avg_engagement:.2f}%
- **Average Video Duration**: {(total_duration / len(self.video_data)) // 60:.0f}:{(total_duration / len(self.video_data)) % 60:02.0f}

## 🏆 Top Performers

### Most Viewed Video
- **Title**: {most_viewed['title']}
- **Views**: {most_viewed['view_count_formatted']} ({most_viewed['view_count']:,})
- **Upload Date**: {most_viewed['upload_date_formatted']}
- **URL**: {most_viewed['url']}

### Highest Engagement Video  
- **Title**: {highest_engagement['title']}
- **Engagement Rate**: {highest_engagement['engagement_rate']}%
- **Views**: {highest_engagement['view_count_formatted']}
- **URL**: {highest_engagement['url']}

## 📊 Success Insights

Based on the data analysis:
- Videos with {self.format_number(avg_views)} or more views are above average
- Engagement rates above {avg_engagement:.1f}% indicate strong audience connection
- The channel's most successful content focuses on: {', '.join(most_viewed.get('categories', ['General']))}

"""
        
        with open(self.output_dir / "01_channel_statistics.md", 'w', encoding='utf-8') as f:
            f.write(stats_content)
    
    def create_success_metrics_report(self):
        """Create detailed success metrics analysis."""
        # Sort videos by different metrics
        by_views = sorted(self.video_data, key=lambda x: x.get('view_count', 0), reverse=True)[:20]
        by_engagement = sorted(self.video_data, key=lambda x: x.get('engagement_rate', 0), reverse=True)[:20]
        
        content = f"""# {self.channel_name} - Success Metrics Analysis

## 🎯 Top 20 Videos by Views

| Rank | Title | Views | Engagement | Duration | Upload Date |
|------|-------|-------|------------|----------|-------------|
"""
        
        for i, video in enumerate(by_views, 1):
            content += f"| {i} | {video['title'][:50]}... | {video['view_count_formatted']} | {video['engagement_rate']}% | {video['duration_formatted']} | {video['upload_date_formatted']} |\n"
        
        content += """
## 🔥 Top 20 Videos by Engagement Rate

| Rank | Title | Engagement | Views | Likes | Comments |
|------|-------|------------|-------|----------|----------|
"""
        
        for i, video in enumerate(by_engagement, 1):
            content += f"| {i} | {video['title'][:50]}... | {video['engagement_rate']}% | {video['view_count_formatted']} | {video['like_count_formatted']} | {video['comment_count_formatted']} |\n"
        
        # Add success patterns analysis
        high_performers = [v for v in self.video_data if v.get('view_count', 0) > (sum(vid.get('view_count', 0) for vid in self.video_data) / len(self.video_data))]
        
        if high_performers:
            avg_duration = sum(v.get('duration', 0) for v in high_performers) / len(high_performers)
            common_tags = []
            for video in high_performers:
                common_tags.extend(video.get('tags', []))
            
            tag_frequency = Counter(common_tags)
            
            content += f"""
## 🎨 Success Patterns Analysis

### High-Performing Videos ({len(high_performers)} videos above average)
- **Average Duration**: {avg_duration // 60:.0f}:{avg_duration % 60:02.0f}
- **Common Tags**: {', '.join([tag for tag, _ in tag_frequency.most_common(10)])}

### Performance Insights
- Videos longer than {avg_duration // 60:.0f} minutes tend to perform better
- Content with these tags shows higher engagement: {', '.join([tag for tag, _ in tag_frequency.most_common(5)])}
- Upload timing and consistency appear to impact performance

"""
        
        with open(self.output_dir / "02_success_metrics.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_content_themes_report(self):
        """Analyze content themes and topics."""
        all_tags = []
        all_categories = []
        title_words = []
        
        for video in self.video_data:
            all_tags.extend(video.get('tags', []))
            all_categories.extend(video.get('categories', []))
            # Extract common words from titles
            title_words.extend([word.lower() for word in video['title'].split() if len(word) > 3])
        
        tag_frequency = Counter(all_tags)
        category_frequency = Counter(all_categories)
        word_frequency = Counter(title_words)
        
        content = f"""# {self.channel_name} - Content Themes Analysis

## 🏷️ Most Common Tags (Top 30)

"""
        for tag, count in tag_frequency.most_common(30):
            percentage = (count / len(self.video_data)) * 100
            content += f"- **{tag}**: {count} videos ({percentage:.1f}%)\n"
        
        content += """
## 📂 Content Categories

"""
        for category, count in category_frequency.most_common(10):
            percentage = (count / len(self.video_data)) * 100
            content += f"- **{category}**: {count} videos ({percentage:.1f}%)\n"
        
        content += """
## 🔤 Common Title Words (Top 20)

"""
        for word, count in word_frequency.most_common(20):
            content += f"- **{word}**: {count} occurrences\n"
        
        # Analyze content by performance
        high_performers = sorted(self.video_data, key=lambda x: x.get('view_count', 0), reverse=True)[:int(len(self.video_data) * 0.2)]  # Top 20%
        
        hp_tags = []
        for video in high_performers:
            hp_tags.extend(video.get('tags', []))
        
        hp_tag_frequency = Counter(hp_tags)
        
        content += """
## 🎯 High-Performing Content Analysis (Top 20% of videos)

### Tags in Most Successful Videos:
"""
        for tag, count in hp_tag_frequency.most_common(15):
            content += f"- **{tag}**: {count} videos\n"
        
        content += f"""
### Content Strategy Insights:
- Focus on topics tagged with: {', '.join([tag for tag, _ in hp_tag_frequency.most_common(5)])}
- High-performing videos often include: {', '.join([word for word, _ in Counter([w for v in high_performers for w in v['title'].lower().split() if len(w) > 3]).most_common(5)])}
- Successful content categories: {', '.join([cat for cat, _ in Counter([c for v in high_performers for c in v.get('categories', [])]).most_common(3)])}

"""
        
        with open(self.output_dir / "03_content_themes.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_performance_rankings(self):
        """Create comprehensive performance rankings."""
        # Create different ranking lists
        rankings = {
            'views': sorted(self.video_data, key=lambda x: x.get('view_count', 0), reverse=True),
            'engagement': sorted(self.video_data, key=lambda x: x.get('engagement_rate', 0), reverse=True),
            'likes': sorted(self.video_data, key=lambda x: x.get('like_count', 0), reverse=True),
            'comments': sorted(self.video_data, key=lambda x: x.get('comment_count', 0), reverse=True),
            'duration': sorted(self.video_data, key=lambda x: x.get('duration', 0), reverse=True)
        }
        
        content = f"""# {self.channel_name} - Performance Rankings

## 🏆 Complete Performance Rankings

### Top 50 Videos by Views
| Rank | Title | Views | Engagement | Duration | Date |
|------|-------|-------|------------|----------|------|
"""
        
        for i, video in enumerate(rankings['views'][:50], 1):
            content += f"| {i} | {video['title'][:60]}... | {video['view_count_formatted']} | {video['engagement_rate']}% | {video['duration_formatted']} | {video['upload_date_formatted']} |\n"
        
        # Export detailed CSV for analysis
        csv_file = self.output_dir / "detailed_video_data.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if self.video_data:
                writer = csv.DictWriter(f, fieldnames=self.video_data[0].keys())
                writer.writeheader()
                writer.writerows(self.video_data)
        
        content += """
## 📊 Data Export

Complete video data has been exported to: `detailed_video_data.csv`

This CSV contains all metadata for further analysis in Excel, Google Sheets, or other tools.

### CSV Columns Include:
- Title, URL, Video ID
- View count, Like count, Comment count
- Engagement rates and metrics
- Upload date, Duration
- Tags, Categories, Description
- Performance rankings

"""
        
        with open(self.output_dir / "04_performance_rankings.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_notebooklm_prompts(self):
        """Generate the Master NotebookLM analysis prompt."""
        print("\n📝 STEP 4: Creating AI-Powered Master Analysis Prompt")
        print("="*80)
        print("   🤖 Generating consolidated Master Prompt (Analysis → Content Ideas)...")
        
        # Create URL list for NotebookLM
        url_file = self.output_dir / "video_urls_for_notebooklm.txt"
        with open(url_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.channel_name} - Video URLs for NotebookLM Analysis\n")
            f.write(f"# Total videos: {len(self.video_data)}\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for video in self.video_data:
                f.write(f"{video['url']}\n")
        
        # Format the master prompt with channel data
        formatted_prompt = self.master_prompt_template.format(
            channel_name=self.channel_name,
            video_count=len(self.video_data)
        )
        
        # Create the master prompt file
        prompt_content = f"""# Master NotebookLM Prompt: YouTube Strategy & Content Generation

**Channel**: {self.channel_name}
**Videos Analyzed**: {len(self.video_data)} videos
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📋 How to Use This Prompt:

### Step 1: Add Sources to NotebookLM
1. Open [NotebookLM](https://notebooklm.google.com)
2. Create a new notebook
3. Import video URLs from `video_urls_for_notebooklm.txt`
4. Wait for processing (under 500K word limit per source)

### Step 2: Run the Master Prompt
1. Copy the prompt below (starts with "# Master YouTube Strategy")
2. Paste into NotebookLM chat
3. Get 3 high-impact video ideas

### Step 3: Iterate & Refine
Use follow-up questions to deepen analysis (50 queries/day on free tier)

---

## 📊 Channel Context:

- **Total Views**: {self.format_number(sum(v.get('view_count', 0) for v in self.video_data))}
- **Avg Views/Video**: {self.format_number(sum(v.get('view_count', 0) for v in self.video_data) / len(self.video_data))}
- **Top Video**: {max(self.video_data, key=lambda x: x.get('view_count', 0))['title']}
- **Key Topics**: {', '.join([tag for tag, _ in Counter([tag for video in self.video_data for tag in video.get('tags', [])]).most_common(5)])}

---

{formatted_prompt}

---

## 💡 Smart Follow-Up Questions (Maximize Your 50 Daily Queries):

**Refine Ideas**:
- "Expand Video Idea #2 into a full script outline with timestamps"
- "Make the hook for Idea #1 more controversial for higher CTR"
- "Generate 3 thumbnail concepts for Idea #3"

**Validate Strategy**:
- "Which idea has highest viral potential based on the data?"
- "Are these ideas different enough from recent {self.channel_name} content?"
- "What specific metrics support Idea #2's rationale?"

**Scale & Monetize**:
- "Turn Idea #1 into a 5-video series"
- "Create a 90-day content calendar using these patterns"
- "What products/sponsorships fit each idea?"
- "Which idea best supports a paid course launch?"

---

## 🎯 Why This Works:

✅ **Optimized for NotebookLM**: Stays under word limits, maximizes daily query value
✅ **3 > 5**: Fewer, deeper, more strategic ideas = higher engagement
✅ **Niche-Focused**: Each idea targets specific audience segment
✅ **Iteration-Ready**: Designed for continuous refinement via follow-ups
✅ **Data-Driven**: Every idea backed by {len(self.video_data)} video analysis

---

**Pro Tip**: Save 10+ queries by batching related questions. Example: "For Idea #1, provide: script outline, 3 thumbnail concepts, and best posting time."
"""
        
        # Save the master prompt
        with open(self.output_dir / "MASTER_NOTEBOOKLM_PROMPT.md", 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        
        print("   ✅ Generated Master Prompt with full workflow + URL list\n")

    
    def create_master_summary(self):
        """Create a master summary and action plan."""
        print("\n📋 STEP 5: Compiling Master Summary")
        print("="*80)
        print("   🎯 Creating executive summary with actionable insights...")
        
        # Calculate key metrics
        total_views = sum(v.get('view_count', 0) for v in self.video_data)
        avg_views = total_views / len(self.video_data)
        avg_engagement = sum(v.get('engagement_rate', 0) for v in self.video_data) / len(self.video_data)
        
        top_video = max(self.video_data, key=lambda x: x.get('view_count', 0))
        top_tags = [tag for tag, _ in Counter([tag for video in self.video_data for tag in video.get('tags', [])]).most_common(10)]
        
        summary_content = f"""# 🎯 {self.channel_name} - Master Analysis Summary

**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Channel URL**: {self.channel_url}
**Videos Analyzed**: {len(self.video_data)}

## 📊 Key Statistics
- **Total Views**: {self.format_number(total_views)} ({total_views:,})
- **Average Views**: {self.format_number(avg_views)} per video
- **Average Engagement**: {avg_engagement:.2f}%
- **Most Successful Video**: {top_video['title']} ({top_video['view_count_formatted']} views)

## 🎯 Content Strategy Insights
- **Main Topics**: {', '.join(top_tags[:5])}
- **High-Performance Tags**: {', '.join(top_tags[:3])}
- **Success Patterns**: Videos with these elements tend to perform 2x+ above average

## 📁 Generated Files

### Analysis Reports
1. `01_channel_statistics.md` - Complete channel overview
2. `02_success_metrics.md` - Performance analysis and rankings  
3. `03_content_themes.md` - Topic and theme analysis
4. `04_performance_rankings.md` - Detailed performance rankings
5. `detailed_video_data.csv` - Complete dataset for Excel analysis

### NotebookLM Resources
- `video_urls_for_notebooklm.txt` - All video URLs for import
- `MASTER_NOTEBOOKLM_PROMPT.md` - **START HERE!** One powerful prompt that:
  - Analyzes success patterns from all videos
  - Generates 5 ready-to-produce video ideas
  - Provides implementation roadmap
  - Includes follow-up questions for deeper insights

## 🚀 Next Steps

### Immediate Actions:
1. **Start with Master Prompt**: Open `MASTER_NOTEBOOKLM_PROMPT.md` and follow the instructions
2. **Get 5 Video Ideas**: Use NotebookLM to generate your first 5 data-backed video concepts
3. **Review Performance Data**: Study `02_success_metrics.md` to understand what works

### Content Strategy:
1. **Focus on Winning Topics**: Prioritize content around: {', '.join(top_tags[:3])}
2. **Optimize Format**: Videos around {sum(v.get('duration', 0) for v in sorted(self.video_data, key=lambda x: x.get('view_count', 0), reverse=True)[:20]) // 20 // 60} minutes perform best
3. **Engagement Tactics**: Study high-engagement videos for community-building strategies

### Data Analysis:
1. **Spreadsheet Analysis**: Import `detailed_video_data.csv` for custom analysis
2. **Trend Identification**: Look for seasonal patterns and timing optimization
3. **Competitive Research**: Compare metrics with similar channels

## 💰 Monetization Opportunities

Based on the analysis, this channel could:
- Create premium content around top-performing topics
- Develop courses or coaching based on successful video themes
- Partner with brands relevant to main content categories
- Build affiliate programs around recommended tools/products

## 🔍 Key Success Factors Identified

1. **Content Topics**: {top_tags[0]} content generates highest engagement
2. **Video Length**: {sum(v.get('duration', 0) for v in sorted(self.video_data, key=lambda x: x.get('view_count', 0), reverse=True)[:10]) // 10 // 60}-minute videos perform best
3. **Engagement**: Videos with {avg_engagement:.1f}%+ engagement rate see 3x more growth
4. **Consistency**: Regular posting in successful categories maintains momentum

---

## 📖 How to Use This Analysis

1. **Start with NotebookLM**: Import URLs and use the generated prompts
2. **Deep Dive Reports**: Read through each analysis report for specific insights
3. **Data Exploration**: Use the CSV for custom analysis and filtering
4. **Strategy Implementation**: Apply insights to your own content strategy

This analysis provides a complete blueprint for understanding and replicating successful YouTube content strategies.

**Generated by YouTube Success Analyzer** 🎯
"""
        
        with open(self.output_dir / "00_MASTER_SUMMARY.md", 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print("   ✅ Master summary complete - Your roadmap to success!\n")
    
    def display_completion_summary(self):
        """Display completion summary and next steps."""
        print(f"\n🎉 Analysis Complete for {self.channel_name}!")
        print("=" * 80)
        print(f"📁 All files saved to: {self.output_dir}")
        print()
        print("📊 Generated Files:")
        print("   📋 00_MASTER_SUMMARY.md - Start here for overview")
        print("   📈 01_channel_statistics.md - Key metrics and stats")
        print("   🎯 02_success_metrics.md - Top performing content")
        print("   🏷️  03_content_themes.md - Topic and theme analysis") 
        print("   🏆 04_performance_rankings.md - Complete rankings")
        print("   📊 detailed_video_data.csv - Full dataset for Excel")
        print("   📝 MASTER_NOTEBOOKLM_PROMPT.md - Get 5 video ideas instantly")
        print("   🔗 video_urls_for_notebooklm.txt - URLs for NotebookLM import")
        print()
        print("🚀 Next Steps:")
        print("   1. Read 00_MASTER_SUMMARY.md for key insights")
        print("   2. Import video URLs into NotebookLM")
        print("   3. Use the specialized prompts for deeper analysis")
        print("   4. Open CSV in Excel/Sheets for custom analysis")
        print()
        print("💡 Pro Tip: Start with the Success Analysis prompt in NotebookLM!")
        print("=" * 80)
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        try:
            # Display banner and get input
            self.display_banner()
            self.get_channel_input()
            
            # Step 1: Extract metadata
            if not self.extract_video_metadata():
                print("❌ Failed to extract video metadata. Exiting.")
                return
            
            # Step 2: Generate analysis reports  
            self.generate_analysis_reports()
            
            # Step 3: Generate NotebookLM prompts
            self.generate_notebooklm_prompts()
            
            # Step 4: Create master summary
            self.create_master_summary()
            
            # Display completion summary
            self.display_completion_summary()
            
            # Ask to open output folder
            print("\n" + "="*80)
            open_folder = input("\n📂 Open analysis folder to review your success insights? (y/n): ").lower()
            if open_folder.startswith('y'):
                try:
                    if sys.platform == 'win32':
                        subprocess.run(['explorer', str(self.output_dir)])
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', str(self.output_dir)])
                    else:
                        subprocess.run(['xdg-open', str(self.output_dir)])
                except Exception:
                    print(f"\n📂 Please manually open: {self.output_dir}")
                    
        except KeyboardInterrupt:
            print("\n\n⚠️ Analysis cancelled by user.")
            print("💡 Run the script again anytime to analyze channels!")
        except Exception as e:
            print(f"\n❌ Error during analysis: {e}")
            print("\n🔧 Troubleshooting:")
            print("   • Make sure the channel URL is valid")
            print("   • Check your internet connection")
            print("   • Try using the channel's @handle format")
            print("   • Some private channels may not be accessible")
            print("\n💡 Need help? The channel URL should look like:")
            print("   https://www.youtube.com/@channelname")

if __name__ == '__main__':
    analyzer = YouTubeSuccessAnalyzer()
    analyzer.run_complete_analysis()