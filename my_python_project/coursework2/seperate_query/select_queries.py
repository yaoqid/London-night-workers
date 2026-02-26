import sqlite3
from pathlib import Path

def get_db_con(db_path):
    """Returns a connection and cursor to the chinook database.

    Returns:
        tuple: A tuple containing the connection and cursor objects.
    """
    # Create a SQL connection the SQLite database and a cursor

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Enable foreign key constraint enforcement for INSERT, UPDATE, and DELETE operations.
    cur.execute('PRAGMA foreign_keys = ON;')
    con.commit()
    return con, cur

def run_chinook_select_queries(con, cur):
    """Runs the select queries on the chinook database."""

    # 1. SELECT Name from artists ORDER BY Name DESC;
    rows = cur.execute("SELECT sex, weighted_count, year FROM SEX WHERE sex = 'Male' ORDER BY weighted_count DESC;").fetchall()
    print("Artists name in descending order:")
    [print(row) for row in rows]

if __name__ == '__main__':
    # Database file locations
    db_path_chinook = Path(__file__).parent.parent.joinpath('data', 'night_worker_normalised.db')
    # Console and cursor for chinook database
    ch_con, ch_cur = get_db_con(db_path_chinook)

    # Chinook database select queries
    run_chinook_select_queries(ch_con, ch_cur)

    # Chinook database select queries with join
    # run_chinook_select_join_queries(ch_con, ch_cur)

    # Close the connection
    ch_con.close()