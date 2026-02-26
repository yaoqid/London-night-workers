import sqlite3
import pytest
from my_python_project.coursework2.night_worker_queries import (
    run_select_queries,
    run_update_queries,
    run_insert_queries,
    run_delete_queries,
)


# Test SELECT queries
# This fcuntion is help by ai tool Microsoft Copilot
def test_select_male_weighted_count_desc(test_db):
    con, cur = test_db
    run_select_queries(con, cur)
    rows = cur.execute(
        "SELECT sex, weighted_count, year FROM SEX WHERE sex = 'Male' "
        "ORDER BY weighted_count DESC"
    ).fetchall()
    assert rows == [('Male', 100000, 2020), ('Male', 80000, 2019)]


def test_select_skill_level_weighted_count_desc(test_db):
    con, cur = test_db
    run_select_queries(con, cur)
    rows = cur.execute(
        "SELECT skill_level, weighted_count, year FROM SKILL_LEVEL "
        "WHERE skill_level = 'Level 4' ORDER BY weighted_count DESC"
    ).fetchall()
    assert rows == [('Level 4', 120000, 2021), ('Level 4', 110000, 2020)]


# Test UPDATE queries
def test_update_disability_status(test_db):
    con, cur = test_db
    run_update_queries(con, cur)
    rows = cur.execute(
        (
            "SELECT * FROM DISABILITY_STATUS "
            "WHERE disability_status = 'Have Equality Act Disabled'"
        )
    ).fetchall()
    assert len(rows) == 1


def test_update_no_matching_rows(test_db):
    con, cur = test_db
    cur.execute(
        "UPDATE DISABILITY_STATUS SET disability_status = 'Invalid Status' "
        "WHERE disability_status = 'Nonexistent Status'"
    )
    con.commit()
    rows = cur.execute(
        "SELECT * FROM DISABILITY_STATUS "
        "WHERE disability_status = 'Invalid Status'"
    ).fetchall()
    assert len(rows) == 0


# Test INSERT queries
def test_insert_single_age_band(test_db):
    con, cur = test_db
    run_insert_queries(con, cur)
    rows = cur.execute(
        "SELECT * FROM AGE_BAND WHERE age_band = '1-15'"
    ).fetchall()
    assert len(rows) == 1


def test_insert_multiple_worker_categories(test_db):
    con, cur = test_db
    run_insert_queries(con, cur)
    rows = cur.execute("SELECT * FROM WORKER_CATEGORY").fetchall()
    assert len(rows) == 9  # 9 rows should have been inserted


# Test DELETE queries
def test_delete_specific_age_bands(test_db):
    con, cur = test_db
    run_delete_queries(con, cur)
    rows = cur.execute(
        "SELECT * FROM AGE_BAND WHERE age_band IN ('16-21', '56-61', "
        "'61-66', '1-15')"
    ).fetchall()
    assert len(rows) == 0  # All specified rows should be deleted


def test_delete_no_matching_age_band(test_db):
    con, cur = test_db
    cur.execute("DELETE FROM AGE_BAND WHERE age_band = 'Nonexistent'")
    con.commit()
    rows = cur.execute("SELECT * FROM AGE_BAND").fetchall()
    assert len(rows) > 0  # Ensure the table is not empty


# Test Error Handling for INSERT queries
def test_insert_duplicate_age_band(test_db):
    con, cur = test_db
    # Modify test to ensure duplicate entries fail
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute(
            "INSERT INTO AGE_BAND (age_band, year, category_name) "
            "VALUES ('16-21', 2023, 'Night')"
        )


def test_insert_invalid_worker_category(test_db):
    con, cur = test_db
    # Expect an IntegrityError due to missing NOT NULL column
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute(
            "INSERT INTO WORKER_CATEGORY (category_name) "
            "VALUES ('Incomplete Data')"
        )


# Test Edge Cases for SELECT queries
def test_select_empty_table(test_db):
    con, cur = test_db
    cur.execute("DELETE FROM SEX")
    con.commit()
    rows = cur.execute("SELECT * FROM SEX").fetchall()
    assert len(rows) == 0  # Table should be empty


def test_select_no_matching_rows(test_db):
    con, cur = test_db
    rows = cur.execute(
        "SELECT * FROM SEX WHERE sex = 'Nonexistent'"
    ).fetchall()
    assert len(rows) == 0  # No rows should match
