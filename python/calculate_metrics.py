"""
Calculate executive KPIs and summary tables for the
University Research Analytics Dashboard.

Input:
    data/processed/research_proposals_clean.csv

Outputs:
    data/processed/executive_kpis.csv
    data/processed/fiscal_year_summary.csv
    data/processed/college_summary.csv
    data/processed/sponsor_summary.csv
    data/processed/research_area_summary.csv
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Repository paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "research_proposals_clean.csv"
)

OUTPUT_DIRECTORY = PROJECT_ROOT / "data" / "processed"

EXECUTIVE_KPI_FILE = (
    OUTPUT_DIRECTORY / "executive_kpis.csv"
)

FISCAL_YEAR_SUMMARY_FILE = (
    OUTPUT_DIRECTORY / "fiscal_year_summary.csv"
)

COLLEGE_SUMMARY_FILE = (
    OUTPUT_DIRECTORY / "college_summary.csv"
)

SPONSOR_SUMMARY_FILE = (
    OUTPUT_DIRECTORY / "sponsor_summary.csv"
)

RESEARCH_AREA_SUMMARY_FILE = (
    OUTPUT_DIRECTORY / "research_area_summary.csv"
)


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

def load_clean_data(file_path: Path) -> pd.DataFrame:
    """Load the cleaned proposal dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Clean dataset was not found:\n{file_path}\n\n"
            "Run clean_data.py before running this script."
        )

    dataset = pd.read_csv(
        file_path,
        parse_dates=[
            "submission_date",
            "decision_date",
            "project_start_date",
            "project_end_date",
        ],
    )

    print(f"Loaded {len(dataset):,} clean records.")

    return dataset


# ---------------------------------------------------------
# Helper calculations
# ---------------------------------------------------------

def safe_percentage(
    numerator: float,
    denominator: float,
) -> float:
    """Calculate a percentage without dividing by zero."""

    if denominator == 0:
        return 0.0

    return round((numerator / denominator) * 100, 2)


def calculate_year_over_year_growth(
    current_value: float,
    previous_value: float,
) -> float:
    """Calculate year-over-year percentage growth."""

    if previous_value == 0:
        return 0.0

    return round(
        ((current_value - previous_value) / previous_value) * 100,
        2,
    )


# ---------------------------------------------------------
# Executive KPIs
# ---------------------------------------------------------

def calculate_executive_kpis(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate project-level executive KPIs."""

    awarded = dataset[
        dataset["proposal_status"] == "Awarded"
    ]

    decided = dataset[
        dataset["proposal_status"].isin(
            ["Awarded", "Declined"]
        )
    ]

    total_proposals = dataset["proposal_id"].nunique()

    total_requested_funding = dataset[
        "requested_amount"
    ].sum()

    total_awarded_funding = awarded[
        "award_amount"
    ].sum()

    awarded_proposal_count = awarded[
        "proposal_id"
    ].nunique()

    decided_proposal_count = decided[
        "proposal_id"
    ].nunique()

    pending_proposal_count = dataset.loc[
        dataset["proposal_status"] == "Pending",
        "proposal_id",
    ].nunique()

    withdrawn_proposal_count = dataset.loc[
        dataset["proposal_status"] == "Withdrawn",
        "proposal_id",
    ].nunique()

    proposal_success_rate = safe_percentage(
        awarded_proposal_count,
        decided_proposal_count,
    )

    average_award_amount = (
        awarded["award_amount"].mean()
        if not awarded.empty
        else 0
    )

    median_award_amount = (
        awarded["award_amount"].median()
        if not awarded.empty
        else 0
    )

    average_decision_time = (
        decided["decision_time_days"].mean()
        if not decided.empty
        else 0
    )

    active_principal_investigators = dataset[
        "principal_investigator_id"
    ].nunique()

    executive_kpis = pd.DataFrame(
        [
            {
                "metric_name": "Total Proposals",
                "metric_value": total_proposals,
                "metric_format": "Whole Number",
            },
            {
                "metric_name": "Total Requested Funding",
                "metric_value": round(
                    total_requested_funding,
                    2,
                ),
                "metric_format": "Currency",
            },
            {
                "metric_name": "Total Awarded Funding",
                "metric_value": round(
                    total_awarded_funding,
                    2,
                ),
                "metric_format": "Currency",
            },
            {
                "metric_name": "Awarded Proposal Count",
                "metric_value": awarded_proposal_count,
                "metric_format": "Whole Number",
            },
            {
                "metric_name": "Decided Proposal Count",
                "metric_value": decided_proposal_count,
                "metric_format": "Whole Number",
            },
            {
                "metric_name": "Pending Proposal Count",
                "metric_value": pending_proposal_count,
                "metric_format": "Whole Number",
            },
            {
                "metric_name": "Withdrawn Proposal Count",
                "metric_value": withdrawn_proposal_count,
                "metric_format": "Whole Number",
            },
            {
                "metric_name": "Proposal Success Rate",
                "metric_value": proposal_success_rate,
                "metric_format": "Percentage",
            },
            {
                "metric_name": "Average Award Amount",
                "metric_value": round(
                    average_award_amount,
                    2,
                ),
                "metric_format": "Currency",
            },
            {
                "metric_name": "Median Award Amount",
                "metric_value": round(
                    median_award_amount,
                    2,
                ),
                "metric_format": "Currency",
            },
            {
                "metric_name": "Average Decision Time",
                "metric_value": round(
                    average_decision_time,
                    2,
                ),
                "metric_format": "Days",
            },
            {
                "metric_name": "Active Principal Investigators",
                "metric_value": active_principal_investigators,
                "metric_format": "Whole Number",
            },
        ]
    )

    return executive_kpis


# ---------------------------------------------------------
# Fiscal year summary
# ---------------------------------------------------------

def calculate_fiscal_year_summary(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Create fiscal-year performance summaries."""

    summary = (
        dataset.groupby("fiscal_year", dropna=False)
        .agg(
            total_proposals=(
                "proposal_id",
                "nunique",
            ),
            total_requested_funding=(
                "requested_amount",
                "sum",
            ),
            total_awarded_funding=(
                "award_amount",
                "sum",
            ),
            awarded_proposals=(
                "awarded_flag",
                "sum",
            ),
            decided_proposals=(
                "decided_flag",
                "sum",
            ),
            pending_proposals=(
                "pending_flag",
                "sum",
            ),
            average_decision_time_days=(
                "decision_time_days",
                "mean",
            ),
            active_principal_investigators=(
                "principal_investigator_id",
                "nunique",
            ),
        )
        .reset_index()
        .sort_values("fiscal_year")
    )

    summary["proposal_success_rate"] = summary.apply(
        lambda row: safe_percentage(
            row["awarded_proposals"],
            row["decided_proposals"],
        ),
        axis=1,
    )

    summary["average_award_amount"] = summary.apply(
        lambda row: (
            row["total_awarded_funding"]
            / row["awarded_proposals"]
            if row["awarded_proposals"] > 0
            else 0
        ),
        axis=1,
    )

    previous_awarded_funding = summary[
        "total_awarded_funding"
    ].shift(1)

    summary["year_over_year_award_growth"] = [
        0.0
        if pd.isna(previous)
        else calculate_year_over_year_growth(
            current,
            previous,
        )
        for current, previous in zip(
            summary["total_awarded_funding"],
            previous_awarded_funding,
        )
    ]

    money_columns = [
        "total_requested_funding",
        "total_awarded_funding",
        "average_award_amount",
    ]

    for column in money_columns:
        summary[column] = summary[column].round(2)

    summary["average_decision_time_days"] = (
        summary["average_decision_time_days"].round(2)
    )

    return summary


# ---------------------------------------------------------
# Grouped summaries
# ---------------------------------------------------------

def create_group_summary(
    dataset: pd.DataFrame,
    group_columns: list[str],
) -> pd.DataFrame:
    """Create a reusable grouped performance summary."""

    summary = (
        dataset.groupby(
            group_columns,
            dropna=False,
        )
        .agg(
            total_proposals=(
                "proposal_id",
                "nunique",
            ),
            total_requested_funding=(
                "requested_amount",
                "sum",
            ),
            total_awarded_funding=(
                "award_amount",
                "sum",
            ),
            awarded_proposals=(
                "awarded_flag",
                "sum",
            ),
            decided_proposals=(
                "decided_flag",
                "sum",
            ),
            pending_proposals=(
                "pending_flag",
                "sum",
            ),
            average_decision_time_days=(
                "decision_time_days",
                "mean",
            ),
            active_principal_investigators=(
                "principal_investigator_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    summary["proposal_success_rate"] = summary.apply(
        lambda row: safe_percentage(
            row["awarded_proposals"],
            row["decided_proposals"],
        ),
        axis=1,
    )

    summary["average_award_amount"] = summary.apply(
        lambda row: (
            row["total_awarded_funding"]
            / row["awarded_proposals"]
            if row["awarded_proposals"] > 0
            else 0
        ),
        axis=1,
    )

    money_columns = [
        "total_requested_funding",
        "total_awarded_funding",
        "average_award_amount",
    ]

    for column in money_columns:
        summary[column] = summary[column].round(2)

    summary["average_decision_time_days"] = (
        summary["average_decision_time_days"].round(2)
    )

    return summary.sort_values(
        "total_awarded_funding",
        ascending=False,
    )


def calculate_college_summary(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Create college-level metrics."""

    return create_group_summary(
        dataset,
        ["college"],
    )


def calculate_sponsor_summary(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Create sponsor-level metrics."""

    return create_group_summary(
        dataset,
        ["sponsor_type", "sponsor"],
    )


def calculate_research_area_summary(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Create research-area metrics."""

    return create_group_summary(
        dataset,
        ["research_area"],
    )


# ---------------------------------------------------------
# Export
# ---------------------------------------------------------

def export_dataframe(
    dataset: pd.DataFrame,
    output_path: Path,
) -> None:
    """Export a DataFrame to CSV."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset.to_csv(
        output_path,
        index=False,
    )


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main() -> None:
    """Run the complete metric-calculation workflow."""

    print("Loading cleaned dataset...")

    dataset = load_clean_data(INPUT_FILE)

    print("Calculating executive KPIs...")

    executive_kpis = calculate_executive_kpis(
        dataset
    )

    print("Calculating fiscal-year summary...")

    fiscal_year_summary = (
        calculate_fiscal_year_summary(dataset)
    )

    print("Calculating college summary...")

    college_summary = calculate_college_summary(
        dataset
    )

    print("Calculating sponsor summary...")

    sponsor_summary = calculate_sponsor_summary(
        dataset
    )

    print("Calculating research-area summary...")

    research_area_summary = (
        calculate_research_area_summary(dataset)
    )

    export_dataframe(
        executive_kpis,
        EXECUTIVE_KPI_FILE,
    )

    export_dataframe(
        fiscal_year_summary,
        FISCAL_YEAR_SUMMARY_FILE,
    )

    export_dataframe(
        college_summary,
        COLLEGE_SUMMARY_FILE,
    )

    export_dataframe(
        sponsor_summary,
        SPONSOR_SUMMARY_FILE,
    )

    export_dataframe(
        research_area_summary,
        RESEARCH_AREA_SUMMARY_FILE,
    )

    print("\nMetric calculation completed successfully.")

    print("\nExecutive KPI output:")
    print(EXECUTIVE_KPI_FILE)

    print("\nFiscal-year summary output:")
    print(FISCAL_YEAR_SUMMARY_FILE)

    print("\nCollege summary output:")
    print(COLLEGE_SUMMARY_FILE)

    print("\nSponsor summary output:")
    print(SPONSOR_SUMMARY_FILE)

    print("\nResearch-area summary output:")
    print(RESEARCH_AREA_SUMMARY_FILE)

    print("\nExecutive KPIs:")
    print(executive_kpis.to_string(index=False))


if __name__ == "__main__":
    main()