# Project Charter

## Project Name

University Research Analytics Dashboard

## Project Purpose

The purpose of this project is to design and develop a business intelligence solution that helps university research leadership analyze extramural research proposals, awards, sponsors, colleges, departments, and funding trends.

The project simulates the type of analytics and reporting work performed by an Office of the Vice President for Research.

## Business Problem

Research activity may be distributed across multiple systems, spreadsheets, and administrative reports. This can make it difficult for university leadership to obtain a consistent view of proposal activity, award performance, sponsor relationships, and organizational trends.

The proposed solution will centralize research data into an analytical dataset and provide an interactive Tableau dashboard for strategic and operational decision-making.

## Project Objectives

1. Create a realistic synthetic dataset representing university research proposals and awards.
2. Clean, validate, and transform the data using Python.
3. Define and document research performance metrics.
4. Create SQL queries for repeatable analysis.
5. Build an interactive Tableau dashboard.
6. Produce metadata, technical documentation, and user guidance.
7. Export a professional PDF dashboard sample for job applications.
8. Publish the complete project in a GitHub repository.

## Primary Stakeholders

- Vice President for Research
- Associate Vice Presidents for Research
- College Deans
- Department Chairs
- Research Administrators
- Sponsored Projects Staff
- Grant Support Personnel
- Institutional Data Analysts

## Stakeholder Needs

### Research Leadership

Needs a high-level view of total funding, proposal activity, award rates, sponsor performance, and year-over-year trends.

### College and Department Leadership

Needs the ability to compare proposal volume, success rates, and funding performance across organizational units.

### Research Administrators

Needs detailed information about proposal statuses, decision timelines, sponsor activity, and operational workload.

### Data Analysts

Needs consistent data definitions, documented calculations, reusable queries, and a reliable analytical dataset.

## Project Scope

### In Scope

- Synthetic research proposal data
- Synthetic award data
- Funding trend analysis
- Sponsor analysis
- College and department comparisons
- Proposal success rates
- Award decision timelines
- Tableau dashboard development
- Python data generation and cleaning
- SQL analysis
- Metadata documentation
- Technical documentation
- User guide
- Dashboard PDF export

### Out of Scope

- Real university data
- Personally identifiable information
- Student data
- Production authentication
- Live university system integrations
- Automated enterprise scheduling
- Predictive award decisions
- Real institutional benchmarking

## Major Deliverables

- Project charter
- Business requirements document
- Synthetic raw dataset
- Clean analytical dataset
- Data dictionary
- Python scripts
- SQL scripts
- Tableau workbook
- Dashboard screenshots
- Dashboard PDF
- Technical documentation
- User guide
- Data flow diagram
- Executive summary

## Assumptions

- All data is synthetic.
- The university fiscal year begins on July 1.
- Each proposal belongs to one college and one department.
- Each proposal has one primary principal investigator.
- Awarded proposals contain an award amount.
- Declined and pending proposals do not contain an award amount.
- Sponsor names will be standardized during data cleaning.
- Proposal success rate will exclude pending proposals.

## Constraints

- Tableau Public may be used for dashboard development.
- No confidential or institutional data will be included.
- Data refreshes will be demonstrated manually.
- The project will simulate a production analytics solution but will not be deployed into an enterprise environment.
- The dashboard must fit on a standard laptop screen.

## Risks

- Synthetic data may not reflect every real-world research administration scenario.
- Unrealistic distributions could reduce the credibility of the analysis.
- Inconsistent metric definitions could create incorrect dashboard results.
- Poor dashboard design could make the information difficult to interpret.

## Risk Mitigation

- Use documented assumptions.
- Validate calculated metrics using both Python and SQL.
- Apply realistic distributions to proposal statuses, funding amounts, sponsors, and departments.
- Reconcile Tableau calculations with summary outputs.
- Document limitations clearly.

## Success Criteria

The project will be considered successful when:

- The dataset contains realistic research proposal records.
- Data quality checks identify no critical errors.
- Key performance indicators are clearly defined.
- Python, SQL, and Tableau results reconcile.
- Dashboard filters work correctly.
- The dashboard supports executive and operational analysis.
- Documentation explains the data, calculations, workflow, and limitations.
- A polished dashboard PDF can be submitted as a professional work sample.