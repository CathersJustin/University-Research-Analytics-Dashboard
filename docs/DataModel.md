# Data Model

## Overview

The University Research Analytics Dashboard will initially use a flattened analytical dataset for Tableau reporting.

The source data will also be represented conceptually as a relational model to demonstrate database design and SQL skills.

---

## Conceptual Entities

The model contains the following primary entities:

- Proposals
- Principal Investigators
- Colleges
- Departments
- Sponsors
- Research Areas

---

## Entity Relationships

### College and Department

- One college may contain many departments.
- Each department belongs to one college.

Relationship:

```text
College 1 ---- Many Departments
```

### Department and Principal Investigator

- One department may contain many principal investigators.
- Each principal investigator belongs to one department.

Relationship:

```text
Department 1 ---- Many Principal Investigators
```

### Principal Investigator and Proposal

- One principal investigator may submit many proposals.
- Each proposal has one primary principal investigator.

Relationship:

```text
Principal Investigator 1 ---- Many Proposals
```

### Sponsor and Proposal

- One sponsor may receive many proposals.
- Each proposal is submitted to one sponsor.

Relationship:

```text
Sponsor 1 ---- Many Proposals
```

### Research Area and Proposal

- One research area may be associated with many proposals.
- Each proposal has one primary research area.

Relationship:

```text
Research Area 1 ---- Many Proposals
```

---

## Relational Tables

### colleges

| Column | Type | Key |
|---|---|---|
| college_id | Integer | Primary Key |
| college_name | Text | Unique |

### departments

| Column | Type | Key |
|---|---|---|
| department_id | Integer | Primary Key |
| department_name | Text | |
| college_id | Integer | Foreign Key |

### principal_investigators

| Column | Type | Key |
|---|---|---|
| principal_investigator_id | Text | Primary Key |
| principal_investigator_name | Text | |
| department_id | Integer | Foreign Key |

### sponsors

| Column | Type | Key |
|---|---|---|
| sponsor_id | Integer | Primary Key |
| sponsor_name | Text | Unique |
| sponsor_type | Text | |

### research_areas

| Column | Type | Key |
|---|---|---|
| research_area_id | Integer | Primary Key |
| research_area_name | Text | Unique |

### proposals

| Column | Type | Key |
|---|---|---|
| proposal_id | Text | Primary Key |
| principal_investigator_id | Text | Foreign Key |
| sponsor_id | Integer | Foreign Key |
| research_area_id | Integer | Foreign Key |
| proposal_type | Text | |
| proposal_status | Text | |
| submission_date | Date | |
| decision_date | Date | |
| project_start_date | Date | |
| project_end_date | Date | |
| requested_amount | Decimal | |
| award_amount | Decimal | |
| direct_costs | Decimal | |
| indirect_costs | Decimal | |

---

## Tableau Analytical Dataset

For Tableau, the relational data will be combined into a flattened table named:

```text
research_proposals_clean.csv
```

The flattened dataset will include descriptive fields such as:

- College
- Department
- Principal investigator
- Sponsor
- Sponsor type
- Research area
- Proposal status
- Proposal type
- Dates
- Funding amounts
- Calculated time fields

This structure will make dashboard development easier while the SQL scripts preserve the normalized relational design.

---

## Data Flow

```text
Synthetic Data Generator
        |
        v
Raw CSV Dataset
        |
        v
Python Cleaning and Validation
        |
        v
Clean Analytical CSV
        |
        +-------------------+
        |                   |
        v                   v
SQL Database           Tableau Dashboard
        |
        v
Validation Queries
```