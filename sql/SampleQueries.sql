/*
University Research Analytics Dashboard
Analytical and Validation Queries
*/


/* -------------------------------------------------------
   Query 1: Executive KPI Summary
------------------------------------------------------- */

SELECT
    COUNT(DISTINCT proposal_id) AS total_proposals,

    ROUND(
        SUM(requested_amount),
        2
    ) AS total_requested_funding,

    ROUND(
        SUM(award_amount),
        2
    ) AS total_awarded_funding,

    SUM(awarded_flag) AS awarded_proposals,

    SUM(decided_flag) AS decided_proposals,

    SUM(pending_flag) AS pending_proposals,

    SUM(
        CASE
            WHEN proposal_status = 'Withdrawn'
            THEN 1
            ELSE 0
        END
    ) AS withdrawn_proposals,

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
                WHEN decided_flag = 1
                THEN decision_time_days
            END
        ),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT principal_investigator_id
    ) AS active_principal_investigators

FROM proposals;


/* -------------------------------------------------------
   Query 2: Proposal Status Distribution
------------------------------------------------------- */

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


/* -------------------------------------------------------
   Query 3: Fiscal-Year Performance
------------------------------------------------------- */

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
        100.0
        * SUM(awarded_flag)
        / NULLIF(SUM(decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        SUM(award_amount)
        / NULLIF(SUM(awarded_flag), 0),
        2
    ) AS average_award_amount,

    ROUND(
        AVG(decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT principal_investigator_id
    ) AS active_principal_investigators

FROM proposals

GROUP BY fiscal_year

ORDER BY fiscal_year;


/* -------------------------------------------------------
   Query 4: Year-over-Year Award Growth
------------------------------------------------------- */

WITH fiscal_year_awards AS (
    SELECT
        fiscal_year,

        ROUND(
            SUM(award_amount),
            2
        ) AS total_awarded_funding

    FROM proposals

    GROUP BY fiscal_year
),

award_growth AS (
    SELECT
        fiscal_year,
        total_awarded_funding,

        LAG(total_awarded_funding)
            OVER (
                ORDER BY fiscal_year
            ) AS previous_year_funding

    FROM fiscal_year_awards
)

SELECT
    fiscal_year,
    total_awarded_funding,
    previous_year_funding,

    ROUND(
        100.0
        * (
            total_awarded_funding
            - previous_year_funding
        )
        / NULLIF(previous_year_funding, 0),
        2
    ) AS year_over_year_award_growth

FROM award_growth

ORDER BY fiscal_year;


/* -------------------------------------------------------
   Query 5: College Performance
------------------------------------------------------- */

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
    ) AS average_award_amount,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days,

    COUNT(
        DISTINCT p.principal_investigator_id
    ) AS active_principal_investigators

FROM proposals AS p

INNER JOIN principal_investigators AS pi
    ON p.principal_investigator_id
       = pi.principal_investigator_id

INNER JOIN departments AS d
    ON pi.department_id
       = d.department_id

INNER JOIN colleges AS c
    ON d.college_id
       = c.college_id

GROUP BY c.college_name

ORDER BY total_awarded_funding DESC;


/* -------------------------------------------------------
   Query 6: Department Performance
------------------------------------------------------- */

SELECT
    c.college_name AS college,
    d.department_name AS department,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days

FROM proposals AS p

INNER JOIN principal_investigators AS pi
    ON p.principal_investigator_id
       = pi.principal_investigator_id

INNER JOIN departments AS d
    ON pi.department_id
       = d.department_id

INNER JOIN colleges AS c
    ON d.college_id
       = c.college_id

GROUP BY
    c.college_name,
    d.department_name

ORDER BY total_awarded_funding DESC;


/* -------------------------------------------------------
   Query 7: Sponsor Performance
------------------------------------------------------- */

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

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days

FROM proposals AS p

INNER JOIN sponsors AS s
    ON p.sponsor_id = s.sponsor_id

GROUP BY
    s.sponsor_type,
    s.sponsor_name

ORDER BY total_awarded_funding DESC;


/* -------------------------------------------------------
   Query 8: Sponsor-Type Performance
------------------------------------------------------- */

SELECT
    s.sponsor_type,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    ROUND(
        SUM(p.award_amount),
        2
    ) AS total_awarded_funding,

    SUM(p.awarded_flag)
        AS awarded_proposals,

    SUM(p.decided_flag)
        AS decided_proposals,

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate,

    ROUND(
        AVG(p.decision_time_days),
        2
    ) AS average_decision_time_days

FROM proposals AS p

INNER JOIN sponsors AS s
    ON p.sponsor_id = s.sponsor_id

GROUP BY s.sponsor_type

ORDER BY total_awarded_funding DESC;


/* -------------------------------------------------------
   Query 9: Research-Area Performance
------------------------------------------------------- */

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

    ROUND(
        100.0
        * SUM(p.awarded_flag)
        / NULLIF(SUM(p.decided_flag), 0),
        2
    ) AS proposal_success_rate

FROM proposals AS p

INNER JOIN research_areas AS ra
    ON p.research_area_id
       = ra.research_area_id

GROUP BY ra.research_area_name

ORDER BY total_awarded_funding DESC;


/* -------------------------------------------------------
   Query 10: Top Principal Investigators by Funding
------------------------------------------------------- */

SELECT
    pi.principal_investigator_id,
    pi.principal_investigator_name,

    c.college_name AS college,
    d.department_name AS department,

    COUNT(DISTINCT p.proposal_id)
        AS total_proposals,

    SUM(p.awarded_flag)
        AS awarded_proposals,

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
    ON pi.department_id
       = d.department_id

INNER JOIN colleges AS c
    ON d.college_id
       = c.college_id

GROUP BY
    pi.principal_investigator_id,
    pi.principal_investigator_name,
    c.college_name,
    d.department_name

ORDER BY total_awarded_funding DESC

LIMIT 20;


/* -------------------------------------------------------
   Query 11: Departments with High Volume and Low Success

   Identifies departments with proposal volume at or above
   the average department volume and a success rate below
   the overall university success rate.
------------------------------------------------------- */

WITH department_metrics AS (
    SELECT
        c.college_name AS college,
        d.department_name AS department,

        COUNT(DISTINCT p.proposal_id)
            AS total_proposals,

        SUM(p.awarded_flag)
            AS awarded_proposals,

        SUM(p.decided_flag)
            AS decided_proposals,

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
        ON pi.department_id
           = d.department_id

    INNER JOIN colleges AS c
        ON d.college_id
           = c.college_id

    GROUP BY
        c.college_name,
        d.department_name
),

benchmarks AS (
    SELECT
        AVG(total_proposals)
            AS average_department_volume,

        100.0
        * SUM(awarded_proposals)
        / NULLIF(SUM(decided_proposals), 0)
            AS university_success_rate

    FROM department_metrics
)

SELECT
    dm.college,
    dm.department,
    dm.total_proposals,
    dm.proposal_success_rate,

    ROUND(
        b.average_department_volume,
        2
    ) AS average_department_volume,

    ROUND(
        b.university_success_rate,
        2
    ) AS university_success_rate

FROM department_metrics AS dm

CROSS JOIN benchmarks AS b

WHERE
    dm.total_proposals
        >= b.average_department_volume

    AND dm.proposal_success_rate
        < b.university_success_rate

ORDER BY
    dm.total_proposals DESC,
    dm.proposal_success_rate ASC;


/* -------------------------------------------------------
   Query 12: Monthly Submission Trend
------------------------------------------------------- */

SELECT
    submission_year,
    submission_month_number,
    submission_month,

    COUNT(DISTINCT proposal_id)
        AS total_proposals,

    ROUND(
        SUM(requested_amount),
        2
    ) AS total_requested_funding,

    ROUND(
        SUM(award_amount),
        2
    ) AS total_awarded_funding

FROM proposals

GROUP BY
    submission_year,
    submission_month_number,
    submission_month

ORDER BY
    submission_year,
    submission_month_number;


/* -------------------------------------------------------
   Data-Quality Validation Queries
------------------------------------------------------- */


/* Query 13: Duplicate Proposal IDs */

SELECT
    proposal_id,
    COUNT(*) AS duplicate_count

FROM proposals

GROUP BY proposal_id

HAVING COUNT(*) > 1;


/* Query 14: Invalid Funding Records */

SELECT
    proposal_id,
    proposal_status,
    requested_amount,
    award_amount,
    direct_costs,
    indirect_costs

FROM proposals

WHERE
    requested_amount <= 0

    OR (
        proposal_status = 'Awarded'
        AND award_amount <= 0
    )

    OR (
        proposal_status <> 'Awarded'
        AND award_amount <> 0
    )

    OR ROUND(
        direct_costs + indirect_costs,
        2
    ) <> ROUND(award_amount, 2);


/* Query 15: Invalid Date Sequences */

SELECT
    proposal_id,
    submission_date,
    decision_date,
    project_start_date,
    project_end_date

FROM proposals

WHERE
    (
        decision_date IS NOT NULL
        AND decision_date < submission_date
    )

    OR (
        project_start_date IS NOT NULL
        AND project_end_date IS NOT NULL
        AND project_end_date < project_start_date
    );


/* Query 16: Missing Foreign-Key Relationships */

SELECT
    p.proposal_id

FROM proposals AS p

LEFT JOIN principal_investigators AS pi
    ON p.principal_investigator_id
       = pi.principal_investigator_id

LEFT JOIN sponsors AS s
    ON p.sponsor_id = s.sponsor_id

LEFT JOIN research_areas AS ra
    ON p.research_area_id
       = ra.research_area_id

WHERE
    pi.principal_investigator_id IS NULL
    OR s.sponsor_id IS NULL
    OR ra.research_area_id IS NULL;