"""
Create and populate the SQLite database for the
University Research Analytics Dashboard.

Inputs:
    data/processed/research_proposals_clean.csv
    sql/CreateTables.sql

Output:
    data/processed/university_research_analytics.db
"""

from pathlib import Path
import sqlite3

import pandas as pd


# ---------------------------------------------------------
# Repository paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLEAN_DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "research_proposals_clean.csv"
)

SCHEMA_FILE = (
    PROJECT_ROOT
    / "sql"
    / "CreateTables.sql"
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "university_research_analytics.db"
)


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

def load_clean_data(file_path: Path) -> pd.DataFrame:
    """Load the clean analytical dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Clean dataset was not found:\n{file_path}\n\n"
            "Run clean_data.py before running this script."
        )

    dataset = pd.read_csv(
        file_path,
        dtype={
            "proposal_id": "string",
            "principal_investigator_id": "string",
        },
    )

    print(f"Loaded {len(dataset):,} clean records.")

    return dataset


def read_schema(file_path: Path) -> str:
    """Read the SQL schema file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Schema file was not found:\n{file_path}"
        )

    return file_path.read_text(encoding="utf-8")


# ---------------------------------------------------------
# Dimension table creation
# ---------------------------------------------------------

def create_colleges(dataset: pd.DataFrame) -> pd.DataFrame:
    """Create the college dimension table."""

    colleges = (
        dataset[["college"]]
        .drop_duplicates()
        .sort_values("college")
        .reset_index(drop=True)
    )

    colleges.insert(
        0,
        "college_id",
        range(1, len(colleges) + 1),
    )

    colleges = colleges.rename(
        columns={"college": "college_name"}
    )

    return colleges


def create_departments(
    dataset: pd.DataFrame,
    colleges: pd.DataFrame,
) -> pd.DataFrame:
    """Create the department dimension table."""

    departments = (
        dataset[["college", "department"]]
        .drop_duplicates()
        .sort_values(["college", "department"])
        .reset_index(drop=True)
    )

    departments = departments.merge(
        colleges,
        left_on="college",
        right_on="college_name",
        how="left",
        validate="many_to_one",
    )

    departments.insert(
        0,
        "department_id",
        range(1, len(departments) + 1),
    )

    departments = departments.rename(
        columns={"department": "department_name"}
    )

    return departments[
        [
            "department_id",
            "department_name",
            "college_id",
        ]
    ]


def create_investigators(
    dataset: pd.DataFrame,
    departments: pd.DataFrame,
    colleges: pd.DataFrame,
) -> pd.DataFrame:
    """Create the principal-investigator dimension table."""

    department_lookup = departments.merge(
        colleges,
        on="college_id",
        how="left",
        validate="many_to_one",
    )

    investigators = (
        dataset[
            [
                "principal_investigator_id",
                "principal_investigator_name",
                "college",
                "department",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    investigators = investigators.merge(
        department_lookup,
        left_on=["college", "department"],
        right_on=["college_name", "department_name"],
        how="left",
        validate="many_to_one",
    )

    return investigators[
        [
            "principal_investigator_id",
            "principal_investigator_name",
            "department_id",
        ]
    ]


def create_sponsors(dataset: pd.DataFrame) -> pd.DataFrame:
    """Create the sponsor dimension table."""

    sponsors = (
        dataset[["sponsor", "sponsor_type"]]
        .drop_duplicates()
        .sort_values(["sponsor_type", "sponsor"])
        .reset_index(drop=True)
    )

    sponsors.insert(
        0,
        "sponsor_id",
        range(1, len(sponsors) + 1),
    )

    sponsors = sponsors.rename(
        columns={"sponsor": "sponsor_name"}
    )

    return sponsors


def create_research_areas(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Create the research-area dimension table."""

    research_areas = (
        dataset[["research_area"]]
        .drop_duplicates()
        .sort_values("research_area")
        .reset_index(drop=True)
    )

    research_areas.insert(
        0,
        "research_area_id",
        range(1, len(research_areas) + 1),
    )

    research_areas = research_areas.rename(
        columns={
            "research_area": "research_area_name"
        }
    )

    return research_areas


# ---------------------------------------------------------
# Fact table creation
# ---------------------------------------------------------

def create_proposals(
    dataset: pd.DataFrame,
    sponsors: pd.DataFrame,
    research_areas: pd.DataFrame,
) -> pd.DataFrame:
    """Create the normalized proposal fact table."""

    proposals = dataset.merge(
        sponsors,
        left_on=["sponsor", "sponsor_type"],
        right_on=["sponsor_name", "sponsor_type"],
        how="left",
        validate="many_to_one",
    )

    proposals = proposals.merge(
        research_areas,
        left_on="research_area",
        right_on="research_area_name",
        how="left",
        validate="many_to_one",
    )

    proposal_columns = [
        "proposal_id",
        "principal_investigator_id",
        "sponsor_id",
        "research_area_id",
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

    return proposals[proposal_columns]


# ---------------------------------------------------------
# Database creation
# ---------------------------------------------------------

def create_database(
    database_path: Path,
    schema_sql: str,
) -> sqlite3.Connection:
    """Create the SQLite database and execute the schema."""

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if database_path.exists():
        database_path.unlink()

    connection = sqlite3.connect(database_path)

    connection.execute("PRAGMA foreign_keys = ON;")
    connection.executescript(schema_sql)

    return connection


def insert_dataframe(
    connection: sqlite3.Connection,
    table_name: str,
    dataset: pd.DataFrame,
) -> None:
    """Insert a DataFrame into an existing SQL table."""

    dataset.to_sql(
        table_name,
        connection,
        if_exists="append",
        index=False,
    )

    print(
        f"Inserted {len(dataset):,} rows into "
        f"{table_name}."
    )


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_row_counts(
    connection: sqlite3.Connection,
    expected_counts: dict[str, int],
) -> None:
    """Compare expected and actual SQL row counts."""

    print("\nValidating table row counts...")

    for table_name, expected_count in expected_counts.items():
        query = f"SELECT COUNT(*) FROM {table_name};"

        actual_count = connection.execute(
            query
        ).fetchone()[0]

        print(
            f"{table_name}: "
            f"expected {expected_count:,}, "
            f"found {actual_count:,}"
        )

        if actual_count != expected_count:
            raise ValueError(
                f"Row-count validation failed for "
                f"{table_name}."
            )


def validate_foreign_keys(
    connection: sqlite3.Connection,
) -> None:
    """Run SQLite foreign-key validation."""

    violations = connection.execute(
        "PRAGMA foreign_key_check;"
    ).fetchall()

    if violations:
        raise ValueError(
            "Foreign-key validation failed:\n"
            + "\n".join(str(row) for row in violations)
        )

    print("Foreign-key validation passed.")


def validate_executive_metrics(
    connection: sqlite3.Connection,
    dataset: pd.DataFrame,
) -> None:
    """Compare important SQL and pandas totals."""

    sql_result = connection.execute(
        """
        SELECT
            COUNT(DISTINCT proposal_id),
            ROUND(SUM(requested_amount), 2),
            ROUND(SUM(award_amount), 2),
            SUM(awarded_flag),
            SUM(decided_flag),
            SUM(pending_flag)
        FROM proposals;
        """
    ).fetchone()

    pandas_result = (
        dataset["proposal_id"].nunique(),
        round(dataset["requested_amount"].sum(), 2),
        round(dataset["award_amount"].sum(), 2),
        int(dataset["awarded_flag"].sum()),
        int(dataset["decided_flag"].sum()),
        int(dataset["pending_flag"].sum()),
    )

    labels = [
        "Total proposals",
        "Total requested funding",
        "Total awarded funding",
        "Awarded proposals",
        "Decided proposals",
        "Pending proposals",
    ]

    print("\nValidating executive metrics...")

    for label, sql_value, pandas_value in zip(
        labels,
        sql_result,
        pandas_result,
    ):
        print(
            f"{label}: SQL={sql_value}, "
            f"Python={pandas_value}"
        )

        if sql_value != pandas_value:
            raise ValueError(
                f"Metric validation failed for {label}."
            )

    print("Executive metric validation passed.")


def display_database_summary(
    connection: sqlite3.Connection,
) -> None:
    """Display a concise database summary."""

    summary_query = """
    SELECT
        COUNT(DISTINCT proposal_id)
            AS total_proposals,

        ROUND(
            SUM(requested_amount),
            2
        ) AS total_requested_funding,

        ROUND(
            SUM(award_amount),
            2
        ) AS total_awarded_funding,

        SUM(awarded_flag)
            AS awarded_proposals,

        SUM(decided_flag)
            AS decided_proposals,

        ROUND(
            100.0 * SUM(awarded_flag)
            / NULLIF(SUM(decided_flag), 0),
            2
        ) AS proposal_success_rate

    FROM proposals;
    """

    summary = pd.read_sql_query(
        summary_query,
        connection,
    )

    print("\nDatabase executive summary:")
    print(summary.to_string(index=False))


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main() -> None:
    """Create, populate, and validate the database."""

    print("Loading cleaned proposal data...")

    dataset = load_clean_data(CLEAN_DATA_FILE)

    print("Creating normalized dimension tables...")

    colleges = create_colleges(dataset)

    departments = create_departments(
        dataset,
        colleges,
    )

    investigators = create_investigators(
        dataset,
        departments,
        colleges,
    )

    sponsors = create_sponsors(dataset)

    research_areas = create_research_areas(dataset)

    proposals = create_proposals(
        dataset,
        sponsors,
        research_areas,
    )

    print("Reading SQL schema...")

    schema_sql = read_schema(SCHEMA_FILE)

    print("Creating SQLite database...")

    connection = create_database(
        DATABASE_FILE,
        schema_sql,
    )

    try:
        insert_dataframe(
            connection,
            "colleges",
            colleges,
        )

        insert_dataframe(
            connection,
            "departments",
            departments,
        )

        insert_dataframe(
            connection,
            "principal_investigators",
            investigators,
        )

        insert_dataframe(
            connection,
            "sponsors",
            sponsors,
        )

        insert_dataframe(
            connection,
            "research_areas",
            research_areas,
        )

        insert_dataframe(
            connection,
            "proposals",
            proposals,
        )

        connection.commit()

        expected_counts = {
            "colleges": len(colleges),
            "departments": len(departments),
            "principal_investigators": len(
                investigators
            ),
            "sponsors": len(sponsors),
            "research_areas": len(research_areas),
            "proposals": len(proposals),
        }

        validate_row_counts(
            connection,
            expected_counts,
        )

        validate_foreign_keys(connection)

        validate_executive_metrics(
            connection,
            dataset,
        )

        display_database_summary(connection)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    print("\nDatabase creation completed successfully.")
    print(f"Database file: {DATABASE_FILE}")


if __name__ == "__main__":
    main()