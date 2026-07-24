"""
Generate a synthetic university research proposal dataset.

The generated data is intended solely for portfolio and educational use.
No real university, employee, or proposal information is included.
"""

from datetime import date, timedelta
from pathlib import Path
import random

import numpy as np
import pandas as pd
from faker import Faker


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RANDOM_SEED = 42
NUMBER_OF_PROPOSALS = 2000
NUMBER_OF_INVESTIGATORS = 180

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

fake = Faker("en_US")


# ---------------------------------------------------------
# Repository paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = RAW_DATA_DIRECTORY / "research_proposals_raw.csv"


# ---------------------------------------------------------
# Reference data
# ---------------------------------------------------------

COLLEGES_AND_DEPARTMENTS = {
    "College of Engineering": [
        "Computer Science",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
    ],
    "College of Medicine": [
        "Biomedical Sciences",
        "Neuroscience",
        "Internal Medicine",
        "Public Health",
    ],
    "College of Arts and Sciences": [
        "Biology",
        "Chemistry",
        "Physics",
        "Psychology",
    ],
    "College of Agriculture": [
        "Plant and Soil Sciences",
        "Animal Sciences",
        "Agricultural Economics",
    ],
    "College of Education": [
        "Educational Leadership",
        "Curriculum and Instruction",
    ],
    "College of Business": [
        "Finance",
        "Management",
        "Marketing",
    ],
}


COLLEGE_WEIGHTS = {
    "College of Engineering": 0.24,
    "College of Medicine": 0.29,
    "College of Arts and Sciences": 0.20,
    "College of Agriculture": 0.12,
    "College of Education": 0.07,
    "College of Business": 0.08,
}


RESEARCH_AREAS_BY_COLLEGE = {
    "College of Engineering": [
        "Artificial Intelligence",
        "Data Science",
        "Renewable Energy",
        "Advanced Manufacturing",
        "Environmental Science",
    ],
    "College of Medicine": [
        "Biomedical Research",
        "Neuroscience",
        "Public Health",
        "Data Science",
    ],
    "College of Arts and Sciences": [
        "Biomedical Research",
        "Environmental Science",
        "Social and Behavioral Science",
        "Data Science",
        "Neuroscience",
    ],
    "College of Agriculture": [
        "Agriculture",
        "Environmental Science",
        "Data Science",
        "Renewable Energy",
    ],
    "College of Education": [
        "Education",
        "Social and Behavioral Science",
        "Data Science",
    ],
    "College of Business": [
        "Business and Economics",
        "Data Science",
        "Social and Behavioral Science",
    ],
}


SPONSORS = [
    ("National Institutes of Health", "Federal", 0.16),
    ("National Science Foundation", "Federal", 0.15),
    ("Department of Energy", "Federal", 0.08),
    ("Department of Defense", "Federal", 0.07),
    ("Department of Agriculture", "Federal", 0.06),
    ("National Aeronautics and Space Administration", "Federal", 0.04),
    ("Centers for Disease Control and Prevention", "Federal", 0.04),
    ("Department of Education", "Federal", 0.04),
    ("State Research Council", "State", 0.06),
    ("State Department of Public Health", "State", 0.04),
    ("Bluegrass Technology Corporation", "Industry", 0.05),
    ("Advanced Manufacturing Solutions", "Industry", 0.04),
    ("Health Innovation Partners", "Industry", 0.04),
    ("Future Science Foundation", "Foundation", 0.04),
    ("Community Health Foundation", "Foundation", 0.03),
    ("Education Advancement Foundation", "Foundation", 0.02),
    ("Regional Research Alliance", "Nonprofit", 0.02),
    ("University Research Initiative", "Internal", 0.02),
]


PROPOSAL_TYPES = [
    "New",
    "Renewal",
    "Resubmission",
    "Supplement",
]

PROPOSAL_TYPE_WEIGHTS = [
    0.62,
    0.18,
    0.14,
    0.06,
]


STATUS_PROBABILITIES = {
    "Federal": {
        "Awarded": 0.34,
        "Declined": 0.50,
        "Pending": 0.12,
        "Withdrawn": 0.04,
    },
    "State": {
        "Awarded": 0.42,
        "Declined": 0.42,
        "Pending": 0.11,
        "Withdrawn": 0.05,
    },
    "Industry": {
        "Awarded": 0.51,
        "Declined": 0.33,
        "Pending": 0.11,
        "Withdrawn": 0.05,
    },
    "Foundation": {
        "Awarded": 0.39,
        "Declined": 0.45,
        "Pending": 0.11,
        "Withdrawn": 0.05,
    },
    "Nonprofit": {
        "Awarded": 0.44,
        "Declined": 0.39,
        "Pending": 0.12,
        "Withdrawn": 0.05,
    },
    "Internal": {
        "Awarded": 0.63,
        "Declined": 0.25,
        "Pending": 0.08,
        "Withdrawn": 0.04,
    },
}


FUNDING_PARAMETERS = {
    "Federal": (13.20, 0.75),
    "State": (12.25, 0.65),
    "Industry": (12.70, 0.70),
    "Foundation": (12.15, 0.65),
    "Nonprofit": (11.85, 0.60),
    "Internal": (10.90, 0.50),
}


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def generate_random_date(start_date: date, end_date: date) -> date:
    """Return a random date between the provided dates."""

    number_of_days = (end_date - start_date).days
    random_offset = random.randint(0, number_of_days)

    return start_date + timedelta(days=random_offset)


def generate_investigators(number_of_investigators: int) -> pd.DataFrame:
    """Create principal investigators assigned to valid departments."""

    college_names = list(COLLEGES_AND_DEPARTMENTS.keys())
    college_weights = [
        COLLEGE_WEIGHTS[college] for college in college_names
    ]

    investigators = []

    for investigator_number in range(1, number_of_investigators + 1):
        college = random.choices(
            college_names,
            weights=college_weights,
            k=1,
        )[0]

        department = random.choice(
            COLLEGES_AND_DEPARTMENTS[college]
        )

        investigators.append(
            {
                "principal_investigator_id": (
                    f"PI-{investigator_number:04d}"
                ),
                "principal_investigator_name": (
                    f"Dr. {fake.unique.name()}"
                ),
                "college": college,
                "department": department,
            }
        )

    return pd.DataFrame(investigators)


def select_sponsor() -> tuple[str, str]:
    """Select a sponsor and return its name and sponsor type."""

    sponsor_weights = [sponsor[2] for sponsor in SPONSORS]

    selected_sponsor = random.choices(
        SPONSORS,
        weights=sponsor_weights,
        k=1,
    )[0]

    sponsor_name = selected_sponsor[0]
    sponsor_type = selected_sponsor[1]

    return sponsor_name, sponsor_type


def select_proposal_status(sponsor_type: str) -> str:
    """Select a proposal status based on sponsor type."""

    status_options = list(
        STATUS_PROBABILITIES[sponsor_type].keys()
    )

    status_weights = list(
        STATUS_PROBABILITIES[sponsor_type].values()
    )

    return random.choices(
        status_options,
        weights=status_weights,
        k=1,
    )[0]


def generate_requested_amount(sponsor_type: str) -> float:
    """Generate a realistic requested funding amount."""

    mean, standard_deviation = FUNDING_PARAMETERS[sponsor_type]

    amount = np.random.lognormal(
        mean=mean,
        sigma=standard_deviation,
    )

    amount = np.clip(amount, 25_000, 5_000_000)

    return float(round(amount / 1000) * 1000)


def generate_funding_values(
    proposal_status: str,
    requested_amount: float,
) -> tuple[float, float, float]:
    """
    Generate award, direct cost, and indirect cost values.

    Non-awarded proposals receive zero dollars.
    """

    if proposal_status != "Awarded":
        return 0.0, 0.0, 0.0

    award_percentage = random.uniform(0.70, 1.00)

    award_amount = round(
        requested_amount * award_percentage,
        2,
    )

    direct_cost_percentage = random.uniform(0.72, 0.86)

    direct_costs = round(
        award_amount * direct_cost_percentage,
        2,
    )

    indirect_costs = round(
        award_amount - direct_costs,
        2,
    )

    return award_amount, direct_costs, indirect_costs


def generate_proposal_dates(
    proposal_status: str,
    submission_date: date,
) -> tuple[date | None, date | None, date | None]:
    """Generate decision and project dates based on proposal status."""

    if proposal_status not in {"Awarded", "Declined"}:
        return None, None, None

    decision_delay = random.randint(30, 300)

    decision_date = submission_date + timedelta(
        days=decision_delay
    )

    if proposal_status == "Declined":
        return decision_date, None, None

    project_start_delay = random.randint(30, 180)

    project_start_date = decision_date + timedelta(
        days=project_start_delay
    )

    project_duration_years = random.choice([1, 2, 3, 4, 5])

    project_end_date = project_start_date + timedelta(
        days=365 * project_duration_years
    )

    return (
        decision_date,
        project_start_date,
        project_end_date,
    )


# ---------------------------------------------------------
# Dataset generation
# ---------------------------------------------------------

def generate_proposal_dataset(
    number_of_proposals: int,
    investigators: pd.DataFrame,
) -> pd.DataFrame:
    """Generate the full synthetic proposal dataset."""

    proposal_records = []

    submission_start_date = date(2021, 7, 1)
    submission_end_date = date(2025, 8, 31)

    for proposal_number in range(1, number_of_proposals + 1):
        investigator = investigators.sample(
            n=1,
            random_state=proposal_number,
        ).iloc[0]

        college = investigator["college"]

        research_area = random.choice(
            RESEARCH_AREAS_BY_COLLEGE[college]
        )

        sponsor, sponsor_type = select_sponsor()

        proposal_type = random.choices(
            PROPOSAL_TYPES,
            weights=PROPOSAL_TYPE_WEIGHTS,
            k=1,
        )[0]

        proposal_status = select_proposal_status(
            sponsor_type
        )

        submission_date = generate_random_date(
            submission_start_date,
            submission_end_date,
        )

        requested_amount = generate_requested_amount(
            sponsor_type
        )

        (
            award_amount,
            direct_costs,
            indirect_costs,
        ) = generate_funding_values(
            proposal_status,
            requested_amount,
        )

        (
            decision_date,
            project_start_date,
            project_end_date,
        ) = generate_proposal_dates(
            proposal_status,
            submission_date,
        )

        proposal_records.append(
            {
                "proposal_id": f"PROP-{proposal_number:06d}",
                "principal_investigator_id": investigator[
                    "principal_investigator_id"
                ],
                "principal_investigator_name": investigator[
                    "principal_investigator_name"
                ],
                "college": college,
                "department": investigator["department"],
                "research_area": research_area,
                "sponsor": sponsor,
                "sponsor_type": sponsor_type,
                "proposal_type": proposal_type,
                "proposal_status": proposal_status,
                "submission_date": submission_date,
                "decision_date": decision_date,
                "project_start_date": project_start_date,
                "project_end_date": project_end_date,
                "requested_amount": requested_amount,
                "award_amount": award_amount,
                "direct_costs": direct_costs,
                "indirect_costs": indirect_costs,
            }
        )

    return pd.DataFrame(proposal_records)


def validate_generated_data(dataset: pd.DataFrame) -> None:
    """Perform basic validation before exporting the raw dataset."""

    if dataset["proposal_id"].duplicated().any():
        raise ValueError("Duplicate proposal IDs were generated.")

    if (dataset["requested_amount"] <= 0).any():
        raise ValueError(
            "Requested funding must be greater than zero."
        )

    awarded = dataset["proposal_status"] == "Awarded"
    non_awarded = dataset["proposal_status"] != "Awarded"

    if (dataset.loc[awarded, "award_amount"] <= 0).any():
        raise ValueError(
            "Every awarded proposal must have an award amount."
        )

    if (dataset.loc[non_awarded, "award_amount"] != 0).any():
        raise ValueError(
            "Non-awarded proposals must have zero award funding."
        )

    calculated_total = (
        dataset["direct_costs"] + dataset["indirect_costs"]
    ).round(2)

    reported_total = dataset["award_amount"].round(2)

    if not calculated_total.equals(reported_total):
        raise ValueError(
            "Direct and indirect costs do not reconcile."
        )


def main() -> None:
    """Generate, validate, and export the proposal dataset."""

    print("Generating principal investigators...")

    investigators = generate_investigators(
        NUMBER_OF_INVESTIGATORS
    )

    print(
        f"Generating {NUMBER_OF_PROPOSALS:,} "
        "synthetic proposals..."
    )

    proposal_dataset = generate_proposal_dataset(
        NUMBER_OF_PROPOSALS,
        investigators,
    )

    validate_generated_data(proposal_dataset)

    RAW_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    proposal_dataset.to_csv(
        OUTPUT_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )

    print("\nDataset successfully generated.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Number of records: {len(proposal_dataset):,}")

    print("\nProposal status totals:")
    print(
        proposal_dataset["proposal_status"]
        .value_counts()
        .to_string()
    )

    print("\nTotal requested funding:")
    print(
        f"${proposal_dataset['requested_amount'].sum():,.2f}"
    )

    print("\nTotal awarded funding:")
    print(
        f"${proposal_dataset['award_amount'].sum():,.2f}"
    )


if __name__ == "__main__":
    main()