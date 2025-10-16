#!/usr/bin/env python3
"""
YouTube Performance Auditor
Analyzes your channel's performance data and provides actionable optimization insights.
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys


class YouTubePerformanceAuditor:
    def __init__(self, totals_csv=None, chart_data_csv=None):
        """Initialize the auditor with CSV file paths."""
        self.totals_csv = totals_csv
        self.chart_data_csv = chart_data_csv
        self.totals_df = None
        self.chart_df = None
        self.analysis_results = {}
        
    def display_banner(self):
        """Display the auditor banner."""
        print()
        print("="*80)
        print("📊 YouTube Performance Auditor - Data-Driven Optimization")
        print("="*80)
        print()
        print("🎯 WHAT THIS AUDITOR DOES:")
        print("   ✅ Analyzes your actual channel performance data")
        print("   ✅ Identifies which videos are working (and why)")
        print("   ✅ Reveals growth patterns and engagement trends")
        print("   ✅ Provides actionable optimization recommendations")
        print("   ✅ Generates a strategic action plan for maximum impact")
        print()
        print("="*80)
        print()
    
    def load_data(self):
        """Load and validate CSV data."""
        print("📂 STEP 1: Loading Your Performance Data")
        print("-"*80)
        
        try:
            # Load totals data
            if self.totals_csv and os.path.exists(self.totals_csv):
                self.totals_df = pd.read_csv(self.totals_csv)
                self.totals_df['Date'] = pd.to_datetime(self.totals_df['Date'])
                print(f"   ✅ Loaded totals data: {len(self.totals_df)} days")
            else:
                print("   ⚠️  No totals CSV found")
            
            # Load chart data
            if self.chart_data_csv and os.path.exists(self.chart_data_csv):
                self.chart_df = pd.read_csv(self.chart_data_csv)
                self.chart_df['Date'] = pd.to_datetime(self.chart_df['Date'])
                print(f"   ✅ Loaded chart data: {len(self.chart_df)} records")
                print(f"   📹 Videos tracked: {self.chart_df['Video title'].nunique()}")
            else:
                print("   ⚠️  No chart data CSV found")
            
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Error loading data: {e}")
            return False
    
    def analyze_overall_performance(self):
        """Analyze overall channel performance."""
        print("📈 STEP 2: Overall Performance Analysis")
        print("-"*80)
        
        if self.totals_df is None:
            print("   ⚠️  No data to analyze")
            return
        
        # Calculate key metrics
        total_views = self.totals_df['Views'].sum()
        days_active = len(self.totals_df[self.totals_df['Views'] > 0])
        avg_daily_views = self.totals_df['Views'].mean()
        peak_day_views = self.totals_df['Views'].max()
        peak_date = self.totals_df[self.totals_df['Views'] == peak_day_views]['Date'].iloc[0]
        
        # Growth trend
        first_half = self.totals_df.iloc[:len(self.totals_df)//2]['Views'].sum()
        second_half = self.totals_df.iloc[len(self.totals_df)//2:]['Views'].sum()
        growth_rate = ((second_half - first_half) / max(first_half, 1)) * 100 if first_half > 0 else 0
        
        print(f"   📊 Total Views: {total_views}")
        print(f"   📅 Days with Activity: {days_active} / {len(self.totals_df)}")
        print(f"   📈 Average Daily Views: {avg_daily_views:.1f}")
        print(f"   🔥 Peak Day: {peak_date.strftime('%Y-%m-%d')} ({int(peak_day_views)} views)")
        print(f"   📊 Growth Trend: {growth_rate:+.1f}% (first half vs second half)")
        print()
        
        self.analysis_results['overall'] = {
            'total_views': total_views,
            'days_active': days_active,
            'avg_daily_views': avg_daily_views,
            'peak_day_views': peak_day_views,
            'peak_date': peak_date,
            'growth_rate': growth_rate
        }
    
    def analyze_video_performance(self):
        """Analyze individual video performance."""
        print("🎬 STEP 3: Video-by-Video Performance Analysis")
        print("-"*80)
        
        if self.chart_df is None:
            print("   ⚠️  No video data to analyze")
            return
        
        # Group by video and calculate metrics
        video_stats = self.chart_df.groupby(['Video title', 'Content', 'Duration']).agg({
            'Views': 'sum',
            'Date': ['min', 'max']
        }).reset_index()
        
        video_stats.columns = ['Video title', 'Content', 'Duration', 'Total Views', 'First Date', 'Last Date']
        video_stats['Days Active'] = (video_stats['Last Date'] - video_stats['First Date']).dt.days + 1
        video_stats['Avg Daily Views'] = video_stats['Total Views'] / video_stats['Days Active']
        video_stats['Duration Minutes'] = video_stats['Duration'] / 60
        
        # Sort by total views
        video_stats = video_stats.sort_values('Total Views', ascending=False)
        
        print("   🏆 TOP PERFORMING VIDEOS:\n")
        for idx, row in video_stats.head(5).iterrows():
            print(f"   #{video_stats.index.get_loc(idx) + 1}. {row['Video title']}")
            print(f"      📊 Total Views: {int(row['Total Views'])}")
            print(f"      📈 Avg Daily Views: {row['Avg Daily Views']:.1f}")
            print(f"      ⏱️  Duration: {row['Duration Minutes']:.1f} minutes")
            print(f"      📅 Active: {row['Days Active']} days")
            print()
        
        # Find underperformers
        print("   ⚠️  UNDERPERFORMING VIDEOS:\n")
        bottom_videos = video_stats[video_stats['Total Views'] < video_stats['Total Views'].median()]
        for idx, row in bottom_videos.head(3).iterrows():
            print(f"   • {row['Video title']}")
            print(f"      📊 Total Views: {int(row['Total Views'])} (below median)")
            print(f"      💡 Opportunity: Needs better title/thumbnail or promotion")
            print()
        
        self.analysis_results['videos'] = video_stats
    
    def identify_success_patterns(self):
        """Identify patterns in successful content."""
        print("🔍 STEP 4: Success Pattern Identification")
        print("-"*80)
        
        if self.chart_df is None or 'videos' not in self.analysis_results:
            print("   ⚠️  Insufficient data for pattern analysis")
            return
        
        video_stats = self.analysis_results['videos']
        
        # Analyze title patterns
        print("   📝 TITLE PATTERN ANALYSIS:\n")
        
        # Title length analysis
        video_stats['Title Length'] = video_stats['Video title'].str.len()
        avg_title_length = video_stats['Title Length'].mean()
        
        top_video = video_stats.iloc[0]
        top_performer_title_length = video_stats.iloc[0]['Title Length']
        
        print(f"   🏆 Best Performing Title: \"{top_video['Video title']}\"")
        print(f"      → {int(top_video['Total Views'])} total views")
        
        print(f"   📏 Average Title Length: {avg_title_length:.0f} characters")
        print(f"   📏 Top Performer Length: {top_performer_title_length} characters")
        
        # Duration analysis
        print(f"\n   ⏱️  DURATION ANALYSIS:\n")
        avg_duration = video_stats['Duration Minutes'].mean()
        top_duration = top_video['Duration Minutes']
        
        print(f"   📊 Average Video Duration: {avg_duration:.1f} minutes")
        print(f"   🏆 Top Performer Duration: {top_duration:.1f} minutes")
        
        if top_duration < avg_duration:
            print(f"   💡 Insight: Shorter videos ({top_duration:.1f}m) outperforming longer ones")
        else:
            print(f"   💡 Insight: Longer videos ({top_duration:.1f}m) getting more engagement")
        
        print()
        
        self.analysis_results['patterns'] = {
            'avg_title_length': avg_title_length,
            'top_title_length': top_performer_title_length,
            'avg_duration': avg_duration,
            'top_duration': top_duration
        }
    
    def analyze_timing_patterns(self):
        """Analyze when videos perform best."""
        print("⏰ STEP 5: Timing & Engagement Pattern Analysis")
        print("-"*80)
        
        if self.chart_df is None:
            print("   ⚠️  No timing data available")
            return
        
        # Daily performance patterns
        daily_views = self.chart_df.groupby('Date')['Views'].sum().reset_index()
        daily_views['Day of Week'] = daily_views['Date'].dt.day_name()
        
        # Find best days
        dow_performance = self.chart_df.copy()
        dow_performance['Day of Week'] = dow_performance['Date'].dt.day_name()
        dow_stats = dow_performance.groupby('Day of Week')['Views'].sum().sort_values(ascending=False)
        
        print("   📅 BEST DAYS FOR VIEWS:\n")
        for day, views in dow_stats.head(3).items():
            print(f"   • {day}: {int(views)} views")
        
        print(f"\n   💡 Optimization Tip: Focus promotion efforts on {dow_stats.index[0]}")
        print()
        
        self.analysis_results['timing'] = {
            'best_day': dow_stats.index[0],
            'best_day_views': dow_stats.iloc[0]
        }
    
    def generate_recommendations(self):
        """Generate actionable optimization recommendations."""
        print("🎯 STEP 6: Strategic Optimization Recommendations")
        print("="*80)
        print()
        
        recommendations = []
        
        # Overall performance recommendations
        if 'overall' in self.analysis_results:
            overall = self.analysis_results['overall']
            
            print("📊 CHANNEL GROWTH STRATEGY:\n")
            
            if overall['growth_rate'] > 0:
                print(f"   ✅ MOMENTUM DETECTED: {overall['growth_rate']:.1f}% growth")
                print("   → Double down on your current content strategy")
                recommendations.append({
                    'priority': 'HIGH',
                    'action': 'Maintain posting consistency',
                    'why': f"You have positive growth momentum ({overall['growth_rate']:.1f}%)"
                })
            else:
                print(f"   ⚠️  GROWTH STAGNANT: {overall['growth_rate']:.1f}% change")
                print("   → Need to try new content formats or topics")
                recommendations.append({
                    'priority': 'CRITICAL',
                    'action': 'Experiment with new content angles',
                    'why': 'Current strategy not driving growth'
                })
            
            if overall['days_active'] < len(self.totals_df) * 0.5:
                print(f"\n   ⚠️  LOW ACTIVITY: Only {overall['days_active']} active days")
                print("   → Increase posting frequency for better algorithm performance")
                recommendations.append({
                    'priority': 'HIGH',
                    'action': 'Increase posting frequency to 3-4x per week',
                    'why': 'Low activity hurts algorithm visibility'
                })
            
            print()
        
        # Video-specific recommendations
        if 'videos' in self.analysis_results:
            video_stats = self.analysis_results['videos']
            
            print("🎬 VIDEO OPTIMIZATION STRATEGY:\n")
            
            top_video = video_stats.iloc[0]
            print(f"   🏆 REPLICATE SUCCESS: \"{top_video['Video title']}\"")
            print(f"      → Create 2-3 similar videos using this format")
            recommendations.append({
                'priority': 'CRITICAL',
                'action': f'Create follow-up to "{top_video["Video title"][:30]}..."',
                'why': f'This format generated {int(top_video["Total Views"])} views'
            })
            
            # Check for underperformers
            low_performers = video_stats[video_stats['Total Views'] < 5]
            if len(low_performers) > 0:
                print(f"\n   ⚠️  {len(low_performers)} VIDEOS NEED ATTENTION:")
                for _, video in low_performers.iterrows():
                    print(f"      • \"{video['Video title'][:40]}...\"")
                print("      → Update thumbnails & titles, or remove from channel")
                recommendations.append({
                    'priority': 'MEDIUM',
                    'action': 'Revamp low-performing video thumbnails',
                    'why': f'{len(low_performers)} videos getting minimal views'
                })
            
            print()
        
        # Pattern-based recommendations
        if 'patterns' in self.analysis_results:
            patterns = self.analysis_results['patterns']
            
            print("📝 TITLE & FORMAT OPTIMIZATION:\n")
            
            print(f"   💡 OPTIMAL TITLE LENGTH: {patterns['top_title_length']} characters")
            print(f"      → Keep titles around this length for best performance")
            recommendations.append({
                'priority': 'MEDIUM',
                'action': f'Optimize titles to ~{patterns["top_title_length"]} characters',
                'why': 'Top performer uses this length'
            })
            
            print(f"\n   ⏱️  OPTIMAL VIDEO LENGTH: {patterns['top_duration']:.1f} minutes")
            print(f"      → Aim for this duration in future videos")
            recommendations.append({
                'priority': 'MEDIUM',
                'action': f'Target {patterns["top_duration"]:.1f}-minute video length',
                'why': 'This duration drives highest engagement'
            })
            
            print()
        
        # Timing recommendations
        if 'timing' in self.analysis_results:
            timing = self.analysis_results['timing']
            
            print("⏰ POSTING SCHEDULE OPTIMIZATION:\n")
            print(f"   📅 BEST DAY TO POST: {timing['best_day']}")
            print(f"      → Schedule new videos for {timing['best_day']} release")
            recommendations.append({
                'priority': 'HIGH',
                'action': f'Schedule releases for {timing["best_day"]}',
                'why': f'This day drives {int(timing["best_day_views"])} views'
            })
            print()
        
        self.analysis_results['recommendations'] = recommendations
    
    def create_action_plan(self):
        """Create a prioritized 30-day action plan."""
        print("📋 YOUR 30-DAY OPTIMIZATION ACTION PLAN")
        print("="*80)
        print()
        
        if 'recommendations' not in self.analysis_results:
            print("   ⚠️  No recommendations generated")
            return
        
        recommendations = sorted(
            self.analysis_results['recommendations'],
            key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}.get(x['priority'], 3)
        )
        
        print("🎯 WEEK 1 - IMMEDIATE ACTIONS (CRITICAL PRIORITY):\n")
        week1 = [r for r in recommendations if r['priority'] == 'CRITICAL']
        for i, rec in enumerate(week1, 1):
            print(f"   {i}. {rec['action']}")
            print(f"      Why: {rec['why']}\n")
        
        print("📈 WEEK 2-3 - HIGH PRIORITY OPTIMIZATIONS:\n")
        week23 = [r for r in recommendations if r['priority'] == 'HIGH']
        for i, rec in enumerate(week23, 1):
            print(f"   {i}. {rec['action']}")
            print(f"      Why: {rec['why']}\n")
        
        print("🔧 WEEK 4 - FINE-TUNING (MEDIUM PRIORITY):\n")
        week4 = [r for r in recommendations if r['priority'] == 'MEDIUM']
        for i, rec in enumerate(week4, 1):
            print(f"   {i}. {rec['action']}")
            print(f"      Why: {rec['why']}\n")
        
        print("="*80)
        print("💡 NEXT STEP: Run this audit weekly to track improvement!")
        print("="*80)
        print()
    
    def run_audit(self):
        """Run the complete audit process."""
        self.display_banner()
        
        if not self.load_data():
            print("❌ Failed to load data. Please check your CSV files.")
            return False
        
        self.analyze_overall_performance()
        self.analyze_video_performance()
        self.identify_success_patterns()
        self.analyze_timing_patterns()
        self.generate_recommendations()
        self.create_action_plan()
        
        return True


def main():
    """Main execution function."""
    print("\n🎬 YouTube Performance Auditor\n")
    
    # Prompt for CSV files
    print("📂 Please provide your YouTube Analytics CSV files:")
    print()
    
    totals_path = input("1. Path to Totals CSV (e.g., 'Untitled spreadsheet - Totals.csv'): ").strip()
    chart_path = input("2. Path to Chart Data CSV (e.g., 'Untitled spreadsheet - Chart data.csv'): ").strip()
    
    # Handle quotes in paths
    totals_path = totals_path.strip('"').strip("'")
    chart_path = chart_path.strip('"').strip("'")
    
    # Create auditor and run analysis
    auditor = YouTubePerformanceAuditor(totals_path, chart_path)
    auditor.run_audit()


if __name__ == "__main__":
    main()
