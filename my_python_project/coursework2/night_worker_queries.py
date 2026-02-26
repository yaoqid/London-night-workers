import sqlite3
from pathlib import Path
# The comments are added by Microsoft Copilot


def get_db_con(db_path):
    """Returns a connection and cursor to the database.

    Args:
        db_path (str): Path to the database file.

    Returns:
        tuple: A tuple containing the connection and cursor objects.
    """
    # Create a SQL connection to the SQLite database and a cursor
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Enable foreign key constraint enforcement for INSERT, UPDATE, and DELETE
    # operations.
    cur.execute('PRAGMA foreign_keys = ON;')
    con.commit()
    return con, cur


def run_select_queries(con, cur):
    """Runs the select queries on the database."""
    # Select sex, weighted_count, and year from SEX where sex is 'Male'
    # and order by weighted_count descending
    print("Males in descending order of weighted count:")
    rows = cur.execute(
        "SELECT sex, weighted_count, year FROM SEX WHERE sex = 'Male' "
        "ORDER BY weighted_count DESC;"
    ).fetchall()
    [print(row) for row in rows]
    print("Level 4 in descending order of weighted count:")
    rows = cur.execute(
        "SELECT skill_level, weighted_count, year FROM SKILL_LEVEL "
        "WHERE skill_level = 'Level 4' "
        "ORDER BY weighted_count DESC;"
    ).fetchall()
    [print(row) for row in rows]


def run_delete_queries(connection, cursor):
    """Runs the DELETE queries on the database.

    Args:
        connection (sqlite3.Connection): Connection object
        cursor (sqlite3.Cursor): Cursor object
    """
    try:
        # Print the age bands before delete
        cursor.execute(
            "SELECT * FROM AGE_BAND WHERE age_band IN ("
            "'16-21', '56-61', '61-66', '1-15')"
        )
        print(cursor.fetchall())
        # Delete the age bands
        sql = (
            "DELETE FROM AGE_BAND WHERE age_band IN "
            "('16-21', '56-61', '61-66', '1-15')"
        )
        cursor.execute(sql)
        # Print the age bands after delete. This should return an empty list.
        cursor.execute(
            "SELECT * FROM AGE_BAND WHERE age_band IN "
            "('16-21', '56-61', '61-66', '1-15')"
        )
        print("After delete:")
        print(cursor.fetchall())
        connection.commit()
    except sqlite3.Error as e:
        print(f"An sqlite3 error occurred: {e}")


def run_update_queries(connection, cursor):
    """Runs the UPDATE queries on the database."""
    try:
        # Update the disability status
        cursor.execute(
            "UPDATE DISABILITY_STATUS SET disability_status = "
            "'Have Equality Act Disabled' "
            "WHERE disability_status = 'Equality Act Disabled';"
        )
        connection.commit()
        # Select and print the updated rows
        cursor.execute(
            "SELECT * FROM DISABILITY_STATUS WHERE disability_status = "
            "'Have Equality Act Disabled';"
        )
        print(cursor.fetchall())
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def run_insert_queries(connection, cursor):
    """Runs the insert queries on the database."""
    try:
        # Insert 1 row into the AGE_BAND table then print it
        print("Inserting a row into AGE_BAND table:")
        age_band = "1-15"
        cursor.execute(
            'INSERT INTO AGE_BAND (age_band, year, category_name) '
            'VALUES (?, ?, ?);',
            (age_band, 2023, "Night")
        )
        connection.commit()
        # Get the last inserted row id
        last_row_id = cursor.lastrowid
        # Select and then print the last inserted row
        cursor.execute('SELECT * FROM AGE_BAND WHERE id = ?', (last_row_id,))
        print(cursor.fetchone())

        # Insert multiple rows into the WORKER_CATEGORY table
        print("Inserting multiple rows into WORKER_CATEGORY table:")
        category_name = "Daytime only"
        year = 2015
        for i in range(1, 10):
            try:
                cursor.execute(
                    'INSERT INTO WORKER_CATEGORY (category_name, year) '
                    'VALUES (?, ?);',
                    (category_name, year)
                )
                connection.commit()
                last_row_id = cursor.lastrowid
                cursor.execute(
                    'SELECT * FROM WORKER_CATEGORY WHERE rowid = ?',
                    (last_row_id,)
                )
                print(cursor.fetchone())
                year += 1
            except sqlite3.IntegrityError as e:
                print(f"An sqlite3 error occurred: {e}")
                year += 1  # Increment year to avoid infinite loop
    except sqlite3.Error as e:
        print(f"An sqlite3 error occurred: {e}")


def main():
    # Database file location
    db_path = Path(__file__).parent.parent.parent.joinpath(
        'data', 'night_worker_normalised.db'
    )
    # Connection and cursor for the database
    con, cur = get_db_con(db_path)

    # Run the SELECT queries
    print("select data:")
    run_select_queries(con, cur)

    # Run the UPDATE queries
    print("updata data:")
    run_update_queries(con, cur)

    # Run the INSERT queries
    print("insert data:")
    run_insert_queries(con, cur)

    # Run the DELETE queries
    print("delete data:")
    run_delete_queries(con, cur)

    # Close the connection
    con.close()


if __name__ == '__main__':
    main()
