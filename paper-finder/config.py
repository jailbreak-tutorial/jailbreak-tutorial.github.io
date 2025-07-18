"""
Configuration file for the arXiv Jailbreaking LLM Paper Scraper
"""

# Search terms organized by category
SEARCH_TERMS = {
    'jailbreaking': [
        'jailbreak', 'jailbreaking', 'jail break', 'jail-breaking',
        'adversarial prompt', 'adversarial attack', 'prompt injection',
        'indirect prompt injection', 'universal adversarial trigger',
        'alignment breaking', 'safety bypass', 'red teaming'
    ],
    'prompt_engineering': [
        'prompt engineering', 'prompt injection', 'prompt hacking',
        'prompt manipulation', 'prompt attack', 'prompt security'
    ],
    'adversarial_attacks': [
        'adversarial attack', 'adversarial prompt', 'adversarial example',
        'universal adversarial', 'transferable adversarial'
    ],
    'safety_alignment': [
        'AI safety', 'alignment', 'safety bypass', 'safety violation',
        'harmful content', 'safety evaluation', 'robustness'
    ],
    'red_teaming': [
        'red team', 'red-teaming', 'red teaming', 'adversarial testing',
        'safety testing', 'vulnerability assessment'
    ],
    'benchmark_evaluation': [
        'jailbreak benchmark', 'safety evaluation', 'robustness evaluation',
        'adversarial evaluation', 'safety testing'
    ]
}

# LLM-related terms to include in search
LLM_TERMS = [
    'large language model', 'LLM', 'GPT', 'language model',
    'transformer', 'BERT', 'T5', 'PaLM', 'Claude', 'ChatGPT'
]

# Date ranges for analysis
DEFAULT_DATE_FROM = '2020-01-01'  # Start from 2020
DEFAULT_DATE_TO = None  # Up to current date

# Output settings
DEFAULT_OUTPUT_DIR = 'outputs'
DEFAULT_MAX_RESULTS = 1000

# Visualization settings
FIGURE_SIZE = (12, 8)
DPI = 300
COLOR_PALETTE = 'husl'

# Analysis settings
TOP_AUTHORS_COUNT = 15
TOP_VENUES_COUNT = 10
WORD_COUNT_BINS = 30 