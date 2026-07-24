# Technical Documentation

## Solution Overview

The University Research Analytics Dashboard is an end-to-end analytics project that uses Python, SQL, and Tableau.

The solution will generate synthetic proposal data, clean and validate it, store it in a relational database structure, and present the results through interactive dashboards.

## Technology Stack

- Python
- pandas
- NumPy
- Faker
- SQL
- Tableau
- Git
- GitHub
- Markdown

## Planned Processing Workflow

1. Generate synthetic proposal records.
2. Export the raw dataset to `data/raw`.
3. Read the raw file using pandas.
4. Validate required fields.
5. Standardize text and dates.
6. Calculate fiscal year and fiscal quarter.
7. Calculate decision time.
8. Validate funding calculations.
9. Export the cleaned dataset to `data/processed`.
10. Build Tableau dashboards.

## Planned Python Files

- generate_dataset.py
- clean_data.py
- calculate_metrics.py

## Planned SQL Files

- CreateTables.sql
- SampleQueries.sql

## Planned Outputs

- research_proposals_raw.csv
- research_proposals_clean.csv
- Tableau Dashboard
- Dashboard PDF
- Dashboard Screenshots

## Validation

The project will validate:

- Duplicate proposals
- Missing values
- Date consistency
- Award calculations
- Direct + Indirect costs
- KPI reconciliation between Python, SQL, and Tableau