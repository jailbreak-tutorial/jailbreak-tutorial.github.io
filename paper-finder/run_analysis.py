#!/usr/bin/env python3
"""
Simple script to run the arXiv jailbreaking paper analysis
"""

import sys
import os
from datetime import datetime, timedelta
from arxiv_scraper import JailbreakingPaperScraper

def run_basic_analysis():
    """Run a basic analysis of recent papers."""
    print("🔍 Running basic jailbreaking LLM paper analysis...")
    
    scraper = JailbreakingPaperScraper()
    
    # Search for papers from 2022 onwards
    date_from = '20220101'
    
    stats, df = scraper.run_complete_analysis(
        max_results=500,
        date_from=date_from,
        output_dir='outputs/basic_analysis'
    )
    
    return stats, df

def run_comprehensive_analysis():
    """Run a comprehensive analysis of all papers."""
    print("🔍 Running comprehensive jailbreaking LLM paper analysis...")
    
    scraper = JailbreakingPaperScraper()
    
    # Search for papers from 2020 onwards
    date_from = '20200101'
    
    stats, df = scraper.run_complete_analysis(
        max_results=1000,
        date_from=date_from,
        output_dir='outputs/comprehensive_analysis'
    )
    
    return stats, df

def run_recent_analysis():
    """Run analysis of very recent papers (last 6 months)."""
    print("🔍 Running recent jailbreaking LLM paper analysis...")
    
    scraper = JailbreakingPaperScraper()
    
    # Search for papers from last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    date_from = six_months_ago.strftime('%Y%m%d')
    
    stats, df = scraper.run_complete_analysis(
        max_results=200,
        date_from=date_from,
        output_dir='outputs/recent_analysis'
    )
    
    return stats, df

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_analysis.py [basic|comprehensive|recent]")
        print("\nOptions:")
        print("  basic         - Analyze papers from 2022 onwards")
        print("  comprehensive - Analyze papers from 2020 onwards")
        print("  recent        - Analyze papers from last 6 months")
        return
    
    analysis_type = sys.argv[1].lower()
    
    if analysis_type == 'basic':
        stats, df = run_basic_analysis()
    elif analysis_type == 'comprehensive':
        stats, df = run_comprehensive_analysis()
    elif analysis_type == 'recent':
        stats, df = run_recent_analysis()
    else:
        print(f"❌ Unknown analysis type: {analysis_type}")
        return
    
    if stats:
        print(f"\n✅ Analysis complete!")
        print(f"📊 Found {stats['total_papers']} papers")
        print(f"📅 Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")

if __name__ == "__main__":
    main() 