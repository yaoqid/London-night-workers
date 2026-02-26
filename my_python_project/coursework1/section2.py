import pandas as pd
import sqlite3
from pathlib import Path


# The method for reduce the error of to many word in a line was suggested by
# Microsoft Copilot
def load_and_prepare_data(file_path1, file_path2, file_path3):
    ''' The following function was help by ai tool Microsoft Copilot
    Copilot suggested to use the following code to load and prepare data
    to standardise column names.'''
    """Load Excel files and standardise column names."""
    try:
        # Load the datasets
        data1 = pd.read_excel(file_path1)
        data2 = pd.read_excel(file_path2)
        data3 = pd.read_excel(file_path3)

        # Rename columns to standardise across datasets
        data1.rename(columns={
            'Year': 'year',
            'Night worker category': 'category_name',
            'Disability': 'disability_status',
            'Weighted count': 'weighted_count'
        }, inplace=True)
        data2.rename(columns={
            'Year': 'year',
            'Night worker category': 'category_name',
            'Age band': 'age_band',
            'Skill level': 'skill_level',
            'Weighted count': 'weighted_count'
        }, inplace=True)
        data3.rename(columns={
            'Year': 'year',
            'Night worker category': 'category_name',
            'Sex': 'sex',
            'Weighted count': 'weighted_count'
        }, inplace=True)

        return data1, data2, data3

    except Exception as e:
        print(f"Error loading and preparing data: {e}")
        return None, None, None


def consolidate_data(data1, data2, data3):
    """Consolidate data from the three datasets into unique tables."""
    try:
        # Consolidate unique entries for WORKER_CATEGORY
        unique_worker_category = pd.concat([
            data1[['year', 'category_name']],
            data2[['year', 'category_name']],
            data3[['year', 'category_name']]
        ]).drop_duplicates()

        # Consolidate DISABILITY_STATUS by summing weighted_count
        consolidated_disability_status = data1.groupby(
            ['disability_status', 'year', 'category_name'], as_index=False
        ).agg({
            'weighted_count': 'sum'
        })

        # Consolidate AGE_BAND by ensuring unique combinations
        consolidated_age_band = data2[[
            'age_band', 'year', 'category_name'
        ]].drop_duplicates()

        # Consolidate SKILL_LEVEL by summing weighted_count for unique
        # combinations
        consolidated_skill_level = data2.groupby(
            ['skill_level', 'year', 'category_name'], as_index=False
        ).agg({
            'weighted_count': 'sum'
        })

        # Consolidate SEX by ensuring unique combinations
        consolidated_sex = data3.drop_duplicates()

        return (unique_worker_category,
                consolidated_disability_status,
                consolidated_age_band,
                consolidated_skill_level,
                consolidated_sex)

    except Exception as e:
        print(f"Error consolidating data: {e}")
        return None, None, None, None, None


def create_and_populate_database(
    db_file, unique_worker_category, consolidated_disability_status,
    consolidated_age_band, consolidated_skill_level, consolidated_sex
):
    ''' The following function was help by ai tool Microsoft Copilot'''
    """ Create SQLite database and populate it with consolidated data."""
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Drop tables if they already exist to reset structure
            cursor.execute("DROP TABLE IF EXISTS WORKER_CATEGORY")
            cursor.execute("DROP TABLE IF EXISTS DISABILITY_STATUS")
            cursor.execute("DROP TABLE IF EXISTS AGE_BAND")
            cursor.execute("DROP TABLE IF EXISTS SKILL_LEVEL")
            cursor.execute("DROP TABLE IF EXISTS SEX")

            # Create tables
            # The following code was suggested by Microsoft Copilot
            cursor.execute('''
                CREATE TABLE WORKER_CATEGORY (
                    category_name TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    PRIMARY KEY (year, category_name)
                )
            ''')

            # DISABILITY_STATUS table
            cursor.execute('''
                CREATE TABLE DISABILITY_STATUS (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disability_status TEXT,
                    weighted_count INTEGER,
                    year INTEGER NOT NULL,
                    category_name TEXT NOT NULL,
                    FOREIGN KEY (year, category_name)
                    REFERENCES WORKER_CATEGORY(year, category_name)
                )
            ''')

            # AGE_BAND table
            cursor.execute('''
                CREATE TABLE AGE_BAND (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    age_band TEXT,
                    year INTEGER NOT NULL,
                    category_name TEXT NOT NULL,
                    FOREIGN KEY (year, category_name)
                    REFERENCES WORKER_CATEGORY(year, category_name)
                )
            ''')

            # SKILL_LEVEL table
            cursor.execute('''
                CREATE TABLE SKILL_LEVEL (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_level TEXT,
                    weighted_count INTEGER,
                    year INTEGER NOT NULL,
                    category_name TEXT NOT NULL,
                    FOREIGN KEY (year, category_name)
                    REFERENCES WORKER_CATEGORY(year, category_name)
                )
            ''')

            # SEX table
            cursor.execute('''
                CREATE TABLE SEX (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sex TEXT,
                weighted_count INTEGER,
                year INTEGER NOT NULL,
                category_name TEXT NOT NULL,
                FOREIGN KEY (year, category_name)
                REFERENCES WORKER_CATEGORY(year, category_name)
                )
            ''')

            # Insert data
            unique_worker_category.to_sql(
                'WORKER_CATEGORY', conn, if_exists='append', index=False
            )
            consolidated_disability_status.to_sql(
                'DISABILITY_STATUS', conn, if_exists='append', index=False
            )
            consolidated_age_band.to_sql(
                'AGE_BAND', conn, if_exists='append', index=False
            )
            consolidated_skill_level.to_sql(
                'SKILL_LEVEL', conn, if_exists='append', index=False
            )
            consolidated_sex.to_sql(
                'SEX', conn, if_exists='append', index=False
            )

        print("Database created and data inserted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error creating and populating database: {e}")


def main():
    try:
        # Define file paths based on your structure
        file_path1 = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question1.xlsx"
        )
        file_path2 = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question2.xlsx"
        )
        file_path3 = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question3.xlsx"
        )
        db_file = str(Path(__file__).parent.parent.parent.joinpath(
            "data", "night_worker_normalised.db"
        ))

        # Load and prepare data
        data1, data2, data3 = load_and_prepare_data(
            file_path1, file_path2, file_path3
        )

        # Consolidate data
        unique_worker_category, consolidated_disability_status, \
            consolidated_age_band, consolidated_skill_level, \
            consolidated_sex = consolidate_data(data1, data2, data3)

        # Create and populate the SQLite database
        create_and_populate_database(
            db_file,
            unique_worker_category,
            consolidated_disability_status,
            consolidated_age_band,
            consolidated_skill_level,
            consolidated_sex
        )

    except Exception as e:
        print(f"Error in main: {e}")


# Run the main function
if __name__ == "__main__":
    main()
