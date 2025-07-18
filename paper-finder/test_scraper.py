#!/usr/bin/env python3
"""
Test script for the arXiv jailbreaking paper scraper
"""

import sys
import os
from arxiv_scraper import JailbreakingPaperScraper

def test_basic_functionality():
    """Test basic scraper functionality with a small search."""
    print("🧪 Testing basic scraper functionality...")
    
    scraper = JailbreakingPaperScraper()
    
    # Test with a small search
    papers = scraper.search_papers(max_results=10)
    
    if papers:
        print(f"✅ Found {len(papers)} papers in test search")
        
        # Test analysis
        stats, df = scraper.analyze_papers()
        if stats:
            print(f"✅ Analysis completed successfully")
            print(f"   - Total papers: {stats['total_papers']}")
            print(f"   - Categories: {len(stats['categories'])}")
            return True
    else:
        print("❌ No papers found in test search")
        return False

def test_export_functionality():
    """Test export functionality."""
    print("🧪 Testing export functionality...")
    
    scraper = JailbreakingPaperScraper()
    
    # Run a small search
    papers = scraper.search_papers(max_results=5)
    
    if papers:
        stats, df = scraper.analyze_papers()
        
        # Test export
        try:
            scraper.export_results(df, 'test_outputs')
            print("✅ Export functionality works")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    else:
        print("❌ No papers to export")
        return False

def main():
    print("🚀 Starting scraper tests...\n")
    
    # Test basic functionality
    basic_test = test_basic_functionality()
    
    print()
    
    # Test export functionality
    export_test = test_export_functionality()
    
    print()
    
    if basic_test and export_test:
        print("✅ All tests passed! Scraper is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 