#!/usr/bin/env python3
"""
Script to regenerate visualizations from existing data without re-scraping.
Perfect for iterating on plot formatting and styling.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import argparse
from collections import Counter
from datetime import datetime
import numpy as np

class PlotRegenerator:
    def __init__(self, data_file=None):
        self.df = None
        self.data_file = data_file
        
    def load_data(self, data_file=None):
        """Load data from CSV or JSON file."""
        if data_file:
            self.data_file = data_file
        
        if not self.data_file:
            print("❌ No data file specified. Use --data-file or set data_file parameter.")
            return False
        
        print(f"📂 Loading data from {self.data_file}...")
        
        try:
            if self.data_file.endswith('.csv'):
                self.df = pd.read_csv(self.data_file)
            elif self.data_file.endswith('.json'):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.df = pd.DataFrame(data)
            else:
                print(f"❌ Unsupported file format: {self.data_file}")
                return False
            
            # Convert date columns
            if 'published_date' in self.df.columns:
                self.df['published_date'] = pd.to_datetime(self.df['published_date'])
            
            print(f"✅ Loaded {len(self.df)} papers")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def _get_top_authors(self, df, top_n=10):
        """Extract top authors from papers."""
        all_authors = []
        for authors in df['authors']:
            if isinstance(authors, str):
                # Handle string representation of list
                import ast
                try:
                    authors = ast.literal_eval(authors)
                except:
                    authors = [authors]
            all_authors.extend(authors)
        
        author_counts = Counter(all_authors)
        return dict(author_counts.most_common(top_n))
    
    def _get_top_venues(self, df, top_n=10):
        """Extract top venues/categories from papers."""
        all_categories = []
        for categories in df['categories']:
            if isinstance(categories, str):
                # Handle string representation of list
                import ast
                try:
                    categories = ast.literal_eval(categories)
                except:
                    categories = [categories]
            all_categories.extend(categories)
        
        category_counts = Counter(all_categories)
        return dict(category_counts.most_common(top_n))
    
    def generate_visualizations(self, output_dir='outputs', style='default'):
        """
        Generate visualizations from loaded data.
        """
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\n📊 Generating visualizations in {output_dir}/...")
        
        # Set style
        if style == 'default':
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
        elif style == 'minimal':
            plt.style.use('default')
            plt.rcParams['figure.facecolor'] = 'white'
            plt.rcParams['axes.facecolor'] = 'white'
        elif style == 'dark':
            plt.style.use('dark_background')
        
        # 1. Monthly publication trends
        self._plot_monthly_trends(output_dir)
        
        # 2. Cumulative publication trends
        self._plot_cumulative_trends(output_dir)
        
        # 3. Category distribution
        self._plot_category_distribution(output_dir)
        
        # 4. Top authors
        self._plot_top_authors(output_dir)
        
        # 5. Word count distribution
        self._plot_word_count_distribution(output_dir)
        
        # 6. Publication heatmap (new)
        self._plot_publication_heatmap(output_dir)
        
        print("✅ Visualizations saved!")
    
    def _plot_monthly_trends(self, output_dir):
        """Plot monthly publication trends."""
        plt.figure(figsize=(12, 6))
        self.df['month'] = self.df['published_date'].dt.to_period('M')
        monthly_counts = self.df.groupby('month').size()
        monthly_counts.plot(kind='line', marker='o', linewidth=2, markersize=4)
        plt.title('Monthly Publication Trends: Jailbreaking LLM Papers', fontsize=14, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Number of Papers')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/monthly_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_cumulative_trends(self, output_dir):
        """Plot cumulative publication trends."""
        plt.figure(figsize=(12, 6))
        
        # Set seaborn whitegrid style
        sns.set_style("whitegrid")
        
        # Set all text to Palatino font
        plt.rcParams['font.family'] = 'Palatino'
        
        self.df['year'] = self.df['published_date'].dt.year
        yearly_counts = self.df.groupby('year').size()
        cumulative_counts = yearly_counts.cumsum()
        
        # Filter to show only from 2021 to present (exclude 2020)
        cumulative_counts = cumulative_counts[cumulative_counts.index >= 2021]
        
        # Plot with red line
        cumulative_counts.plot(kind='line', marker='o', linewidth=2, markersize=8, color='red')
        
        # Set title with larger font
        # plt.title('Cumulative Number of Jailbreaking Papers', fontsize=24, fontweight='bold')
        
        # Remove x and y labels
        plt.xlabel('')
        plt.ylabel('')
        
        # Format x-axis to show only years with larger font
        plt.xticks(cumulative_counts.index, cumulative_counts.index, fontsize=18)
        plt.yticks(fontsize=18)
        
        plt.tight_layout()
        # plt.savefig(f'{output_dir}/cumulative_trends.png', dpi=300, bbox_inches='tight')
        # plt.close()
        plt.show()
    
    def _plot_category_distribution(self, output_dir):
        """Plot category distribution."""
        plt.figure(figsize=(10, 6))
        category_counts = self.df['search_category'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(category_counts)))
        plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', colors=colors)
        plt.title('Distribution by Search Category', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/category_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_top_authors(self, output_dir):
        """Plot top authors."""
        plt.figure(figsize=(12, 8))
        top_authors = self._get_top_authors(self.df, top_n=15)
        authors = list(top_authors.keys())
        counts = list(top_authors.values())
        
        # Create horizontal bar plot
        y_pos = np.arange(len(authors))
        plt.barh(y_pos, counts, color='skyblue', edgecolor='navy', alpha=0.7)
        plt.yticks(y_pos, authors)
        plt.xlabel('Number of Papers')
        plt.title('Top Authors in Jailbreaking LLM Research', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/top_authors.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_word_count_distribution(self, output_dir):
        """Plot word count distribution."""
        plt.figure(figsize=(10, 6))
        plt.hist(self.df['word_count'], bins=30, alpha=0.7, edgecolor='black', color='lightcoral')
        plt.xlabel('Word Count')
        plt.ylabel('Number of Papers')
        plt.title('Distribution of Abstract Word Counts', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/word_count_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_publication_heatmap(self, output_dir):
        """Plot publication heatmap by year and category."""
        plt.figure(figsize=(12, 8))
        
        # Create pivot table
        self.df['year'] = self.df['published_date'].dt.year
        heatmap_data = self.df.groupby(['year', 'search_category']).size().unstack(fill_value=0)
        
        # Create heatmap
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Number of Papers'})
        plt.title('Publication Heatmap: Papers by Year and Category', fontsize=14, fontweight='bold')
        plt.xlabel('Search Category')
        plt.ylabel('Year')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/publication_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def customize_plot_style(self, style_config):
        """
        Apply custom plot styling.
        
        Args:
            style_config (dict): Dictionary with style parameters
                - figure_size: tuple (width, height)
                - dpi: int
                - color_palette: str
                - font_size: int
                - grid_alpha: float
        """
        if 'figure_size' in style_config:
            plt.rcParams['figure.figsize'] = style_config['figure_size']
        if 'dpi' in style_config:
            plt.rcParams['figure.dpi'] = style_config['dpi']
        if 'font_size' in style_config:
            plt.rcParams['font.size'] = style_config['font_size']
        if 'grid_alpha' in style_config:
            plt.rcParams['grid.alpha'] = style_config['grid_alpha']

def main():
    parser = argparse.ArgumentParser(description='Regenerate visualizations from existing data')
    parser.add_argument('--data-file', type=str, required=True, help='Path to CSV or JSON data file')
    parser.add_argument('--output-dir', type=str, default='outputs', help='Output directory for plots')
    parser.add_argument('--style', type=str, default='default', 
                       choices=['default', 'minimal', 'dark'], help='Plot style')
    parser.add_argument('--figure-size', type=str, help='Figure size as "width,height" (e.g., "12,8")')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for saved figures')
    parser.add_argument('--font-size', type=int, help='Base font size')
    
    args = parser.parse_args()
    
    # Initialize regenerator
    regenerator = PlotRegenerator()
    
    # Load data
    if not regenerator.load_data(args.data_file):
        return
    
    # Apply custom styling if specified
    style_config = {}
    if args.figure_size:
        width, height = map(int, args.figure_size.split(','))
        style_config['figure_size'] = (width, height)
    if args.dpi:
        style_config['dpi'] = args.dpi
    if args.font_size:
        style_config['font_size'] = args.font_size
    
    if style_config:
        regenerator.customize_plot_style(style_config)
    
    # Generate visualizations
    regenerator.generate_visualizations(args.output_dir, args.style)
    
    print(f"\n✅ All plots regenerated in {args.output_dir}/")

if __name__ == "__main__":
    main() 