# arXiv Jailbreaking LLM Paper Scraper

A comprehensive tool to search, analyze, and visualize arXiv papers related to LLM jailbreaking and related topics.

## Features

- **Comprehensive Search**: Searches across multiple categories of jailbreaking-related terms
- **Quantitative Analysis**: Provides statistics on publication trends, authors, and venues
- **Visualization**: Generates charts and graphs for better understanding
- **Data Export**: Exports results in CSV, JSON, and text formats
- **Flexible Configuration**: Customizable search terms and date ranges

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run a basic analysis of recent papers:
```bash
python run_analysis.py basic
```

### Available Analysis Types

- **basic**: Papers from 2022 onwards (500 max results)
- **comprehensive**: Papers from 2020 onwards (1000 max results)  
- **recent**: Papers from last 6 months (200 max results)

### Advanced Usage

Run the scraper directly with custom parameters:
```bash
python arxiv_scraper.py --max-results 1000 --date-from 2023-01-01 --output-dir my_outputs
```

### Command Line Options

- `--max-results`: Maximum results per search term (default: 1000)
- `--date-from`: Start date in YYYY-MM-DD format
- `--output-dir`: Output directory (default: outputs)
- `--visualize`: Generate visualizations

## Search Categories

The scraper searches for papers in these categories:

1. **Jailbreaking**: Direct jailbreaking techniques and attacks
2. **Prompt Engineering**: Prompt manipulation and injection
3. **Adversarial Attacks**: Adversarial examples and attacks
4. **Safety & Alignment**: AI safety and alignment research
5. **Red Teaming**: Adversarial testing and evaluation
6. **Benchmark Evaluation**: Safety evaluation and benchmarking

## Output Files

The scraper generates several output files:

- `jailbreaking_papers.csv`: Complete dataset in CSV format
- `jailbreaking_papers.json`: Complete dataset in JSON format
- `summary_report.txt`: Text summary of findings
- `monthly_trends.png`: Publication trends over time
- `cumulative_trends.png`: Cumulative publication trends by year
- `category_distribution.png`: Distribution by search category
- `top_authors.png`: Most prolific authors
- `word_count_distribution.png`: Abstract length distribution

## Example Output

```
🚀 Starting complete jailbreaking LLM paper analysis...
🔍 Searching arXiv for jailbreaking-related papers...

📊 Searching category: jailbreaking
Searching jailbreaking: 100%|██████████| 12/12 [00:30<00:00]

📊 Searching category: prompt_engineering
Searching prompt_engineering: 100%|██████████| 6/6 [00:15<00:00]

✅ Found 247 unique papers

📈 Analyzing papers...
📊 Generating visualizations in outputs/...
✅ Visualizations saved!
💾 Exporting results to outputs/...
✅ Results exported!

📋 Summary:
  Total papers: 247
  Date range: 2020-01-15 to 2024-01-15
  Categories: 6
  Results saved to: outputs/
```

## Configuration

Edit `config.py` to customize:
- Search terms and categories
- Date ranges
- Output settings
- Visualization parameters

## Dependencies

- `arxiv`: arXiv API client
- `pandas`: Data manipulation
- `matplotlib`: Plotting
- `seaborn`: Statistical visualization
- `tqdm`: Progress bars
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{jailbreaking_scraper,
  title={arXiv Jailbreaking LLM Paper Scraper},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/jailbreaking-scraper}
}
``` 