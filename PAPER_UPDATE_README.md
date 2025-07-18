# Paper Tracker Update Workflow

This document explains how to update the recent papers displayed on the paper tracker page.

## Workflow

### 1. Run Paper Finder Analysis
First, run the comprehensive analysis in the paper-finder directory:
```bash
cd paper-finder
python run_analysis.py
```

### 2. Update Recent Papers
After the analysis is complete, run the update script to extract the most recent papers:
```bash
python3 update_recent_papers.py
```

This script will:
- Read from `paper-finder/outputs/comprehensive_analysis/jailbreaking_papers.json`
- Extract the 20 most recent papers
- Save them to `most-recent-papers.json`
- Display a summary of the extracted papers

### 3. Website Updates
The paper tracker page (`paper-tracker.html`) will automatically load the updated papers from `most-recent-papers.json` when the page is refreshed.

## Files

- `update_recent_papers.py` - Script to extract recent papers
- `most-recent-papers.json` - Output file with recent papers (auto-generated)
- `paper-tracker.html` - Web page that loads papers dynamically

## Features

- **Dynamic Loading**: Papers are loaded from JSON file, not hardcoded
- **Error Handling**: Graceful fallback if JSON file is missing
- **Simplified Venues**: All papers show "arXiv" as venue (removed categorization)
- **Full Author Lists**: Complete author names, not abbreviated
- **Recent Papers**: Always shows the 20 most recent papers from the dataset

## Example Output

When you run `update_recent_papers.py`, you'll see:
```
✅ Successfully extracted 20 recent papers to most-recent-papers.json
📅 Date range: 2025-07-02 to 2025-07-03

📊 Summary:
   - Total papers extracted: 20
   - Latest paper: Answer Matching Outperforms Multiple Choice for La...
   - Output file: most-recent-papers.json
``` 