# Generic Concurrent Real-Time Pipeline & Dashboard

## Main File:
`main.py`

## Data Path:
`data/`

## Config File:
`config.json`


## Instructions to Run:

First, unzip the code, navigate to that directory, ensure you have pip setup, and then do the following:

```bash
pip install -r requirements.txt --break-system-packages
python main.py
```


## Folder Structure
```tree
.
├── config.json
├── core
│   ├── aggregator.py
│   ├── data_processor.py
│   ├── __init__.py
│   └── protocols.py
├── data
│   ├── gdp_with_continent_filled.json
│   ├── unseen_climate_data.csv
│   └── World_Bank_Dataset.csv
├── main.py
├── plugins
│   ├── input
│   │   ├── data_loader.py
│   │   └── __init__.py
│   └── output
│       ├── chart_implementations.py
│       ├── chart_writer.py
│       ├── console_writer.py
│       ├── __init__.py
│       ├── pipeline_monitor.py
│       ├── pipeline_telemetry.py
│       ├── protocols.py
│       └── web
│           ├── __init__.py
│           ├── server.py
│           ├── static
│           │   └── style.css
│           └── templates
│               └── index.html
├── README.md
├── readme.txt
├── requirements.txt
└── stream
    ├── __init__.py
    └── Stream.py
```
