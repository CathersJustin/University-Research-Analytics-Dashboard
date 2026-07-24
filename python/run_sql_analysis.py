"""
Run analytical SQL queries and reconcile SQL results with
the Python summary outputs.

Inputs:
    data/processed/university_research_analytics.db
    data/processed/executive_kpis.csv
    data/processed/fiscal_year_summary.csv
    data/processed/college_summary.csv
    data/processed/sponsor_summary.csv
    data/processed/research_area_summary.csv

Outputs:
    data/processed/sql_outputs/sql_executive_summary.csv
    data/processed/sql_outputs/sql_fiscal_year_summary.csv
    data/processed/sql_outputs/sql_college_summary.csv
    data/processed/sql_outputs/sql_department_summary.csv
    data/processed/sql_outputs/sql_sponsor_summary.csv
    data/processed/sql_outputs/sql_research_area_summary.csv
    data/processed/sql_outputs/sql_top_investigators.csv
    data/processed/sql_outputs/sql_status_summary.csv
    data/processed/sql_outputs/sql_reconciliation_report.csv
    data/processed/sql_outputs/sql_reconciliation_report.txt
"""

from pathlib import Path
import sqlite3

import pandas as pd


# ---------------------------------------------------------
# Repository paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIRECTORY = PROJECT_ROOT / "data" / "processed"

DATABASE_FILE = (
    PROCESSED_DIRECTORY
    / "university_research_analytics.db"
)

OUTPUT_DIRECTORY = (
    PROCESSED_DIRECTORY
    / "sql_outputs"
)

PYTHON_EXECUTIVE_KPI_FILE = (
    PROCESSED_DIRECTORY
    / "executive_kpis.csv"
)

PYTHON_FISCAL_YEAR_FILE = (
    PROCESSED_DIRECTORY
    / "fiscal_year_summary.csv"
)

PYTHON_COLLEGE_FILE = (
    PROCESSED_DIRECTORY
    / "college_summary.csv"
)

PYTHON_SPONSOR_FILE = (
    PROCESSED_DIRECTORY
    / "sponsor_summary.csv"
)

PYTHON_RESEARCH_AREA_FILE = (
    PROCESSED_DIRECTORY
    / "research_area_summary.csv"
)


# ---------------------------------------------------------
# SQL queries
# ---------------------------------------------------------

EXECUTIVE_SUMMARY_QUERY = """
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
        AS awarded_proposal_count,

    SUM(decided_flag)
        AS decided_proposal_count,

    SUM(pending_flag)
        AS pending_proposal_count,

    SUM(
        CASE
            WHEN proposal_status = 'Withdrawn'
            THEN 1
            ELSE 0
        END
    ) AS withdrawn_proposal_count,

    ROUND(
        100.0
        * SUM(awarded_flag)
        / NULLIF(SUM(decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        AVG(
            CASE
                WHEN proposal_status = 'Awarded'
                THEN award_amount
            END
        ),
        2
    ) AS average_award_amount,

    ROUND(
        AVG(
            CASE
                WHEN proposal_status = 'Awarded'
                THEN award_amount
            END
        ),
        2
    ) AS mean_award_amount,

    ROUND(
        AVG(
            CASE
                WHEN decided_flag = 1
                THEN decision_time_days
            END
        ),
        2
    ) AS average_decision_time,

    COUNT(
        DISTINCT principal_investigator_id
    ) AS active_principal_investigators

FROM proposals;
"""


STATUS_SUMMARY_QUERY = """
SELECT
    proposal_status,

    COUNT(*) AS proposal_count,

    ROUND(
        100.0 * COUNT(*)
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_proposals

FROM proposals

GROUP BY proposal_status

ORDER BY proposal_count DESC;
"""


FISCAL_YEAR_SUMMARY_QUERY = """
SELECT
    fiscal_year,

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

    SUM(pending_flag)
        AS pending_proposals,

    ROUND(
        AVG(decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT principal_investigator_id
    ) AS active_principal_investigators,

    ROUND(
        100.0
        * SUM(awarded_flag)
        / NULLIF(SUM(decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        SUM(award_amount)
        / NULLIF(SUM(awarded_flag), 0),
        2
    ) AS average_award_amount

FROM proposals

GROUP BY fiscal_year

ORDER BY fiscal_year;
"""


COLLEGE_SUMMARY_QUERY = """
SELECT
    c.college_name AS college,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    ROUND(
        SUM(p.requested_amount),
        2
    ) AS total_requested_funding,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    SUM(p.pending_flag)
        AS pending_proposals,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT p.principal_investigator_id
    ) AS active_principal_investigators,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        SUM(p.award_amount)
        / NULLIF(SUM(p.awarded_flag), 0),
        2
    ) AS average_award_amount

FROM proposals AS p

INNER JOIN principal_investigators AS pi
    ON p.principal_investigator_id
       = pi.principal_investigator_id

INNER JOIN departments AS d
    ON pi.department_id = d.department_id

INNER JOIN colleges AS c
    ON d.college_id = c.college_id

GROUP BY c.college_name

ORDER BY total_awarded_funding DESC;
"""


DEPARTMENT_SUMMARY_QUERY = """
SELECT
    c.college_name AS college,
    d.department_name AS department,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    ROUND(
        SUM(p.requested_amount),
        2
    ) AS total_requested_funding,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    SUM(p.pending_flag)
        AS pending_proposals,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT p.principal_investigator_id
    ) AS active_principal_investigators,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        SUM(p.award_amount)
        / NULLIF(SUM(p.awarded_flag), 0),
        2
    ) AS average_award_amount

FROM proposals AS p

INNER JOIN principal_investigators AS pi
    ON p.principal_investigator_id
       = pi.principal_investigator_id

INNER JOIN departments AS d
    ON pi.department_id = d.department_id

INNER JOIN colleges AS c
    ON d.college_id = c.college_id

GROUP BY
    c.college_name,
    d.department_name

ORDER BY total_awarded_funding DESC;
"""


SPONSOR_SUMMARY_QUERY = """
SELECT
    s.sponsor_type,
    s.sponsor_name AS sponsor,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    ROUND(
        SUM(p.requested_amount),
        2
    ) AS total_requested_funding,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    SUM(p.pending_flag)
        AS pending_proposals,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT p.principal_investigator_id
    ) AS active_principal_investigators,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        SUM(p.award_amount)
        / NULLIF(SUM(p.awarded_flag), 0),
        2
    ) AS average_award_amount

FROM proposals AS p

INNER JOIN sponsors AS s
    ON p.sponsor_id = s.sponsor_id

GROUP BY
    s.sponsor_type,
    s.sponsor_name

ORDER BY total_awarded_funding DESC;
"""


RESEARCH_AREA_SUMMARY_QUERY = """
SELECT
    ra.research_area_name AS research_area,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    ROUND(
        SUM(p.requested_amount),
        2
    ) AS total_requested_funding,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    SUM(p.pending_flag)
        AS pending_proposals,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT p.principal_investigator_id
    ) AS active_principal_investigators,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        SUM(p.award_amount)
        / NULLIF(SUM(p.awarded_flag), 0),
        2
    ) AS average_award_amount

FROM proposals AS p

INNER JOIN research_areas AS ra
    ON p.research_area_id
       = ra.research_area_id

GROUP BY ra.research_area_name

ORDER BY total_awarded_funding DESC;
"""


TOP_INVESTIGATORS_QUERY = """
SELECT
    pi.principal_investigator_id,
    pi.principal_investigator_name,

    c.college_name AS college,
    d.department_name AS department,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate

FROM proposals AS p

INNER JOIN principal_investigators AS pi
    ON p.principal_investigator_id
       = pi.principal_investigator_id

INNER JOIN departments AS d
    ON pi.department_id = d.department_id

INNER JOIN colleges AS c
    ON d.college_id = c.college_id

GROUP BY
    pi.principal_investigator_id,
    pi.principal_investigator_name,
    c.college_name,
    d.department_name

ORDER BY total_awarded_funding DESC

LIMIT 20;
"""


# ---------------------------------------------------------
# File validation
# ---------------------------------------------------------

def validate_input_files() -> None:
    """Confirm that all required files exist."""

    required_files = [
        DATABASE_FILE,
        PYTHON_EXECUTIVE_KPI_FILE,
        PYTHON_FISCAL_YEAR_FILE,
        PYTHON_COLLEGE_FILE,
        PYTHON_SPONSOR_FILE,
        PYTHON_RESEARCH_AREA_FILE,
    ]

    missing_files = [
        file_path
        for file_path in required_files
        if not file_path.exists()
    ]

    if missing_files:
        missing_text = "\n".join(
            str(file_path)
            for file_path in missing_files
        )

        raise FileNotFoundError(
            "The following required files were not found:\n"
            f"{missing_text}"
        )


# ---------------------------------------------------------
# SQL execution
# ---------------------------------------------------------

def execute_query(
    connection: sqlite3.Connection,
    query: str,
) -> pd.DataFrame:
    """Execute a SQL query and return a DataFrame."""

    return pd.read_sql_query(
        query,
        connection,
    )


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

    print(
        f"Exported {len(dataset):,} rows to "
        f"{output_path.name}"
    )


# ---------------------------------------------------------
# Reconciliation helpers
# ---------------------------------------------------------

def convert_python_kpis_to_row(
    file_path: Path,
) -> pd.DataFrame:
    """Convert the vertical Python KPI file into one row."""

    kpis = pd.read_csv(file_path)

    metric_lookup = dict(
        zip(
            kpis["metric_name"],
            kpis["metric_value"],
        )
    )

    result = pd.DataFrame(
        [
            {
                "total_proposals": metric_lookup[
                    "Total Proposals"
                ],
                "total_requested_funding": metric_lookup[
                    "Total Requested Funding"
                ],
                "total_awarded_funding": metric_lookup[
                    "Total Awarded Funding"
                ],
                "awarded_proposal_count": metric_lookup[
                    "Awarded Proposal Count"
                ],
                "decided_proposal_count": metric_lookup[
                    "Decided Proposal Count"
                ],
                "pending_proposal_count": metric_lookup[
                    "Pending Proposal Count"
                ],
                "withdrawn_proposal_count": metric_lookup[
                    "Withdrawn Proposal Count"
                ],
                "proposal_success_rate": metric_lookup[
                    "Proposal Success Rate"
                ],
                "average_award_amount": metric_lookup[
                    "Average Award Amount"
                ],
                "average_decision_time": metric_lookup[
                    "Average Decision Time"
                ],
                "active_principal_investigators": (
                    metric_lookup[
                        "Active Principal Investigators"
                    ]
                ),
            }
        ]
    )

    return result


def compare_values(
    comparison_name: str,
    key_value: str,
    metric_name: str,
    python_value: object,
    sql_value: object,
    tolerance: float = 0.01,
) -> dict[str, object]:
    """Compare Python and SQL values."""

    python_missing = pd.isna(python_value)
    sql_missing = pd.isna(sql_value)

    if python_missing and sql_missing:
        matches = True
        difference = 0.0

    elif python_missing or sql_missing:
        matches = False
        difference = None

    else:
        try:
            python_number = float(python_value)
            sql_number = float(sql_value)

            difference = round(
                sql_number - python_number,
                4,
            )

            matches = abs(difference) <= tolerance

        except (TypeError, ValueError):
            difference = None
            matches = str(python_value) == str(sql_value)

    return {
        "comparison": comparison_name,
        "key": key_value,
        "metric": metric_name,
        "python_value": python_value,
        "sql_value": sql_value,
        "difference": difference,
        "status": "PASS" if matches else "FAIL",
    }


def reconcile_single_row(
    comparison_name: str,
    python_data: pd.DataFrame,
    sql_data: pd.DataFrame,
    metric_columns: list[str],
) -> list[dict[str, object]]:
    """Compare two single-row summary tables."""

    results = []

    for metric in metric_columns:
        results.append(
            compare_values(
                comparison_name=comparison_name,
                key_value="All Records",
                metric_name=metric,
                python_value=python_data.iloc[0][metric],
                sql_value=sql_data.iloc[0][metric],
            )
        )

    return results


def reconcile_grouped_data(
    comparison_name: str,
    python_data: pd.DataFrame,
    sql_data: pd.DataFrame,
    key_columns: list[str],
    metric_columns: list[str],
) -> list[dict[str, object]]:
    """Compare grouped Python and SQL summary tables."""

    merged = python_data.merge(
        sql_data,
        on=key_columns,
        how="outer",
        suffixes=("_python", "_sql"),
        indicator=True,
    )

    results = []

    for _, row in merged.iterrows():
        key_value = " | ".join(
            str(row[column])
            for column in key_columns
        )

        if row["_merge"] != "both":
            results.append(
                {
                    "comparison": comparison_name,
                    "key": key_value,
                    "metric": "Group Presence",
                    "python_value": (
                        "Present"
                        if row["_merge"] != "right_only"
                        else "Missing"
                    ),
                    "sql_value": (
                        "Present"
                        if row["_merge"] != "left_only"
                        else "Missing"
                    ),
                    "difference": None,
                    "status": "FAIL",
                }
            )

            continue

        for metric in metric_columns:
            results.append(
                compare_values(
                    comparison_name=comparison_name,
                    key_value=key_value,
                    metric_name=metric,
                    python_value=row[
                        f"{metric}_python"
                    ],
                    sql_value=row[
                        f"{metric}_sql"
                    ],
                )
            )

    return results


# ---------------------------------------------------------
# Reconciliation workflow
# ---------------------------------------------------------

def create_reconciliation_report(
    sql_executive: pd.DataFrame,
    sql_fiscal_year: pd.DataFrame,
    sql_college: pd.DataFrame,
    sql_sponsor: pd.DataFrame,
    sql_research_area: pd.DataFrame,
) -> pd.DataFrame:
    """Compare SQL outputs with Python summary outputs."""

    reconciliation_results = []

    python_executive = convert_python_kpis_to_row(
        PYTHON_EXECUTIVE_KPI_FILE
    )

    executive_metrics = [
        "total_proposals",
        "total_requested_funding",
        "total_awarded_funding",
        "awarded_proposal_count",
        "decided_proposal_count",
        "pending_proposal_count",
        "withdrawn_proposal_count",
        "proposal_success_rate",
        "average_award_amount",
        "average_decision_time",
        "active_principal_investigators",
    ]

    reconciliation_results.extend(
        reconcile_single_row(
            "Executive KPIs",
            python_executive,
            sql_executive,
            executive_metrics,
        )
    )

    grouped_metric_columns = [
        "total_proposals",
        "total_requested_funding",
        "total_awarded_funding",
        "awarded_proposals",
        "decided_proposals",
        "pending_proposals",
        "average_decision_time_days",
        "active_principal_investigators",
        "proposal_success_rate",
        "average_award_amount",
    ]

    python_fiscal_year = pd.read_csv(
        PYTHON_FISCAL_YEAR_FILE
    )

    reconciliation_results.extend(
        reconcile_grouped_data(
            "Fiscal Year Summary",
            python_fiscal_year,
            sql_fiscal_year,
            ["fiscal_year"],
            grouped_metric_columns,
        )
    )

    python_college = pd.read_csv(
        PYTHON_COLLEGE_FILE
    )

    reconciliation_results.extend(
        reconcile_grouped_data(
            "College Summary",
            python_college,
            sql_college,
            ["college"],
            grouped_metric_columns,
        )
    )

    python_sponsor = pd.read_csv(
        PYTHON_SPONSOR_FILE
    )

    reconciliation_results.extend(
        reconcile_grouped_data(
            "Sponsor Summary",
            python_sponsor,
            sql_sponsor,
            ["sponsor_type", "sponsor"],
            grouped_metric_columns,
        )
    )

    python_research_area = pd.read_csv(
        PYTHON_RESEARCH_AREA_FILE
    )

    reconciliation_results.extend(
        reconcile_grouped_data(
            "Research Area Summary",
            python_research_area,
            sql_research_area,
            ["research_area"],
            grouped_metric_columns,
        )
    )

    return pd.DataFrame(reconciliation_results)


def write_text_report(
    report: pd.DataFrame,
    output_path: Path,
) -> None:
    """Write a readable reconciliation report."""

    pass_count = int(
        report["status"].eq("PASS").sum()
    )

    fail_count = int(
        report["status"].eq("FAIL").sum()
    )

    overall_status = (
        "PASSED"
        if fail_count == 0
        else "FAILED"
    )

    lines = [
        "University Research Analytics Dashboard",
        "SQL and Python Reconciliation Report",
        "=" * 48,
        "",
        f"Checks performed: {len(report):,}",
        f"Passed checks: {pass_count:,}",
        f"Failed checks: {fail_count:,}",
        f"Overall status: {overall_status}",
        "",
    ]

    if fail_count > 0:
        lines.append("Failed checks:")
        lines.append("")

        failed_rows = report[
            report["status"] == "FAIL"
        ]

        for _, row in failed_rows.iterrows():
            lines.extend(
                [
                    f"Comparison: {row['comparison']}",
                    f"Key: {row['key']}",
                    f"Metric: {row['metric']}",
                    f"Python value: {row['python_value']}",
                    f"SQL value: {row['sql_value']}",
                    f"Difference: {row['difference']}",
                    "",
                ]
            )
    else:
        lines.append(
            "All compared Python and SQL metrics match."
        )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main() -> None:
    """Run SQL queries, export results, and reconcile metrics."""

    validate_input_files()

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Connecting to SQLite database...")

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        print("Running executive summary query...")

        sql_executive = execute_query(
            connection,
            EXECUTIVE_SUMMARY_QUERY,
        )

        print("Running proposal-status query...")

        sql_status = execute_query(
            connection,
            STATUS_SUMMARY_QUERY,
        )

        print("Running fiscal-year query...")

        sql_fiscal_year = execute_query(
            connection,
            FISCAL_YEAR_SUMMARY_QUERY,
        )

        print("Running college query...")

        sql_college = execute_query(
            connection,
            COLLEGE_SUMMARY_QUERY,
        )

        print("Running department query...")

        sql_department = execute_query(
            connection,
            DEPARTMENT_SUMMARY_QUERY,
        )

        print("Running sponsor query...")

        sql_sponsor = execute_query(
            connection,
            SPONSOR_SUMMARY_QUERY,
        )

        print("Running research-area query...")

        sql_research_area = execute_query(
            connection,
            RESEARCH_AREA_SUMMARY_QUERY,
        )

        print("Running top-investigator query...")

        sql_top_investigators = execute_query(
            connection,
            TOP_INVESTIGATORS_QUERY,
        )

    finally:
        connection.close()

    print("\nExporting SQL results...")

    export_dataframe(
        sql_executive,
        OUTPUT_DIRECTORY
        / "sql_executive_summary.csv",
    )

    export_dataframe(
        sql_status,
        OUTPUT_DIRECTORY
        / "sql_status_summary.csv",
    )

    export_dataframe(
        sql_fiscal_year,
        OUTPUT_DIRECTORY
        / "sql_fiscal_year_summary.csv",
    )

    export_dataframe(
        sql_college,
        OUTPUT_DIRECTORY
        / "sql_college_summary.csv",
    )

    export_dataframe(
        sql_department,
        OUTPUT_DIRECTORY
        / "sql_department_summary.csv",
    )

    export_dataframe(
        sql_sponsor,
        OUTPUT_DIRECTORY
        / "sql_sponsor_summary.csv",
    )

    export_dataframe(
        sql_research_area,
        OUTPUT_DIRECTORY
        / "sql_research_area_summary.csv",
    )

    export_dataframe(
        sql_top_investigators,
        OUTPUT_DIRECTORY
        / "sql_top_investigators.csv",
    )

    print("\nReconciling SQL and Python results...")

    reconciliation_report = (
        create_reconciliation_report(
            sql_executive=sql_executive,
            sql_fiscal_year=sql_fiscal_year,
            sql_college=sql_college,
            sql_sponsor=sql_sponsor,
            sql_research_area=sql_research_area,
        )
    )

    reconciliation_csv_file = (
        OUTPUT_DIRECTORY
        / "sql_reconciliation_report.csv"
    )

    reconciliation_text_file = (
        OUTPUT_DIRECTORY
        / "sql_reconciliation_report.txt"
    )

    export_dataframe(
        reconciliation_report,
        reconciliation_csv_file,
    )

    write_text_report(
        reconciliation_report,
        reconciliation_text_file,
    )

    failed_checks = int(
        reconciliation_report[
            "status"
        ].eq("FAIL").sum()
    )

    print("\nSQL analysis completed.")

    print(
        f"Reconciliation checks: "
        f"{len(reconciliation_report):,}"
    )

    print(
        f"Failed checks: {failed_checks:,}"
    )

    print(
        f"Reconciliation report: "
        f"{reconciliation_text_file}"
    )

    if failed_checks > 0:
        raise ValueError(
            "SQL and Python reconciliation failed. "
            "Review the reconciliation report."
        )

    print(
        "\nAll SQL and Python metrics reconcile."
    )


if __name__ == "__main__":
    main()