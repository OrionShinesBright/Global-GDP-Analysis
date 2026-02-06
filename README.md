# Global GDP Analysis

A simple python dataset visualizer and analyzer that uses the World Bank GDP report dataset.

## Rationale

Made for our SDA semester project, the major purpose of this project is to showcase strong functional programming concepts, and clean architecture. The program is modular, and configuration based. Documentation is a key aspect of the codebase.

## Project Structure
```bash
.
├── config.json             # User configuration file
├── dashboard.py            # Visualization module
├── data_loader.py          # Data Fetching module
├── data_processor.py       # Data Processing module
├── data/
│   └── gdp.csv             # dataset in separate directory
├── Makefile
└── README.md
```

## External Tools

We have made use of the following external tools, to improve the smoothness of our workflows:
1. [ruff](https://github.com/astral-sh/ruff.git) (for formatting python code)
2. [matplotlib](https://matplotlib.org/) (for visualization and plotting graphs)
