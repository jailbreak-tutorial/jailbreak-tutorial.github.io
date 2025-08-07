#!/usr/bin/env python3
"""
arXiv Jailbreaking LLM Paper Scraper

This script searches arXiv for papers related to LLM jailbreaking and related topics,
providing quantitative analysis and visualization of the research landscape.
"""

import arxiv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from collections import Counter
import re
from tqdm import tqdm
import argparse

class JailbreakingPaperScraper:
    def __init__(self):
        self.papers = []
        self.search_terms = {
            'jailbreaking': [
                'jailbreak', 'jailbreaking', 'jail break', 'jail-breaking',
                'adversarial prompt', 'prompt injection', "prompt hacking",
                'universal adversarial trigger', 'alignment breaking', 'universal adversarial', 'transferable adversarial', 'red team', 'red-teaming', 'red teaming'
            ],
            'prompt_engineering': [
                'prompt injection', 'prompt hacking', 'prompt manipulation', 'prompt attack', 'prompt security', 'adversarial prompt'
            ],
            'safety_alignment': [
                'AI safety', 'alignment', 'safety bypass', 'safety training', 'safety fine-tuning', 'safety alignment'
            ],
            'benchmark_evaluation': [
                'jailbreak benchmark', 'safety evaluation', 'robustness evaluation',
                'adversarial evaluation'
            ]
        }
        
    def search_papers(self, max_results=1000, date_from=None, date_to=None):
        """
        Search arXiv for papers related to jailbreaking and related topics.
        """
        print("🔍 Searching arXiv for jailbreaking-related papers...")
        
        all_papers = []
        
        for category, terms in self.search_terms.items():
            print(f"\n📊 Searching category: {category}")
            
            for term in tqdm(terms, desc=f"Searching {category}"):
                try:
                    # Create search query
                    query = f'"{term}" AND ("large language model" OR "LLM" OR "GPT" OR "language model")'
                    
                    # Add date filters if provided
                    if date_from:
                        query += f' AND submittedDate:[{date_from} TO {date_to or datetime.now().strftime("%Y%m%d")}]'
                    
                    # Search arXiv
                    search = arxiv.Search(
                        query=query,
                        max_results=max_results,
                        sort_by=arxiv.SortCriterion.SubmittedDate
                    )
                    
                    for result in search.results():
                        paper_data = {
                            'title': result.title,
                            'authors': [author.name for author in result.authors],
                            'summary': result.summary,
                            'published_date': result.published,
                            'updated_date': result.updated,
                            'arxiv_id': result.entry_id.split('/')[-1],
                            'pdf_url': result.pdf_url,
                            'categories': result.categories,
                            'search_term': term,
                            'search_category': category,
                            'word_count': len(result.summary.split())
                        }
                        
                        # Check if paper is already in our list
                        if not any(p['arxiv_id'] == paper_data['arxiv_id'] for p in all_papers):
                            all_papers.append(paper_data)
                            
                except Exception as e:
                    print(f"⚠️ Error searching for term '{term}': {e}")
                    continue
        
        self.papers = all_papers
        print(f"\n✅ Found {len(self.papers)} unique papers")
        return self.papers
    
    def analyze_papers(self):
        """
        Analyze the collected papers and generate statistics.
        """
        if not self.papers:
            print("❌ No papers to analyze. Run search_papers() first.")
            return
        
        print("\n📈 Analyzing papers...")
        
        df = pd.DataFrame(self.papers)
        
        # Basic statistics
        stats = {
            'total_papers': len(df),
            'date_range': {
                'earliest': df['published_date'].min(),
                'latest': df['published_date'].max()
            },
            'categories': df['search_category'].value_counts().to_dict(),
            'top_authors': self._get_top_authors(df),
            'top_venues': self._get_top_venues(df),
            'monthly_trends': self._get_monthly_trends(df),
            'word_count_stats': {
                'mean': df['word_count'].mean(),
                'median': df['word_count'].median(),
                'min': df['word_count'].min(),
                'max': df['word_count'].max()
            }
        }
        
        return stats, df
    
    def _get_top_authors(self, df, top_n=10):
        """Extract top authors from papers."""
        all_authors = []
        for authors in df['authors']:
            all_authors.extend(authors)
        
        author_counts = Counter(all_authors)
        return dict(author_counts.most_common(top_n))
    
    def _get_top_venues(self, df, top_n=10):
        """Extract top venues/categories from papers."""
        all_categories = []
        for categories in df['categories']:
            all_categories.extend(categories)
        
        category_counts = Counter(all_categories)
        return dict(category_counts.most_common(top_n))
    
    def _get_monthly_trends(self, df):
        """Get monthly publication trends."""
        df['month'] = df['published_date'].dt.to_period('M')
        monthly_counts = df.groupby('month').size()
        return monthly_counts.to_dict()
    
    def generate_visualizations(self, df, output_dir='outputs'):
        """
        Generate visualizations of the paper analysis.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\n📊 Generating visualizations in {output_dir}/...")
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Monthly publication trends
        plt.figure(figsize=(12, 6))
        df['month'] = df['published_date'].dt.to_period('M')
        monthly_counts = df.groupby('month').size()
        monthly_counts.plot(kind='line', marker='o')
        plt.title('Monthly Publication Trends: Jailbreaking LLM Papers', fontsize=14, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Number of Papers')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/monthly_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Cumulative publication trends
        plt.figure(figsize=(12, 6))
        df['year'] = df['published_date'].dt.year
        yearly_counts = df.groupby('year').size()
        cumulative_counts = yearly_counts.cumsum()
        cumulative_counts.plot(kind='line', marker='o', linewidth=2, markersize=8)
        plt.title('Cumulative Publication Trends: Jailbreaking LLM Papers', fontsize=14, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Cumulative Number of Papers')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/cumulative_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Category distribution
        plt.figure(figsize=(10, 6))
        category_counts = df['search_category'].value_counts()
        plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
        plt.title('Distribution by Search Category', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/category_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Top authors
        plt.figure(figsize=(12, 8))
        top_authors = self._get_top_authors(df, top_n=15)
        authors = list(top_authors.keys())
        counts = list(top_authors.values())
        
        plt.barh(range(len(authors)), counts)
        plt.yticks(range(len(authors)), authors)
        plt.xlabel('Number of Papers')
        plt.title('Top Authors in Jailbreaking LLM Research', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/top_authors.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Word count distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df['word_count'], bins=30, alpha=0.7, edgecolor='black')
        plt.xlabel('Word Count')
        plt.ylabel('Number of Papers')
        plt.title('Distribution of Abstract Word Counts', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/word_count_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Visualizations saved!")
    
    def export_results(self, df, output_dir='outputs'):
        """
        Export results to various formats.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\n💾 Exporting results to {output_dir}/...")
        
        # Export to CSV
        df.to_csv(f'{output_dir}/jailbreaking_papers.csv', index=False)
        
        # Export to JSON
        papers_json = df.to_dict('records')
        with open(f'{output_dir}/jailbreaking_papers.json', 'w') as f:
            json.dump(papers_json, f, indent=2, default=str)
        
        # Generate summary report
        stats, _ = self.analyze_papers()
        with open(f'{output_dir}/summary_report.txt', 'w') as f:
            f.write("Jailbreaking LLM Papers Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Papers Found: {stats['total_papers']}\n")
            f.write(f"Date Range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}\n\n")
            
            f.write("Category Distribution:\n")
            for category, count in stats['categories'].items():
                f.write(f"  {category}: {count} papers\n")
            
            f.write(f"\nTop Authors:\n")
            for author, count in list(stats['top_authors'].items())[:10]:
                f.write(f"  {author}: {count} papers\n")
        
        print("✅ Results exported!")
    
    def run_complete_analysis(self, max_results=1000, date_from=None, output_dir='outputs'):
        """
        Run complete analysis pipeline.
        """
        print("🚀 Starting complete jailbreaking LLM paper analysis...")
        
        # Search for papers
        self.search_papers(max_results=max_results, date_from=date_from)
        
        if not self.papers:
            print("❌ No papers found. Exiting.")
            return
        
        # Analyze papers
        stats, df = self.analyze_papers()
        
        # Generate visualizations
        self.generate_visualizations(df, output_dir)
        
        # Export results
        self.export_results(df, output_dir)
        
        # Print summary
        print(f"\n📋 Summary:")
        print(f"  Total papers: {stats['total_papers']}")
        print(f"  Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        print(f"  Categories: {len(stats['categories'])}")
        print(f"  Results saved to: {output_dir}/")
        
        return stats, df

def main():
    parser = argparse.ArgumentParser(description='arXiv Jailbreaking LLM Paper Scraper')
    parser.add_argument('--max-results', type=int, default=1000, help='Maximum results per search term')
    parser.add_argument('--date-from', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--output-dir', type=str, default='outputs', help='Output directory')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = JailbreakingPaperScraper()
    
    # Run analysis
    stats, df = scraper.run_complete_analysis(
        max_results=args.max_results,
        date_from=args.date_from,
        output_dir=args.output_dir
    )
    
    if args.visualize and df is not None:
        scraper.generate_visualizations(df, args.output_dir)

if __name__ == "__main__":
    main() 