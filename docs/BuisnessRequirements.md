# Business Requirements Document

## 1. Project Overview

The University Research Analytics Dashboard will provide an interactive reporting solution for analyzing synthetic extramural research proposal and award data.

The dashboard is intended to support research leadership, college administrators, department leadership, research administrators, and data analysts.

## 2. Business Need

Research leaders need timely and accurate information to understand:

- Proposal activity
- Award performance
- Funding trends
- Sponsor relationships
- College and department performance
- Decision timelines
- Research portfolio composition

A centralized dashboard will reduce reliance on static spreadsheets and allow users to explore data through filters, drill-downs, and self-service visualizations.

## 3. Business Questions

The dashboard should answer the following questions:

1. How many proposals were submitted?
2. How much funding was requested?
3. How much funding was awarded?
4. What percentage of decided proposals were awarded?
5. Which colleges receive the most funding?
6. Which departments submit the most proposals?
7. Which departments have strong proposal volume but low success rates?
8. Which sponsors provide the most funding?
9. Which sponsor types have the highest success rates?
10. Which research areas receive the most funding?
11. How has awarded funding changed over time?
12. How long does it take sponsors to make decisions?
13. Which principal investigators receive the most funding?
14. How do colleges compare in proposal volume, success rate, and award value?
15. Which research areas are growing or declining?

## 4. Functional Requirements

### FR-01 Executive KPI Summary

The dashboard shall display:

- Total proposals
- Total requested funding
- Total awarded funding
- Awarded proposal count
- Proposal success rate
- Average award amount
- Average decision time

### FR-02 Time Trend Analysis

The dashboard shall display research activity by:

- Fiscal year
- Fiscal quarter
- Calendar year
- Submission month
- Decision month

### FR-03 Organizational Analysis

The dashboard shall support analysis by:

- College
- Department
- Principal investigator

### FR-04 Sponsor Analysis

The dashboard shall display:

- Funding by sponsor
- Proposal count by sponsor
- Award count by sponsor
- Success rate by sponsor
- Average award amount by sponsor
- Funding by sponsor type

### FR-05 Research Area Analysis

The dashboard shall allow users to compare:

- Proposal volume by research area
- Awarded funding by research area
- Success rate by research area
- Funding trends by research area

### FR-06 Proposal Status Analysis

The dashboard shall display proposal counts by:

- Awarded
- Declined
- Pending
- Withdrawn

### FR-07 Interactive Filters

Users shall be able to filter by:

- Fiscal year
- College
- Department
- Sponsor
- Sponsor type
- Research area
- Proposal type
- Proposal status
- Principal investigator

### FR-08 Drill-Down

Users shall be able to move from:

- College to department
- Sponsor type to sponsor
- Fiscal year to quarter and month

### FR-09 Tooltips

Charts shall provide contextual information through Tableau tooltips.

### FR-10 Dynamic Titles

Dashboard titles shall update based on active filter selections.

### FR-11 Dashboard Navigation

Users shall be able to navigate between:

- Executive Overview
- College and Department Analysis
- Sponsor Analysis
- Proposal Detail

### FR-12 Export

Users shall be able to export dashboard views to:

- PDF
- Image
- Crosstab, where supported

## 5. Data Requirements

The analytical dataset shall include:

- Proposal ID
- Principal investigator ID
- Principal investigator name
- College
- Department
- Research area
- Sponsor
- Sponsor type
- Proposal type
- Proposal status
- Submission date
- Decision date
- Project start date
- Project end date
- Requested amount
- Award amount
- Direct costs
- Indirect costs
- Fiscal year
- Fiscal quarter
- Decision time in days

## 6. KPI Definitions

### Total Proposals

Count of unique proposal IDs.

### Total Requested Funding

Sum of requested amounts across all proposals.

### Total Awarded Funding

Sum of award amounts for proposals with an Awarded status.

### Awarded Proposal Count

Count of unique proposals with an Awarded status.

### Decided Proposal Count

Count of proposals with an Awarded or Declined status.

Pending and withdrawn proposals are excluded.

### Proposal Success Rate

Awarded proposal count divided by decided proposal count.

### Average Award Amount

Total awarded funding divided by awarded proposal count.

### Median Award Amount

Median award amount among awarded proposals.

### Average Decision Time

Average number of days between submission date and decision date for decided proposals.

### Year-over-Year Award Growth

Percentage change in total awarded funding from the previous fiscal year.

### Active Principal Investigators

Count of unique principal investigators with at least one proposal during the selected period.

## 7. Data Quality Requirements

- Proposal IDs must be unique.
- Required fields must not be blank.
- Awarded proposals must have an award amount greater than zero.
- Declined, pending, and withdrawn proposals must have an award amount of zero.
- Decision dates must not occur before submission dates.
- Project end dates must not occur before project start dates.
- Requested amounts must be greater than zero.
- College and department combinations must be valid.
- Sponsor names must use consistent formatting.
- Fiscal year values must be derived consistently.
- Proposal status values must use an approved list.

## 8. Nonfunctional Requirements

- Dashboard visuals must be readable on a standard laptop.
- Formatting must be consistent across all views.
- Calculations must reconcile with Python and SQL validation results.
- The dashboard must use clear labels and plain-language definitions.
- Filters must update all relevant visualizations.
- Documentation must identify assumptions and limitations.
- No real or confidential data may be used.
- Repository files must follow a clear naming convention.
- The Tableau workbook must be packaged for portability.

## 9. Acceptance Criteria

The dashboard will be accepted when:

- KPI values match validated Python and SQL calculations.
- All interactive filters work correctly.
- Drill-down paths operate as designed.
- No awarded proposal has a missing or zero award amount.
- Pending and declined proposals do not contribute to awarded funding.
- Fiscal year calculations are consistent.
- Data fields and calculations are documented.
- Dashboard views can be exported to PDF.
- The final PDF is readable and suitable for a job application.