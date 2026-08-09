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
- A Jupyter notebook (`data_workflow.ipynb`) with the whole workflow: loading
  the dataset, two documented cleaning functions, a reusable EDA function,
  three visualizations and a written summary of the findings.

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
1. Clone this repository.
2. Create and activate a virtual environment (Python 3.12 or newer):
   ```
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Start Jupyter:
   ```
   jupyter notebook
   ```
5. Open `data_workflow.ipynb` and run all cells
   (Kernel > Restart Kernel and Run All Cells).

The dataset `lei_switzerland.csv` is already part of the repository, so
no download is needed to run the notebook.

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

### Bias Awareness: Where could poor data cleaning introduce bias?
The biggest risk in this project is the name normalization. If I normalize
too aggressively, different companies get merged into one, and if I
normalize too little, the same company is counted several times. My
duplicate check showed both sides of this: after normalization 65
additional rows repeat a name that already exists, but some of these
matches (like generic fund names) probably belong to different entities. A real duplicate check would also have to
compare the legal form and the address, the name alone is only a first
hint. The effect is also not equal for everyone,
because umlauts and French or Italian accents are only common in some
regions of Switzerland, so a bad cleaning rule would distort exactly those
regions. On top of that, no cleaning can fix the selection bias of the
dataset itself. It only contains companies that needed an LEI, so it never
represents all Swiss companies.

### How would this workflow change for a machine learning project?
The cleaning functions would become a fixed preprocessing pipeline with
train/test awareness, so the normalization rules would be built on training
data only. I would add encodings for the categorical columns (legal form,
registration status) and turn the data quality checks into automated tests
that stop the pipeline when something looks wrong. The EDA results would
directly guide the setup: with 54% of the entities in one legal form and
27% lapsed registrations, I would have to make sure that the small groups
do not get lost when splitting the data into training and test sets. I
also could not judge a model by accuracy alone: if the task is to predict
lapsed versus not lapsed, a model that always says "not lapsed" would
already look 73% correct without learning anything.

### How does this prepare for neural network projects?
The normalized name column is exactly the input that a name-matching model
needs: multilingual company names with a consistent and reproducible
preprocessing. The 209 rows whose normalized name already appears in an
earlier row are a natural starting point for building training pairs. The committed CSV
preserves the exact snapshot I analyzed, and the scripts document how it
was built, so I can prepare a newer Golden Copy in the same way. For
comparing model runs against each other I would always work with such a
fixed snapshot.

### What is the agentic automation potential?
Every step in this workflow is already a small, documented function for
downloading, filtering, cleaning and summarizing the data. These are
exactly the kind of tools an agent can call. A due diligence agent could
refresh the dataset with the download script, run the cleaning and the
explore function as a data quality check, and raise an alarm when something
changes suddenly, for example the lapsed rate of a legal form. Since I work
on the LEI system professionally, this is not a theoretical idea for me, it
is the direction this field is actually moving.
