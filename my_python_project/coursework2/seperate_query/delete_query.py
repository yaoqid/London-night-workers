import sqlite3
from pathlib import Path

from select_queries import get_db_con

def run_chinook_delete_queries(connection, cursor):
    """Runs the DELETE queries on the chinook database.

    Args:
        connection (sqlite3.Connection): connection object
        cursor (sqlite3.Cursor): cursor object
    """

    # These all assume you ran the insert queries from the previous tutorial activity! If not please run
    # tutorialpkg/sample_code/tutorial8_insert_queries.py first.
    
    # 1. Delete all Artists where the Name is any of: New Artist 1, New Artist 2, New Artist 3, New Artist 4, New Artist 100
    try:
        # Print the artists before delete
        cursor.execute(
            "SELECT * FROM AGE_BAND WHERE age_band IN ('New Artist 1', 'New Artist 2', 'New Artist 3', 'New Artist 4', 'New Artist 100', '1-15')")
        print(cursor.fetchall())
        # Delete the artists
        sql = "DELETE FROM AGE_BAND WHERE age_band IN ('New Artist 1', 'New Artist 2', 'New Artist 3', 'New Artist 4', 'New Artist 100', '1-15')"
        cursor.execute(sql)
        # Print the artists after delete. This should return an empty list.
        cursor.execute(
            "SELECT * FROM AGE_BAND WHERE age_band IN ('New Artist 1', 'New Artist 2', 'New Artist 3', 'New Artist 4', 'New Artist 100', '1-15')")
        print(cursor.fetchall())
        connection.commit()
    except sqlite3.Error as e:
        print(f"An sqlite3 error occurred: {e}")


if __name__ == '__main__':
    # Database file locations
    db_path_chinook = Path(__file__).parent.parent.joinpath('data', 'night_worker_normalised.db')
    # Console and cursor for chinook database
    ch_con, ch_cur = get_db_con(db_path_chinook)

    # Run the Chinook database DELETE queries
    run_chinook_delete_queries(ch_con, ch_cur)
    ch_con.close()