# Global GDP Analysis

A simple python dataset visualizer and analyzer that uses the World Bank GDP report dataset.

---

## Rationale

Made for our SDA semester project, the major purpose of this project is to showcase strong functional programming concepts, and clean architecture. The program is modular, and configuration based. Showcasing the power and succinctness of the Functional Programming Paradigm. Documentation is a key aspect of the codebase.

---

## Project Structure
```bash
.
├── config.json                     # User Configuration File
├── main.py                         # Entry Point
├── assets
│   └── World_Bank_Dataset.csv      # Data-set
├── helpers
│   ├── chart_implementations.py    # Graphing Functions
│   └── prompt_handler.py           # Dashboard-menu Handler
└── src
    ├── dashboard.py                # Dashboard Controller
    ├── data_loader.py              # Loads data from Data-set
    └── data_processor.py           # Sanitizes, filters, processes data
```

---

## How to Run

### Clone this repository
``` bash
git clone https://github.com/OrionShinesBright/Global-GDP-Analysis/
cd Global-GDP-Analysis/
```

### Install the dependencies for your system
**For Arch Linux**
```bash
sudo pacman -S --needed python python-matplotlib python-pycountry
yay -S python-squarify python-wordcloud python-inquirerpy
```
**For Ubuntu**
```bash
sudo apt install -y curl
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv venv
uv pip install squarify wordcloud inquirerpy pycountry
sudo apt install -y python3-tk python3-matplotlib
```

### Run the Dashboard
**For Arch Linux**
```bash
python main.py
```
**For Ubuntu**
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
