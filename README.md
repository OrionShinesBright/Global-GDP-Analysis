# Global GDP Analysis

A simple python dataset visualizer and analyzer that uses the World Bank GDP report dataset.

---

## Rationale

Made for our SDA semester project, the major purpose of this project is to showcase strong functional programming concepts, and clean architecture. The program is modular, and configuration based. Showcasing the power and succinctness of the Functional Programming Paradigm. Documentation is a key aspect of the codebase.

---

## Project Structure
```bash
Global-GDP-Analysis/
├── README.md
├── config.json
├── core/
│   ├── __init__.py
│   ├── compute_operations.py
│   ├── data_processor.py
│   └── protocols.py
├── data/
│   ├── World_Bank_Dataset.csv
│   └── gdp_with_continent_filled.json
├── main.py
└── plugins/
    ├── input/
    │   ├── __init__.py
    │   └── data_loader.py
    └── output/
        ├── __init__.py
        ├── chart_implementations.py
        ├── chart_render.py
        ├── console_writer.py
        ├── dashboard.py
        ├── prompt_handler.py
        └── protocols.py
```

---

## How to Run

**Clone the Repository**
```bash
git clone https://github.com/OrionShinesBright/Global-GDP-Analysis/
cd Global-GDP-Analysis/
```

**Get Dependencies**
```bash
# For Archlinux
sudo pacman -S --needed base-devel git python python-matplotlib python-pycountry

# For Ubuntu
sudo apt install -y python3-tk python3-matplotlib git curl python-is-python3 python3
```

**Setup the Environment**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv venv
uv pip install squarify wordcloud inquirerpy pycountry
```

**Run the Dashboard**
```bash
uv run main.py
```

---

## External Tools

We have made use of the following external tools, to improve the smoothness of our workflows:
1. [ruff](https://github.com/astral-sh/ruff) (for formatting python code)
2. [matplotlib](https://matplotlib.org/) (for visualization and plotting graphs)
3. [squarify](https://github.com/laserson/squarify) (for visualization of `treemap` graph variant)
4. [wordcloud](https://github.com/amueller/word_cloud) (for visualization of `wordcloud` graph variant)
5. [InquirerPy](https://github.com/kazhala/InquirerPy) (for building the TUI used in dashboard prompt)
6. [pycountry](https://github.com/pycountry/pycountry) (to identify between currently recognized countries of the world)
