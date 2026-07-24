"""
Perform exploratory data analysis for the
University Research Analytics Dashboard.

Input:
    data/processed/research_proposals_clean.csv

Outputs:
    images/proposal_status_distribution.png
    images/fiscal_year_funding_trend.png
    images/college_awarded_funding.png
    images/college_success_rate.png
    images/top_sponsors_by_funding.png
    images/research_area_awarded_funding.png
    images/decision_time_by_sponsor_type.png
    data/processed/eda_summary_statistics.csv
    docs/ExploratoryAnalysis.md
"""

from pathlib import Path

import matplotlib.pyplot as plt
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

IMAGE_DIRECTORY = PROJECT_ROOT / "images"

SUMMARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "eda_summary_statistics.csv"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "docs"
    / "ExploratoryAnalysis.md"
)


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

def load_data(file_path: Path) -> pd.DataFrame:
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

    print(f"Loaded {len(dataset):,} proposal records.")

    return dataset


# ---------------------------------------------------------
# Summary calculations
# ---------------------------------------------------------

def calculate_summary_statistics(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate high-level exploratory statistics."""

    awarded = dataset[
        dataset["proposal_status"] == "Awarded"
    ]

    decided = dataset[
        dataset["proposal_status"].isin(
            ["Awarded", "Declined"]
        )
    ]

    statistics = [
        {
            "metric": "Total Proposals",
            "value": dataset["proposal_id"].nunique(),
        },
        {
            "metric": "Total Requested Funding",
            "value": dataset["requested_amount"].sum(),
        },
        {
            "metric": "Total Awarded Funding",
            "value": dataset["award_amount"].sum(),
        },
        {
            "metric": "Awarded Proposals",
            "value": len(awarded),
        },
        {
            "metric": "Declined Proposals",
            "value": int(
                dataset["proposal_status"]
                .eq("Declined")
                .sum()
            ),
        },
        {
            "metric": "Pending Proposals",
            "value": int(
                dataset["proposal_status"]
                .eq("Pending")
                .sum()
            ),
        },
        {
            "metric": "Withdrawn Proposals",
            "value": int(
                dataset["proposal_status"]
                .eq("Withdrawn")
                .sum()
            ),
        },
        {
            "metric": "Proposal Success Rate",
            "value": (
                len(awarded) / len(decided) * 100
                if len(decided) > 0
                else 0
            ),
        },
        {
            "metric": "Average Award Amount",
            "value": awarded["award_amount"].mean(),
        },
        {
            "metric": "Median Award Amount",
            "value": awarded["award_amount"].median(),
        },
        {
            "metric": "Average Decision Time Days",
            "value": decided["decision_time_days"].mean(),
        },
        {
            "metric": "Median Decision Time Days",
            "value": decided["decision_time_days"].median(),
        },
        {
            "metric": "Active Principal Investigators",
            "value": dataset[
                "principal_investigator_id"
            ].nunique(),
        },
    ]

    summary = pd.DataFrame(statistics)

    summary["value"] = summary["value"].round(2)

    return summary


# ---------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------

def save_current_figure(
    output_path: Path,
) -> None:
    """Save and close the active matplotlib figure."""

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Created {output_path.name}")


# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

def create_status_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create proposal status distribution chart."""

    status_order = [
        "Awarded",
        "Declined",
        "Pending",
        "Withdrawn",
    ]

    status_counts = (
        dataset["proposal_status"]
        .value_counts()
        .reindex(status_order)
        .fillna(0)
    )

    plt.figure(figsize=(9, 5))

    status_counts.plot(
        kind="bar"
    )

    plt.title("Proposal Status Distribution")
    plt.xlabel("Proposal Status")
    plt.ylabel("Number of Proposals")
    plt.xticks(rotation=0)

    save_current_figure(
        IMAGE_DIRECTORY
        / "proposal_status_distribution.png"
    )


def create_fiscal_year_funding_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create awarded funding trend by fiscal year."""

    fiscal_summary = (
        dataset.groupby("fiscal_year")
        .agg(
            requested_funding=(
                "requested_amount",
                "sum",
            ),
            awarded_funding=(
                "award_amount",
                "sum",
            ),
        )
        .reset_index()
        .sort_values("fiscal_year")
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        fiscal_summary["fiscal_year"],
        fiscal_summary["requested_funding"],
        marker="o",
        label="Requested Funding",
    )

    plt.plot(
        fiscal_summary["fiscal_year"],
        fiscal_summary["awarded_funding"],
        marker="o",
        label="Awarded Funding",
    )

    plt.title("Requested and Awarded Funding by Fiscal Year")
    plt.xlabel("Fiscal Year")
    plt.ylabel("Funding Amount")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    save_current_figure(
        IMAGE_DIRECTORY
        / "fiscal_year_funding_trend.png"
    )


def create_college_funding_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create awarded funding chart by college."""

    college_funding = (
        dataset.groupby("college")["award_amount"]
        .sum()
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    college_funding.plot(
        kind="barh"
    )

    plt.title("Total Awarded Funding by College")
    plt.xlabel("Awarded Funding")
    plt.ylabel("College")

    save_current_figure(
        IMAGE_DIRECTORY
        / "college_awarded_funding.png"
    )


def create_college_success_rate_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create proposal success rate chart by college."""

    summary = (
        dataset.groupby("college")
        .agg(
            awarded_proposals=(
                "awarded_flag",
                "sum",
            ),
            decided_proposals=(
                "decided_flag",
                "sum",
            ),
        )
        .reset_index()
    )

    summary["proposal_success_rate"] = (
        summary["awarded_proposals"]
        / summary["decided_proposals"]
        * 100
    )

    summary = summary.sort_values(
        "proposal_success_rate"
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        summary["college"],
        summary["proposal_success_rate"],
    )

    plt.title("Proposal Success Rate by College")
    plt.xlabel("Success Rate (%)")
    plt.ylabel("College")

    save_current_figure(
        IMAGE_DIRECTORY
        / "college_success_rate.png"
    )


def create_top_sponsor_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create top sponsors by awarded funding chart."""

    sponsor_funding = (
        dataset.groupby("sponsor")["award_amount"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    plt.figure(figsize=(11, 7))

    sponsor_funding.plot(
        kind="barh"
    )

    plt.title("Top 10 Sponsors by Awarded Funding")
    plt.xlabel("Awarded Funding")
    plt.ylabel("Sponsor")

    save_current_figure(
        IMAGE_DIRECTORY
        / "top_sponsors_by_funding.png"
    )


def create_research_area_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create awarded funding chart by research area."""

    area_funding = (
        dataset.groupby("research_area")["award_amount"]
        .sum()
        .sort_values()
    )

    plt.figure(figsize=(11, 7))

    area_funding.plot(
        kind="barh"
    )

    plt.title("Awarded Funding by Research Area")
    plt.xlabel("Awarded Funding")
    plt.ylabel("Research Area")

    save_current_figure(
        IMAGE_DIRECTORY
        / "research_area_awarded_funding.png"
    )


def create_decision_time_chart(
    dataset: pd.DataFrame,
) -> None:
    """Create average decision time by sponsor type."""

    decided = dataset[
        dataset["decided_flag"] == 1
    ]

    decision_time = (
        decided.groupby("sponsor_type")[
            "decision_time_days"
        ]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(9, 6))

    decision_time.plot(
        kind="barh"
    )

    plt.title("Average Decision Time by Sponsor Type")
    plt.xlabel("Average Decision Time in Days")
    plt.ylabel("Sponsor Type")

    save_current_figure(
        IMAGE_DIRECTORY
        / "decision_time_by_sponsor_type.png"
    )


# ---------------------------------------------------------
# Insight generation
# ---------------------------------------------------------

def format_currency(value: float) -> str:
    """Format a value as U.S. currency."""

    return f"${value:,.2f}"


def calculate_insights(
    dataset: pd.DataFrame,
) -> dict[str, object]:
    """Calculate the primary insights for the written report."""

    awarded = dataset[
        dataset["proposal_status"] == "Awarded"
    ]

    decided = dataset[
        dataset["proposal_status"].isin(
            ["Awarded", "Declined"]
        )
    ]

    college_summary = (
        dataset.groupby("college")
        .agg(
            total_proposals=(
                "proposal_id",
                "nunique",
            ),
            awarded_funding=(
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
        )
        .reset_index()
    )

    college_summary["success_rate"] = (
        college_summary["awarded_proposals"]
        / college_summary["decided_proposals"]
        * 100
    )

    top_funded_college = college_summary.loc[
        college_summary["awarded_funding"].idxmax()
    ]

    highest_success_college = college_summary.loc[
        college_summary["success_rate"].idxmax()
    ]

    lowest_success_college = college_summary.loc[
        college_summary["success_rate"].idxmin()
    ]

    sponsor_summary = (
        dataset.groupby("sponsor")
        .agg(
            awarded_funding=(
                "award_amount",
                "sum",
            ),
            total_proposals=(
                "proposal_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    top_sponsor = sponsor_summary.loc[
        sponsor_summary["awarded_funding"].idxmax()
    ]

    research_area_summary = (
        dataset.groupby("research_area")
        .agg(
            awarded_funding=(
                "award_amount",
                "sum",
            ),
            total_proposals=(
                "proposal_id",
                "nunique",
            ),
        )
        .reset_index()
    )

    top_research_area = research_area_summary.loc[
        research_area_summary["awarded_funding"].idxmax()
    ]

    sponsor_type_decision_time = (
        decided.groupby("sponsor_type")[
            "decision_time_days"
        ]
        .mean()
    )

    slowest_sponsor_type = (
        sponsor_type_decision_time.idxmax()
    )

    fastest_sponsor_type = (
        sponsor_type_decision_time.idxmin()
    )

    success_rate = (
        len(awarded) / len(decided) * 100
        if len(decided) > 0
        else 0
    )

    return {
        "total_proposals": dataset[
            "proposal_id"
        ].nunique(),
        "total_requested": dataset[
            "requested_amount"
        ].sum(),
        "total_awarded": dataset[
            "award_amount"
        ].sum(),
        "success_rate": success_rate,
        "average_award": awarded[
            "award_amount"
        ].mean(),
        "average_decision_time": decided[
            "decision_time_days"
        ].mean(),
        "top_funded_college": top_funded_college[
            "college"
        ],
        "top_funded_college_amount": top_funded_college[
            "awarded_funding"
        ],
        "highest_success_college": highest_success_college[
            "college"
        ],
        "highest_success_rate": highest_success_college[
            "success_rate"
        ],
        "lowest_success_college": lowest_success_college[
            "college"
        ],
        "lowest_success_rate": lowest_success_college[
            "success_rate"
        ],
        "top_sponsor": top_sponsor["sponsor"],
        "top_sponsor_amount": top_sponsor[
            "awarded_funding"
        ],
        "top_research_area": top_research_area[
            "research_area"
        ],
        "top_research_area_amount": top_research_area[
            "awarded_funding"
        ],
        "slowest_sponsor_type": slowest_sponsor_type,
        "slowest_decision_time": (
            sponsor_type_decision_time.max()
        ),
        "fastest_sponsor_type": fastest_sponsor_type,
        "fastest_decision_time": (
            sponsor_type_decision_time.min()
        ),
    }


def write_analysis_report(
    insights: dict[str, object],
    output_path: Path,
) -> None:
    """Write the exploratory analysis report."""

    report = f"""# Exploratory Data Analysis

## Overview

This analysis evaluates synthetic university research proposal and award activity. The findings will guide the design of the Tableau dashboard.

## Executive Summary

- Total proposals analyzed: {insights["total_proposals"]:,}
- Total requested funding: {format_currency(insights["total_requested"])}
- Total awarded funding: {format_currency(insights["total_awarded"])}
- Proposal success rate: {insights["success_rate"]:.2f}%
- Average award amount: {format_currency(insights["average_award"])}
- Average sponsor decision time: {insights["average_decision_time"]:.2f} days

## Key Findings

### College Funding Performance

The college receiving the most awarded funding was **{insights["top_funded_college"]}**, with {format_currency(insights["top_funded_college_amount"])} in total awarded funding.

### College Proposal Success

The highest proposal success rate belonged to **{insights["highest_success_college"]}**, at {insights["highest_success_rate"]:.2f}%.

The lowest proposal success rate belonged to **{insights["lowest_success_college"]}**, at {insights["lowest_success_rate"]:.2f}%.

This comparison may help research leadership identify colleges that have strong activity but may benefit from additional proposal-development support.

### Sponsor Concentration

The sponsor providing the most awarded funding was **{insights["top_sponsor"]}**, with {format_currency(insights["top_sponsor_amount"])} in total awards.

Sponsor concentration should be monitored because heavy dependence on a small number of sponsors may create portfolio risk.

### Research Area Performance

The research area receiving the most awarded funding was **{insights["top_research_area"]}**, with {format_currency(insights["top_research_area_amount"])}.

This may indicate a strategic research strength or concentration of institutional expertise.

### Sponsor Decision Time

The sponsor type with the longest average decision time was **{insights["slowest_sponsor_type"]}**, averaging {insights["slowest_decision_time"]:.2f} days.

The sponsor type with the shortest average decision time was **{insights["fastest_sponsor_type"]}**, averaging {insights["fastest_decision_time"]:.2f} days.

Decision-time analysis can help research administrators set expectations and identify proposals that may require follow-up.

## Recommended Tableau Dashboard Views

### Executive Overview

- Total proposals
- Total requested funding
- Total awarded funding
- Proposal success rate
- Average award amount
- Average decision time
- Fiscal-year funding trend
- Proposal status distribution

### College and Department Analysis

- Awarded funding by college
- Success rate by college
- Department comparison table
- High-volume, low-success departments
- Principal investigator rankings

### Sponsor Analysis

- Top sponsors by awarded funding
- Success rate by sponsor
- Average decision time by sponsor type
- Sponsor concentration
- Sponsor-type filtering

### Research Portfolio Analysis

- Funding by research area
- Proposal count by research area
- Success rate by research area
- Research-area trends over time

## Limitations

- The dataset is synthetic.
- Results do not represent a real university.
- Proposal outcomes and funding values were generated using simulated distributions.
- The analysis is intended for portfolio and educational purposes.
"""

    output_path.write_text(
        report,
        encoding="utf-8",
    )


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main() -> None:
    """Run the exploratory analysis workflow."""

    dataset = load_data(INPUT_FILE)

    IMAGE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Calculating summary statistics...")

    summary_statistics = calculate_summary_statistics(
        dataset
    )

    summary_statistics.to_csv(
        SUMMARY_FILE,
        index=False,
    )

    print("Creating proposal status chart...")
    create_status_chart(dataset)

    print("Creating fiscal-year funding chart...")
    create_fiscal_year_funding_chart(dataset)

    print("Creating college funding chart...")
    create_college_funding_chart(dataset)

    print("Creating college success-rate chart...")
    create_college_success_rate_chart(dataset)

    print("Creating sponsor chart...")
    create_top_sponsor_chart(dataset)

    print("Creating research-area chart...")
    create_research_area_chart(dataset)

    print("Creating decision-time chart...")
    create_decision_time_chart(dataset)

    print("Generating written analysis...")

    insights = calculate_insights(dataset)

    write_analysis_report(
        insights,
        REPORT_FILE,
    )

    print("\nExploratory analysis completed.")
    print(f"Summary statistics: {SUMMARY_FILE}")
    print(f"Analysis report: {REPORT_FILE}")
    print(f"Charts directory: {IMAGE_DIRECTORY}")


if __name__ == "__main__":
    main()