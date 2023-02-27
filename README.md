# work-with-datasets
## About

This is small project which take dataset with client information and other with client financial information, filter data by country/countries and merge both together. Return output dataset with new column names and save logs in file.

## Getting Started

1. Clone this repo
2. Install requirements
```pip install -r requirements.txt```
3. To run tests: ```python -m pytest```

## Run App

To run help type: ```python main.py -h```

To run app for default settings (for template datasets and countries to filter): ```python main.py -d```

To run app for specific values follow this schema:

```python main.py -x <first-path> -y <second-path> -c <"first-country"> <"second-country">```

For example:
```python main.py -x dataset_one.csv -y dataset_two.csv -c "United Kingdom"```