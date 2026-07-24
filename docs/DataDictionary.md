# Data Dictionary

## Overview

This document defines the fields used in the University Research Analytics Dashboard dataset.

The dataset represents synthetic university research proposals, awards, principal investigators, departments, colleges, sponsors, and funding activity.

---

## Proposal Dataset

| Field Name | Data Type | Description | Example | Required |
|---|---|---|---|---|
| proposal_id | Text | Unique identifier assigned to each proposal | PROP-000001 | Yes |
| principal_investigator_id | Text | Unique identifier assigned to the principal investigator | PI-0042 | Yes |
| principal_investigator_name | Text | Full name of the principal investigator | Dr. Jordan Smith | Yes |
| college | Text | College associated with the proposal | College of Engineering | Yes |
| department | Text | Department associated with the proposal | Computer Science | Yes |
| research_area | Text | Primary research category | Artificial Intelligence | Yes |
| sponsor | Text | Organization receiving the proposal | National Science Foundation | Yes |
| sponsor_type | Text | Classification of the sponsor | Federal | Yes |
| proposal_type | Text | Type of proposal submission | New | Yes |
| proposal_status | Text | Current or final proposal outcome | Awarded | Yes |
| submission_date | Date | Date the proposal was submitted | 2025-02-15 | Yes |
| decision_date | Date | Date the sponsor issued a decision | 2025-06-20 | No |
| project_start_date | Date | Planned or actual project start date | 2025-08-01 | No |
| project_end_date | Date | Planned or actual project end date | 2028-07-31 | No |
| requested_amount | Decimal | Total funding requested | 425000.00 | Yes |
| award_amount | Decimal | Total amount awarded | 375000.00 | Yes |
| direct_costs | Decimal | Portion of award assigned to direct project costs | 300000.00 | Yes |
| indirect_costs | Decimal | Portion of award assigned to indirect costs | 75000.00 | Yes |
| fiscal_year | Integer | University fiscal year derived from submission date | 2025 | Yes |
| fiscal_quarter | Text | Fiscal quarter derived from submission date | FY2025 Q3 | Yes |
| submission_year | Integer | Calendar year of submission | 2025 | Yes |
| submission_month | Text | Calendar month of submission | February | Yes |
| decision_time_days | Integer | Number of days between submission and decision | 125 | No |

---

## Approved Proposal Status Values

| Status | Definition |
|---|---|
| Awarded | Sponsor approved the proposal and issued funding |
| Declined | Sponsor rejected the proposal |
| Pending | Sponsor decision has not yet been received |
| Withdrawn | Proposal was withdrawn before a final sponsor decision |

---

## Approved Proposal Type Values

| Proposal Type | Definition |
|---|---|
| New | New proposal submitted for funding |
| Renewal | Request to continue an existing funded project |
| Resubmission | Revised proposal submitted after a previous decline |
| Supplement | Request for additional funding under an existing award |

---

## Approved Sponsor Type Values

| Sponsor Type | Definition |
|---|---|
| Federal | United States federal government agency |
| State | State government organization |
| Industry | Private commercial organization |
| Foundation | Private nonprofit foundation |
| Nonprofit | Nonprofit organization other than a foundation |
| Internal | University-funded research program |

---

## Colleges and Departments

| College | Department |
|---|---|
| College of Engineering | Computer Science |
| College of Engineering | Electrical Engineering |
| College of Engineering | Mechanical Engineering |
| College of Engineering | Civil Engineering |
| College of Medicine | Biomedical Sciences |
| College of Medicine | Neuroscience |
| College of Medicine | Internal Medicine |
| College of Medicine | Public Health |
| College of Arts and Sciences | Biology |
| College of Arts and Sciences | Chemistry |
| College of Arts and Sciences | Physics |
| College of Arts and Sciences | Psychology |
| College of Agriculture | Plant and Soil Sciences |
| College of Agriculture | Animal Sciences |
| College of Agriculture | Agricultural Economics |
| College of Education | Educational Leadership |
| College of Education | Curriculum and Instruction |
| College of Business | Finance |
| College of Business | Management |
| College of Business | Marketing |

---

## Research Areas

| Research Area | Description |
|---|---|
| Artificial Intelligence | Machine learning, deep learning, automation, and intelligent systems |
| Data Science | Statistical modeling, analytics, and computational methods |
| Biomedical Research | Disease mechanisms, diagnostics, and treatment research |
| Neuroscience | Brain, nervous system, behavior, and cognition |
| Public Health | Population health, epidemiology, and health policy |
| Renewable Energy | Solar, wind, storage, and sustainable energy |
| Advanced Manufacturing | Robotics, materials, and industrial systems |
| Environmental Science | Climate, ecosystems, pollution, and sustainability |
| Agriculture | Crop science, livestock, food systems, and agricultural technology |
| Education | Teaching, learning, leadership, and educational policy |
| Social and Behavioral Science | Human behavior, communities, and social systems |
| Business and Economics | Finance, management, markets, and economic development |

---

## Calculated Fields

### Fiscal Year

The university fiscal year begins July 1.

- July through December belong to the following fiscal year.
- January through June belong to the current calendar year.

Example:

- Submission date: October 10, 2024
- Fiscal year: 2025

### Fiscal Quarter

| Calendar Months | Fiscal Quarter |
|---|---|
| July through September | Q1 |
| October through December | Q2 |
| January through March | Q3 |
| April through June | Q4 |

Example output:

```text
FY2025 Q2