import sqlite3
from pathlib import Path

from select_queries import get_db_con

def run_chinook_update_queries(connection, cursor):
    """Runs the UPDATE queries on the chinook database."""

    # These all assume you ran the insert queries from the previous tutorial activity!

    # 1. Change the artist name from New Artist 1 to New Artist 100 for all instances
    try:
        cursor.execute("UPDATE DISABILITY_STATUS SET disability_status = 'Have Equality Act Disabled' WHERE disability_status = 'Equality Act Disabled';")
        connection.commit()
        cursor.execute("SELECT * FROM DISABILITY_STATUS WHERE disability_status = 'Have Equality Act Disabled';")
        print(cursor.fetchall())
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    # Database file locations
    db_path_chinook = Path(__file__).parent.parent.joinpath('data', 'night_worker_normalised.db')
    # Console and cursor for chinook database
    ch_con, ch_cur = get_db_con(db_path_chinook)
    # Run the Chinook database UPDATE queries
    run_chinook_update_queries(ch_con, ch_cur)
    ch_con.close()