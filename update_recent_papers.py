#!/usr/bin/env python3
"""
Extract the most recent papers from jailbreaking_papers.json and save them to most-recent-papers.json
for dynamic loading on the website.
"""

import json
from datetime import datetime
import sys

def extract_recent_papers(json_file_path, output_file_path, num_papers=20):
    """Extract the most recent papers and save them to a JSON file."""
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        # Sort papers by published_date (most recent first)
        papers.sort(key=lambda x: x['published_date'], reverse=True)
        
        # Take the most recent papers
        recent_papers = papers[:num_papers]
        
        # Format the papers for the website
        formatted_papers = []
        for paper in recent_papers:
            # Parse the published date
            pub_date = datetime.fromisoformat(paper['published_date'].replace('Z', '+00:00'))
            
            # Join authors with commas
            authors = ', '.join(paper['authors'])
            
            # Truncate summary if too long
            summary = paper['summary']
            if len(summary) > 200:
                summary = summary[:200] + '...'
            
            formatted_paper = {
                'title': paper['title'],
                'authors': authors,
                'date': pub_date.strftime('%Y-%m-%d'),
                'abstract': summary
            }
            formatted_papers.append(formatted_paper)
        
        # Save to output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_papers, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully extracted {len(formatted_papers)} recent papers to {output_file_path}")
        print(f"📅 Date range: {formatted_papers[-1]['date']} to {formatted_papers[0]['date']}")
        
        return formatted_papers
        
    except Exception as e:
        print(f"❌ Error processing papers: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    input_file = "paper-finder/outputs/comprehensive_analysis/jailbreaking_papers.json"
    output_file = "most-recent-papers.json"
    
    papers = extract_recent_papers(input_file, output_file, 20)
    
    if papers:
        print(f"\n📊 Summary:")
        print(f"   - Total papers extracted: {len(papers)}")
        print(f"   - Latest paper: {papers[0]['title'][:50]}...")
        print(f"   - Output file: {output_file}")
    else:
        print("❌ No papers were processed.")
        sys.exit(1) 