# AI Programming Foundations Project: Swiss LEI Data Workflow

## Project Description
In this project I build a reproducible data workflow for the Legal Entity
Identifier (LEI) data published by GLEIF, filtered down to entities registered
in Switzerland. A Jupyter notebook loads the prepared dataset, cleans it,
explores it and creates a few visualizations. I will reuse the cleaned dataset
in the later capstone projects, where the topic will be entity matching for
compliance checks.

## What Was Built
- A download script (`download_golden_copy.py`) that fetches the latest
  GLEIF Golden Copy file (around 500 MB).
- A preprocessing script (`prepare_dataset.py`) that reproduces the dataset
  subset (`lei_switzerland.csv`, around 28k rows x 12 columns) from the official
  GLEIF source.

## Dataset
GLEIF LEI Golden Copy (Level 1, "Who is who"), filtered to Swiss entities:
https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy

The filtered dataset `lei_switzerland.csv` is included in this repository.

To recreate it from scratch, either download the Golden Copy CSV file
manually from the link above, or let the download script fetch the latest
file for you:
```
python download_golden_copy.py
python prepare_dataset.py
```
Note: GLEIF publishes a new Golden Copy every day, so a fresh download can
give slightly different numbers than the snapshot used in this project.

## How to Run the Project
TODO

## Dependencies
`requirements.txt` was created inside the project's own virtual
environment with:
```
pip freeze > requirements.txt
```

## Connection to Future AI Work
I picked this dataset with the later capstone projects in mind. The cleaned
dataset will be the input for an entity-matching machine learning project,
and the normalized company names can serve as training data for a deep
learning model for name matching. The small workflow functions from this
project could later also be used as tools by an agent that runs compliance
checks automatically.

## Reflections
TODO
