#!/usr/bin/env python3
"""
Example usage of the arXiv jailbreaking paper scraper
"""

from arxiv_scraper import JailbreakingPaperScraper
from datetime import datetime, timedelta

def example_basic_usage():
    """Basic usage example."""
    print("📚 Example: Basic Usage")
    print("=" * 40)
    
    # Initialize scraper
    scraper = JailbreakingPaperScraper()
    
    # Search for recent papers
    papers = scraper.search_papers(max_results=50)
    
    if papers:
        print(f"Found {len(papers)} papers")
        
        # Analyze the papers
        stats, df = scraper.analyze_papers()
        
        print(f"\n📊 Analysis Results:")
        print(f"  Total papers: {stats['total_papers']}")
        print(f"  Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        
        print(f"\n📈 Category Distribution:")
        for category, count in stats['categories'].items():
            print(f"  {category}: {count} papers")
        
        print(f"\n👥 Top Authors:")
        for author, count in list(stats['top_authors'].items())[:5]:
            print(f"  {author}: {count} papers")
    
    print("\n" + "=" * 40)

def example_custom_search():
    """Example with custom search parameters."""
    print("📚 Example: Custom Search")
    print("=" * 40)
    
    scraper = JailbreakingPaperScraper()
    
    # Search for papers from last year
    one_year_ago = datetime.now() - timedelta(days=365)
    date_from = one_year_ago.strftime('%Y%m%d')
    
    papers = scraper.search_papers(
        max_results=100,
        date_from=date_from
    )
    
    if papers:
        print(f"Found {len(papers)} papers from the last year")
        
        # Generate visualizations
        stats, df = scraper.analyze_papers()
        scraper.generate_visualizations(df, 'example_outputs')
        
        print("✅ Visualizations saved to example_outputs/")
    
    print("\n" + "=" * 40)

def example_export_data():
    """Example of exporting data in different formats."""
    print("📚 Example: Data Export")
    print("=" * 40)
    
    scraper = JailbreakingPaperScraper()
    
    # Search for papers
    papers = scraper.search_papers(max_results=25)
    
    if papers:
        stats, df = scraper.analyze_papers()
        
        # Export to different formats
        scraper.export_results(df, 'example_exports')
        
        print("✅ Data exported to:")
        print("  - example_exports/jailbreaking_papers.csv")
        print("  - example_exports/jailbreaking_papers.json")
        print("  - example_exports/summary_report.txt")
    
    print("\n" + "=" * 40)

def main():
    print("🚀 arXiv Jailbreaking Paper Scraper - Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_custom_search()
    example_export_data()
    
    print("✅ All examples completed!")

if __name__ == "__main__":
    main() 