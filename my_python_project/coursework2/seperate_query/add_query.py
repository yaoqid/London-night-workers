import sqlite3
from pathlib import Path

from select_queries import get_db_con

def run_chinook_insert_queries(connection, cursor):
    """Runs the insert queries on the chinook database."""

    # 1. Insert 1 row into the artists table then print it
    # Insert the new artist using a parametrised query
    artist_name = "1-15"  # This is a string
    cursor.execute('INSERT INTO AGE_BAND (age_band, year, category_name) VALUES (?, ?, ?);', (artist_name, 2023, "Night"))
    connection.commit()
    # Get the last inserted row id
    last_row_id = cursor.lastrowid
    # Select and then print the last inserted row
    cursor.execute('SELECT * FROM AGE_BAND WHERE id = ?', (last_row_id,))
    print(cursor.fetchone())
    # Insert multiple rows into the WORKER_CATEGORY table
    category_name = "Daytime only"
    year = 2015
    for i in range(1, 10):
        try:
            cursor.execute('INSERT INTO WORKER_CATEGORY (category_name, year) VALUES (?, ?);', (category_name, year))
            connection.commit()
            last_row_id = cursor.lastrowid
            cursor.execute('SELECT * FROM WORKER_CATEGORY WHERE rowid = ?', (last_row_id,))
            print(cursor.fetchone())
            year += 1
        except sqlite3.IntegrityError as e:
            print(f"An sqlite3 error occurred: {e}")
            year += 1  # Increment year to avoid infinite loop




if __name__ == '__main__':
    # Database file locations
    db_path_chinook = Path(__file__).parent.parent.joinpath('data', 'night_worker_normalised.db')
    # Console and cursor for chinook database
    ch_con, ch_cur = get_db_con(db_path_chinook)

    # Run the Chinook database INSERT queries
    run_chinook_insert_queries(ch_con, ch_cur)

    # Close the connection
    ch_con.close()