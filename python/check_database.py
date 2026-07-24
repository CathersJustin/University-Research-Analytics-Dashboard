import sqlite3

import pandas as pd


DATABASE_FILE = "data/processed/university_research_analytics.db"


def main() -> None:
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
            """
        ).fetchall()

        print("Tables in database:\n")

        for table in tables:
            print(table[0])

        query = """
        SELECT
            p.proposal_id,
            pi.principal_investigator_name,
            c.college_name,
            d.department_name,
            s.sponsor_name,
            ra.research_area_name,
            p.proposal_status,
            p.award_amount
        FROM proposals AS p
        INNER JOIN principal_investigators AS pi
            ON p.principal_investigator_id
               = pi.principal_investigator_id
        INNER JOIN departments AS d
            ON pi.department_id = d.department_id
        INNER JOIN colleges AS c
            ON d.college_id = c.college_id
        INNER JOIN sponsors AS s
            ON p.sponsor_id = s.sponsor_id
        INNER JOIN research_areas AS ra
            ON p.research_area_id = ra.research_area_id
        LIMIT 10;
        """

        records = pd.read_sql_query(query, connection)

        print("\nSample joined proposal records:\n")
        print(records.to_string(index=False))

    finally:
        connection.close()


if __name__ == "__main__":
    main()