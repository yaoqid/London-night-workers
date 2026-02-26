import pytest
import sqlite3


@pytest.fixture(scope="function")
def test_db():
    # the function is help by ai tool Microsoft Copilot
    """Creates an in-memory SQLite database for testing."""
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE SEX (
            id INTEGER PRIMARY KEY,
            sex TEXT,
            weighted_count INTEGER,
            year INTEGER,
            category_name TEXT
        );
        INSERT INTO SEX VALUES
            (1, 'Male', 100000, 2020, 'Night'),
            (2, 'Male', 80000, 2019, 'Night');

        CREATE TABLE SKILL_LEVEL (
            id INTEGER PRIMARY KEY,
            skill_level TEXT,
            weighted_count INTEGER,
            year INTEGER,
            category_name TEXT
        );
        INSERT INTO SKILL_LEVEL VALUES
            (1, 'Level 4', 120000, 2021, 'Night'),
            (2, 'Level 4', 110000, 2020, 'Night');

        CREATE TABLE AGE_BAND (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age_band TEXT UNIQUE,
            year INTEGER,
            category_name TEXT
        );
        INSERT INTO AGE_BAND VALUES
            (1, '16-21', 2020, 'Night'),
            (2, '56-61', 2020, 'Night');

        CREATE TABLE DISABILITY_STATUS (
            id INTEGER PRIMARY KEY,
            disability_status TEXT,
            weighted_count INTEGER,
            year INTEGER,
            category_name TEXT
        );
        INSERT INTO DISABILITY_STATUS VALUES
            (1, 'Equality Act Disabled', 5000, 2020, 'Night');

        CREATE TABLE WORKER_CATEGORY (
            category_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (category_name, year)
        );
    """)
    con.commit()
    yield con, cur
    con.close()
