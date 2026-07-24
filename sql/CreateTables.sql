/*
University Research Analytics Dashboard
Relational Database Schema

Database dialect: SQLite
Purpose: Store normalized research proposal data for analysis.
*/

PRAGMA foreign_keys = ON;


/* -------------------------------------------------------
   Remove existing tables in dependency order
------------------------------------------------------- */

DROP TABLE IF EXISTS proposals;
DROP TABLE IF EXISTS principal_investigators;
DROP TABLE IF EXISTS research_areas;
DROP TABLE IF EXISTS sponsors;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS colleges;


/* -------------------------------------------------------
   Colleges
------------------------------------------------------- */

CREATE TABLE colleges (
    college_id INTEGER PRIMARY KEY,
    college_name TEXT NOT NULL UNIQUE
);


/* -------------------------------------------------------
   Departments
------------------------------------------------------- */

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    college_id INTEGER NOT NULL,

    CONSTRAINT uq_department_college
        UNIQUE (department_name, college_id),

    CONSTRAINT fk_department_college
        FOREIGN KEY (college_id)
        REFERENCES colleges (college_id)
);


/* -------------------------------------------------------
   Principal Investigators
------------------------------------------------------- */

CREATE TABLE principal_investigators (
    principal_investigator_id TEXT PRIMARY KEY,
    principal_investigator_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,

    CONSTRAINT fk_investigator_department
        FOREIGN KEY (department_id)
        REFERENCES departments (department_id)
);


/* -------------------------------------------------------
   Sponsors
------------------------------------------------------- */

CREATE TABLE sponsors (
    sponsor_id INTEGER PRIMARY KEY,
    sponsor_name TEXT NOT NULL UNIQUE,
    sponsor_type TEXT NOT NULL,

    CONSTRAINT chk_sponsor_type
        CHECK (
            sponsor_type IN (
                'Federal',
                'State',
                'Industry',
                'Foundation',
                'Nonprofit',
                'Internal'
            )
        )
);


/* -------------------------------------------------------
   Research Areas
------------------------------------------------------- */

CREATE TABLE research_areas (
    research_area_id INTEGER PRIMARY KEY,
    research_area_name TEXT NOT NULL UNIQUE
);


/* -------------------------------------------------------
   Proposals
------------------------------------------------------- */

CREATE TABLE proposals (
    proposal_id TEXT PRIMARY KEY,

    principal_investigator_id TEXT NOT NULL,
    sponsor_id INTEGER NOT NULL,
    research_area_id INTEGER NOT NULL,

    proposal_type TEXT NOT NULL,
    proposal_status TEXT NOT NULL,

    submission_date TEXT NOT NULL,
    decision_date TEXT,
    project_start_date TEXT,
    project_end_date TEXT,

    requested_amount NUMERIC NOT NULL,
    award_amount NUMERIC NOT NULL DEFAULT 0,
    direct_costs NUMERIC NOT NULL DEFAULT 0,
    indirect_costs NUMERIC NOT NULL DEFAULT 0,

    fiscal_year INTEGER NOT NULL,
    fiscal_quarter TEXT NOT NULL,

    submission_year INTEGER NOT NULL,
    submission_month TEXT NOT NULL,
    submission_month_number INTEGER NOT NULL,

    decision_year INTEGER,
    decision_month TEXT,
    decision_time_days INTEGER,
    project_duration_days INTEGER,

    decided_flag INTEGER NOT NULL DEFAULT 0,
    awarded_flag INTEGER NOT NULL DEFAULT 0,
    pending_flag INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT fk_proposal_investigator
        FOREIGN KEY (principal_investigator_id)
        REFERENCES principal_investigators (
            principal_investigator_id
        ),

    CONSTRAINT fk_proposal_sponsor
        FOREIGN KEY (sponsor_id)
        REFERENCES sponsors (sponsor_id),

    CONSTRAINT fk_proposal_research_area
        FOREIGN KEY (research_area_id)
        REFERENCES research_areas (research_area_id),

    CONSTRAINT chk_proposal_type
        CHECK (
            proposal_type IN (
                'New',
                'Renewal',
                'Resubmission',
                'Supplement'
            )
        ),

    CONSTRAINT chk_proposal_status
        CHECK (
            proposal_status IN (
                'Awarded',
                'Declined',
                'Pending',
                'Withdrawn'
            )
        ),

    CONSTRAINT chk_requested_amount
        CHECK (requested_amount > 0),

    CONSTRAINT chk_award_amount
        CHECK (award_amount >= 0),

    CONSTRAINT chk_direct_costs
        CHECK (direct_costs >= 0),

    CONSTRAINT chk_indirect_costs
        CHECK (indirect_costs >= 0),

    CONSTRAINT chk_cost_reconciliation
        CHECK (
            ROUND(direct_costs + indirect_costs, 2)
            = ROUND(award_amount, 2)
        ),

    CONSTRAINT chk_awarded_proposal_amount
        CHECK (
            (
                proposal_status = 'Awarded'
                AND award_amount > 0
            )
            OR
            (
                proposal_status <> 'Awarded'
                AND award_amount = 0
            )
        ),

    CONSTRAINT chk_decided_flag
        CHECK (decided_flag IN (0, 1)),

    CONSTRAINT chk_awarded_flag
        CHECK (awarded_flag IN (0, 1)),

    CONSTRAINT chk_pending_flag
        CHECK (pending_flag IN (0, 1)),

    CONSTRAINT chk_submission_month_number
        CHECK (
            submission_month_number
            BETWEEN 1 AND 12
        )
);


/* -------------------------------------------------------
   Indexes

   Indexes improve filtering and grouping performance.
------------------------------------------------------- */

CREATE INDEX idx_proposals_submission_date
    ON proposals (submission_date);

CREATE INDEX idx_proposals_fiscal_year
    ON proposals (fiscal_year);

CREATE INDEX idx_proposals_status
    ON proposals (proposal_status);

CREATE INDEX idx_proposals_investigator
    ON proposals (principal_investigator_id);

CREATE INDEX idx_proposals_sponsor
    ON proposals (sponsor_id);

CREATE INDEX idx_proposals_research_area
    ON proposals (research_area_id);

CREATE INDEX idx_departments_college
    ON departments (college_id);