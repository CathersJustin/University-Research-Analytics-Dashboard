"""
Clean, validate, and enrich the synthetic research proposal dataset.

Input:
    data/raw/research_proposals_raw.csv

Output:
    data/processed/research_proposals_clean.csv
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Repository paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "research_proposals_raw.csv"
)

PROCESSED_DIRECTORY = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    PROCESSED_DIRECTORY
    / "research_proposals_clean.csv"
)

VALIDATION_REPORT_FILE = (
    PROCESSED_DIRECTORY
    / "data_validation_report.txt"
)


# ---------------------------------------------------------
# Approved values
# ---------------------------------------------------------

APPROVED_PROPOSAL_STATUSES = {
    "Awarded",
    "Declined",
    "Pending",
    "Withdrawn",
}

APPROVED_PROPOSAL_TYPES = {
    "New",
    "Renewal",
    "Resubmission",
    "Supplement",
}

APPROVED_SPONSOR_TYPES = {
    "Federal",
    "State",
    "Industry",
    "Foundation",
    "Nonprofit",
    "Internal",
}

COLLEGES_AND_DEPARTMENTS = {
    "College of Engineering": {
        "Computer Science",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
    },
    "College of Medicine": {
        "Biomedical Sciences",
        "Neuroscience",
        "Internal Medicine",
        "Public Health",
    },
    "College of Arts and Sciences": {
        "Biology",
        "Chemistry",
        "Physics",
        "Psychology",
    },
    "College of Agriculture": {
        "Plant and Soil Sciences",
        "Animal Sciences",
        "Agricultural Economics",
    },
    "College of Education": {
        "Educational Leadership",
        "Curriculum and Instruction",
    },
    "College of Business": {
        "Finance",
        "Management",
        "Marketing",
    },
}

REQUIRED_COLUMNS = [
    "proposal_id",
    "principal_investigator_id",
    "principal_investigator_name",
    "college",
    "department",
    "research_area",
    "sponsor",
    "sponsor_type",
    "proposal_type",
    "proposal_status",
    "submission_date",
    "requested_amount",
    "award_amount",
    "direct_costs",
    "indirect_costs",
]

DATE_COLUMNS = [
    "submission_date",
    "decision_date",
    "project_start_date",
    "project_end_date",
]

NUMERIC_COLUMNS = [
    "requested_amount",
    "award_amount",
    "direct_costs",
    "indirect_costs",
]


# ---------------------------------------------------------
# File loading
# ---------------------------------------------------------

def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Read the raw proposal dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw dataset was not found:\n{file_path}\n\n"
            "Run generate_dataset.py before running this script."
        )

    dataset = pd.read_csv(file_path)

    print(f"Loaded {len(dataset):,} raw records.")

    return dataset


# ---------------------------------------------------------
# Structural validation
# ---------------------------------------------------------

def validate_required_columns(dataset: pd.DataFrame) -> None:
    """Confirm that all required columns exist."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataset.columns
    ]

    if missing_columns:
        raise ValueError(
            "The raw dataset is missing required columns: "
            + ", ".join(missing_columns)
        )


def convert_data_types(dataset: pd.DataFrame) -> pd.DataFrame:
    """Convert date and numeric fields to appropriate data types."""

    cleaned = dataset.copy()

    for column in DATE_COLUMNS:
        cleaned[column] = pd.to_datetime(
            cleaned[column],
            errors="coerce",
        )

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce",
        )

    return cleaned


# ---------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------

def clean_text_fields(dataset: pd.DataFrame) -> pd.DataFrame:
    """Remove extra spaces and standardize text formatting."""

    cleaned = dataset.copy()

    text_columns = cleaned.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned[column] = (
            cleaned[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    return cleaned


# ---------------------------------------------------------
# Calculated date fields
# ---------------------------------------------------------

def calculate_fiscal_year(
    submission_date: pd.Timestamp,
) -> int | None:
    """
    Calculate fiscal year assuming the fiscal year begins July 1.

    July through December are assigned to the following fiscal year.
    January through June remain in the current calendar year.
    """

    if pd.isna(submission_date):
        return None

    if submission_date.month >= 7:
        return submission_date.year + 1

    return submission_date.year


def calculate_fiscal_quarter(
    submission_date: pd.Timestamp,
) -> str | None:
    """Calculate the university fiscal quarter."""

    if pd.isna(submission_date):
        return None

    month = submission_date.month
    fiscal_year = calculate_fiscal_year(submission_date)

    if month in {7, 8, 9}:
        quarter = "Q1"
    elif month in {10, 11, 12}:
        quarter = "Q2"
    elif month in {1, 2, 3}:
        quarter = "Q3"
    else:
        quarter = "Q4"

    return f"FY{fiscal_year} {quarter}"


def add_calculated_fields(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Add fiscal, calendar, and duration fields."""

    cleaned = dataset.copy()

    cleaned["fiscal_year"] = (
        cleaned["submission_date"]
        .apply(calculate_fiscal_year)
        .astype("Int64")
    )

    cleaned["fiscal_quarter"] = (
        cleaned["submission_date"]
        .apply(calculate_fiscal_quarter)
        .astype("string")
    )

    cleaned["submission_year"] = (
        cleaned["submission_date"]
        .dt.year
        .astype("Int64")
    )

    cleaned["submission_month"] = (
        cleaned["submission_date"]
        .dt.month_name()
        .astype("string")
    )

    cleaned["submission_month_number"] = (
        cleaned["submission_date"]
        .dt.month
        .astype("Int64")
    )

    cleaned["decision_year"] = (
        cleaned["decision_date"]
        .dt.year
        .astype("Int64")
    )

    cleaned["decision_month"] = (
        cleaned["decision_date"]
        .dt.month_name()
        .astype("string")
    )

    cleaned["decision_time_days"] = (
        cleaned["decision_date"]
        - cleaned["submission_date"]
    ).dt.days.astype("Int64")

    cleaned["project_duration_days"] = (
        cleaned["project_end_date"]
        - cleaned["project_start_date"]
    ).dt.days.astype("Int64")

    cleaned["decided_flag"] = (
        cleaned["proposal_status"]
        .isin({"Awarded", "Declined"})
        .astype(int)
    )

    cleaned["awarded_flag"] = (
        cleaned["proposal_status"]
        .eq("Awarded")
        .astype(int)
    )

    cleaned["pending_flag"] = (
        cleaned["proposal_status"]
        .eq("Pending")
        .astype(int)
    )

    return cleaned


# ---------------------------------------------------------
# Data-quality validation
# ---------------------------------------------------------

def collect_validation_results(
    dataset: pd.DataFrame,
) -> dict[str, int]:
    """Calculate the number of records violating each quality rule."""

    awarded_mask = dataset["proposal_status"].eq("Awarded")
    non_awarded_mask = ~awarded_mask

    invalid_college_department = dataset.apply(
        lambda row: (
            row["college"] not in COLLEGES_AND_DEPARTMENTS
            or row["department"]
            not in COLLEGES_AND_DEPARTMENTS.get(
                row["college"],
                set(),
            )
        ),
        axis=1,
    )

    calculated_award_total = (
        dataset["direct_costs"]
        + dataset["indirect_costs"]
    ).round(2)

    reported_award_total = dataset["award_amount"].round(2)

    validation_results = {
        "duplicate_proposal_ids": int(
            dataset["proposal_id"].duplicated().sum()
        ),
        "missing_required_values": int(
            dataset[REQUIRED_COLUMNS].isna().any(axis=1).sum()
        ),
        "invalid_proposal_statuses": int(
            (~dataset["proposal_status"].isin(
                APPROVED_PROPOSAL_STATUSES
            )).sum()
        ),
        "invalid_proposal_types": int(
            (~dataset["proposal_type"].isin(
                APPROVED_PROPOSAL_TYPES
            )).sum()
        ),
        "invalid_sponsor_types": int(
            (~dataset["sponsor_type"].isin(
                APPROVED_SPONSOR_TYPES
            )).sum()
        ),
        "invalid_college_department_combinations": int(
            invalid_college_department.sum()
        ),
        "nonpositive_requested_amounts": int(
            (dataset["requested_amount"] <= 0).sum()
        ),
        "awarded_records_without_positive_award": int(
            (
                awarded_mask
                & (dataset["award_amount"] <= 0)
            ).sum()
        ),
        "non_awarded_records_with_award_amount": int(
            (
                non_awarded_mask
                & (dataset["award_amount"] != 0)
            ).sum()
        ),
        "cost_reconciliation_errors": int(
            (
                calculated_award_total
                != reported_award_total
            ).sum()
        ),
        "decision_dates_before_submission": int(
            (
                dataset["decision_date"].notna()
                & (
                    dataset["decision_date"]
                    < dataset["submission_date"]
                )
            ).sum()
        ),
        "project_end_dates_before_start": int(
            (
                dataset["project_end_date"].notna()
                & dataset["project_start_date"].notna()
                & (
                    dataset["project_end_date"]
                    < dataset["project_start_date"]
                )
            ).sum()
        ),
        "pending_records_with_decision_dates": int(
            (
                dataset["proposal_status"].eq("Pending")
                & dataset["decision_date"].notna()
            ).sum()
        ),
        "decided_records_without_decision_dates": int(
            (
                dataset["proposal_status"].isin(
                    {"Awarded", "Declined"}
                )
                & dataset["decision_date"].isna()
            ).sum()
        ),
        "awarded_records_without_project_dates": int(
            (
                awarded_mask
                & (
                    dataset["project_start_date"].isna()
                    | dataset["project_end_date"].isna()
                )
            ).sum()
        ),
    }

    return validation_results


def write_validation_report(
    validation_results: dict[str, int],
    output_path: Path,
    record_count: int,
) -> None:
    """Write a text report containing data-quality results."""

    total_errors = sum(validation_results.values())

    report_lines = [
        "University Research Analytics Dashboard",
        "Data Validation Report",
        "=" * 45,
        "",
        f"Records evaluated: {record_count:,}",
        f"Total validation errors: {total_errors:,}",
        "",
        "Validation results:",
    ]

    for rule, error_count in validation_results.items():
        readable_rule = rule.replace("_", " ").title()

        report_lines.append(
            f"- {readable_rule}: {error_count:,}"
        )

    report_lines.extend(
        [
            "",
            (
                "Validation status: PASSED"
                if total_errors == 0
                else "Validation status: FAILED"
            ),
        ]
    )

    output_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )


def raise_if_validation_fails(
    validation_results: dict[str, int],
) -> None:
    """Stop processing if any validation rule fails."""

    failed_rules = {
        rule: count
        for rule, count in validation_results.items()
        if count > 0
    }

    if not failed_rules:
        return

    failure_details = "\n".join(
        f"- {rule}: {count}"
        for rule, count in failed_rules.items()
    )

    raise ValueError(
        "Data validation failed:\n"
        f"{failure_details}\n\n"
        "Review the validation report for details."
    )


# ---------------------------------------------------------
# Output formatting
# ---------------------------------------------------------

def arrange_output_columns(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Arrange fields into a Tableau-friendly order."""

    output_columns = [
        "proposal_id",
        "principal_investigator_id",
        "principal_investigator_name",
        "college",
        "department",
        "research_area",
        "sponsor",
        "sponsor_type",
        "proposal_type",
        "proposal_status",
        "submission_date",
        "decision_date",
        "project_start_date",
        "project_end_date",
        "requested_amount",
        "award_amount",
        "direct_costs",
        "indirect_costs",
        "fiscal_year",
        "fiscal_quarter",
        "submission_year",
        "submission_month",
        "submission_month_number",
        "decision_year",
        "decision_month",
        "decision_time_days",
        "project_duration_days",
        "decided_flag",
        "awarded_flag",
        "pending_flag",
    ]

    return dataset[output_columns].sort_values(
        by=["submission_date", "proposal_id"]
    )


def export_clean_data(
    dataset: pd.DataFrame,
    output_path: Path,
) -> None:
    """Export the cleaned dataset to CSV."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset.to_csv(
        output_path,
        index=False,
        date_format="%Y-%m-%d",
    )


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main() -> None:
    """Run the complete cleaning and validation pipeline."""

    print("Loading raw dataset...")

    raw_dataset = load_raw_data(RAW_FILE)

    validate_required_columns(raw_dataset)

    print("Converting data types...")

    cleaned_dataset = convert_data_types(raw_dataset)

    print("Cleaning text fields...")

    cleaned_dataset = clean_text_fields(cleaned_dataset)

    print("Adding calculated fields...")

    cleaned_dataset = add_calculated_fields(
        cleaned_dataset
    )

    print("Validating data quality...")

    validation_results = collect_validation_results(
        cleaned_dataset
    )

    PROCESSED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_validation_report(
        validation_results,
        VALIDATION_REPORT_FILE,
        len(cleaned_dataset),
    )

    raise_if_validation_fails(validation_results)

    cleaned_dataset = arrange_output_columns(
        cleaned_dataset
    )

    export_clean_data(
        cleaned_dataset,
        OUTPUT_FILE,
    )

    print("\nData cleaning completed successfully.")
    print(f"Clean dataset: {OUTPUT_FILE}")
    print(f"Validation report: {VALIDATION_REPORT_FILE}")
    print(f"Records exported: {len(cleaned_dataset):,}")
    print(f"Columns exported: {len(cleaned_dataset.columns)}")

    print("\nFiscal year totals:")
    print(
        cleaned_dataset["fiscal_year"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nProposal status totals:")
    print(
        cleaned_dataset["proposal_status"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()