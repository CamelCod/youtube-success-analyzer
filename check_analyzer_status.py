#!/usr/bin/env python3
"""
YouTube Analyzer Status Checker
Quickly diagnose if the analyzer is running, hung, or completed.
"""

import os
import sys
import time
import subprocess
from pathlib import Path


def check_running_process():
    """Check if analyzer is currently running."""
    try:
        result = subprocess.run(
            ['ps', 'aux'], 
            capture_output=True, 
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if 'youtube_success_analyzer.py' in line and 'grep' not in line:
                parts = line.split()
                pid = parts[1]
                cpu_time = parts[9]  # CPU time
                
                # Parse CPU time (format: minutes:seconds.centiseconds)
                if ':' in cpu_time:
                    mins, secs = cpu_time.split(':')
                    total_mins = int(mins) + int(float(secs)) / 60
                else:
                    total_mins = int(float(cpu_time)) / 60
                
                return {
                    'running': True,
                    'pid': pid,
                    'cpu_time': cpu_time,
                    'runtime_mins': total_mins
                }
        
        return {'running': False}
    
    except Exception as e:
        return {'running': False, 'error': str(e)}


def check_recent_output():
    """Check for recent analysis output."""
    analysis_dir = Path(__file__).parent / 'analysis'
    
    if not analysis_dir.exists():
        return None
    
    recent_dirs = []
    for channel_dir in analysis_dir.iterdir():
        if channel_dir.is_dir():
            for run_dir in channel_dir.iterdir():
                if run_dir.is_dir():
                    mtime = run_dir.stat().st_mtime
                    recent_dirs.append((mtime, channel_dir.name, run_dir.name, run_dir))
    
    if not recent_dirs:
        return None
    
    recent_dirs.sort(reverse=True)
    latest = recent_dirs[0]
    
    return {
        'timestamp': latest[0],
        'age_mins': (time.time() - latest[0]) / 60,
        'channel': latest[1],
        'run_id': latest[2],
        'path': latest[3],
        'has_files': len(list(latest[3].iterdir())) > 0
    }


def check_yt_dlp_cache():
    """Check recent yt-dlp activity."""
    cache_dir = Path.home() / '.cache' / 'yt-dlp'
    
    if not cache_dir.exists():
        return {'exists': False}
    
    recent_files = []
    cutoff = time.time() - 600  # Last 10 minutes
    
    for root, dirs, files in os.walk(cache_dir):
        for f in files:
            path = Path(root) / f
            try:
                mtime = path.stat().st_mtime
                if mtime > cutoff:
                    recent_files.append(mtime)
            except:
                pass
    
    if recent_files:
        latest = max(recent_files)
        return {
            'exists': True,
            'recent_activity': True,
            'last_activity': latest,
            'mins_ago': (time.time() - latest) / 60,
            'file_count': len(recent_files)
        }
    else:
        return {
            'exists': True,
            'recent_activity': False
        }


def main():
    """Run full diagnostic."""
    print("\n" + "="*80)
    print("🔍 YouTube Analyzer Status Diagnostic")
    print("="*80 + "\n")
    
    # Check if process is running
    print("📊 PROCESS STATUS:")
    print("-" * 80)
    process = check_running_process()
    
    if process['running']:
        runtime = process['runtime_mins']
        print(f"   ✅ Analyzer is RUNNING")
        print(f"   🆔 PID: {process['pid']}")
        print(f"   ⏱️  CPU Time: {process['cpu_time']}")
        print(f"   📈 Runtime: {runtime:.1f} minutes")
        
        if runtime > 60:
            print(f"   ⚠️  WARNING: Running for {runtime:.0f} minutes - may be hung")
            print("   💡 Check yt-dlp activity below to confirm")
    else:
        print("   ⭕ Analyzer is NOT running")
    
    print()
    
    # Check recent output
    print("📁 RECENT OUTPUT:")
    print("-" * 80)
    output = check_recent_output()
    
    if output:
        age_hrs = output['age_mins'] / 60
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(output['timestamp']))
        
        print(f"   📂 Latest Analysis: {output['channel']}")
        print(f"   🕒 Created: {time_str} ({age_hrs:.1f} hours ago)")
        print(f"   📝 Run ID: {output['run_id']}")
        print(f"   📊 Has Output: {'✅ Yes' if output['has_files'] else '❌ No (empty)'}")
        
        if output['has_files']:
            file_count = len(list(output['path'].iterdir()))
            print(f"   📄 Files Generated: {file_count}")
        else:
            print("   ⚠️  WARNING: Directory exists but no files generated")
    else:
        print("   ⭕ No recent analysis runs found")
    
    print()
    
    # Check yt-dlp activity
    print("🌐 YT-DLP ACTIVITY:")
    print("-" * 80)
    cache = check_yt_dlp_cache()
    
    if not cache['exists']:
        print("   ⭕ No yt-dlp cache found")
    elif cache['recent_activity']:
        mins_ago = cache['mins_ago']
        print(f"   ✅ Recent activity detected")
        print(f"   🕒 Last activity: {mins_ago:.1f} minutes ago")
        print(f"   📊 Active files: {cache['file_count']}")
        
        if mins_ago < 5:
            print("   💚 Analyzer is actively working!")
        elif mins_ago < 15:
            print("   💛 Some recent activity (may be slow)")
        else:
            print("   ⚠️  WARNING: No activity in 15+ minutes - likely hung")
    else:
        print("   ❌ No recent activity (last 10 minutes)")
        print("   ⚠️  Analyzer may be HUNG or waiting for input")
    
    print()
    
    # Diagnosis and recommendations
    print("🎯 DIAGNOSIS & RECOMMENDATIONS:")
    print("="*80)
    
    if process['running']:
        if cache.get('recent_activity') and cache['mins_ago'] < 10:
            print("   ✅ STATUS: Analyzer is working normally")
            print("   💡 ACTION: Let it continue - check back in 15-30 minutes")
        elif process['runtime_mins'] > 30 and not cache.get('recent_activity'):
            print("   ❌ STATUS: Analyzer is HUNG (no activity)")
            print("   💡 ACTION: Kill process and restart:")
            print(f"      kill -9 {process['pid']}")
            print("      python3 youtube_success_analyzer.py")
        elif process['runtime_mins'] > 120:
            print("   ⚠️  STATUS: Running very long (2+ hours)")
            print("   💡 ACTION: Large channel - may be normal, but monitor closely")
        else:
            print("   💛 STATUS: Running but slow progress")
            print("   💡 ACTION: Monitor for another 15-30 minutes")
    else:
        if output and not output['has_files']:
            print("   ⚠️  STATUS: Previous run failed (no output)")
            print("   💡 ACTION: Check for errors and try again")
        elif output and output['age_mins'] < 60:
            print("   ✅ STATUS: Recently completed successfully")
            print(f"   💡 ACTION: Check output in: {output['path']}")
        else:
            print("   ⭕ STATUS: Ready to run")
            print("   💡 ACTION: Start analyzer:")
            print("      python3 youtube_success_analyzer.py")
    
    print("="*80)
    print()


if __name__ == "__main__":
    main()
