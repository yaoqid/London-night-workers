import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# The method for reduce the error of to many word in a line was suggested by
# Microsoft Copilot
def describe_dataframe(excel_path):
    """Process each sheet in the Excel file, excluding the first sheet."""
    try:
        # Load the Excel file and retrieve sheet names
        excel_data = pd.ExcelFile(excel_path)
        sheet_names = excel_data.sheet_names[1:]  # Skip the first sheet
        print("Processing sheets:", sheet_names)
        print(f"Number of sheets to process: {len(sheet_names)}")

        # Process each sheet fully
        for sheet_name in sheet_names:
            try:
                # Read the sheet skipping 19 rows
                df = pd.read_excel(
                    excel_path, sheet_name=sheet_name, skiprows=19
                )
                print(f"\nSheet: {sheet_name}")
                print("\nShape of the dataframe:")
                print(df.shape)
                print("\nFirst 5 rows of the dataframe:")
                print(df.head())
                print("\nLast 5 rows of the dataframe:")
                print(df.tail())
                print("\nColumn names:")
                print(df.columns)
                print("\nData types of the columns:")
                print(df.dtypes)
                print("\nRows with missing values:")
                print(df[df.isna().any(axis=1)])
                print("\nColumns with missing values:")
                print(df.isnull().sum())
            except Exception as e:
                print(f"Error processing sheet {sheet_name}: {e}")
    except Exception as e:
        print(f"Error loading Excel file {excel_path}: {e}")


def delete_rows(df):
    """Set the 20th row as header and drop the first 19 rows."""
    try:
        df.columns = df.iloc[18]  # Set the 20th row as column headers
        df = df.drop(range(19))  # Drop the first 19 rows
        df = df.reset_index(drop=True)  # Reset the index
    except Exception as e:
        print(f"Error deleting rows: {e}")
    return df


def prepare_dataframe_question1(df):
    try:
        # Clean the dataframe by setting the appropriate header
        # and removing excess rows
        df = delete_rows(df)
        # Convert the 'Year' column to datetime format
        # The way how to change the column name was suggested by
        # Microsoft Copilot
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce').dt.year
        # Filter for 'Night' category and select columns specific
        df = df[df['Night worker category'] == 'Night']
        # Filter for 'London' place of work
        df = df[df['Place of work'] == 'London']
        # Select columns specific to disability status
        df = df[
            ['Year', 'Night worker category', 'Disability', 'Weighted count']
        ]

        # Define the path to save the prepared file based on the sheet
        filepath_to_save = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question1.xlsx"
        )
        df.to_excel(filepath_to_save, index=False)
    except Exception as e:
        print(f"Error preparing dataframe for question 1: {e}")
    return df


def prepare_dataframe_question2(df):
    try:
        """
        Modify the data for demographic trends analysis related to age,
        skill level and disability status.
        Only keeps rows where 'Night worker category' is 'Night' if applicable.
        """
        # Clean the dataframe by setting the appropriate header
        # and removing excess rows
        df = delete_rows(df)
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce').dt.year
        # Filter for 'Night' category and select columns specific
        # to skill levels
        df = df[df['Night worker category'] == 'Night']
        # Filter for 'London' place of work
        df = df[df['Place of work'] == 'London']
        # Select columns specific to skill levels
        df = df[
            [
                'Year', 'Night worker category', 'Age band',
                'Skill level', 'Weighted count'
            ]
        ]

        # Define the path to save the prepared file based on the sheet
        filepath_to_save = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question2.xlsx"
        )
        df.to_excel(filepath_to_save, index=False)
    except Exception as e:
        print(f"Error preparing dataframe for question 2: {e}")
    return df


def prepare_dataframe_question3(df):
    try:
        # Clean the dataframe by setting the appropriate header
        # and removing excess rows
        df = delete_rows(df)
        # Convert the 'Year' column to datetime format
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce').dt.year
        # Filter for 'Night' category and select columns specific
        df = df[df['Night worker category'] == 'Night']
        # Filter for 'London' place of work
        df = df[df['Place of work'] == 'London']
        # Select columns specific to disability status
        df = df[['Year', 'Night worker category', 'Sex', 'Weighted count']]

        # Define the path to save the prepared file based on the sheet
        filepath_to_save = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question3.xlsx"
        )
        df.to_excel(filepath_to_save, index=False)
    except Exception as e:
        print(f"Error preparing dataframe for question 3: {e}")
    return df


def analyse_data1():
    try:
        # Load the Excel file using the specified path format
        df_path = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question1.xlsx"
        )
        df = pd.read_excel(df_path)

        # Convert the 'Year' column to datetime format
        df['Year'] = pd.to_datetime(df['Year'])

        # Separate the data by Sex
        male_data = df[df['Disability'] == 'Equality Act Disabled']
        female_data = df[df['Disability'] == 'Not Equality Act Disabled']

        # Plotting the trend of night workers over the years
        # for each sex
        plt.figure(figsize=(10, 6))
        plt.plot(male_data['Year'], male_data['Weighted count'],
                 label='Male', marker='o')
        plt.plot(female_data['Year'], female_data['Weighted count'],
                 label='Female', marker='o')

        # Labeling the plot
        plt.title('Trends in Number of Night Workers by Sex Over the Years')
        plt.xlabel('Year')
        plt.ylabel('Weighted Count of Night Workers')
        plt.legend()
        plt.grid(True)

        # Save the plot as an image
        save_path = Path(__file__).parent.parent.parent.joinpath(
            "data", 'question1.png'
        )
        plt.savefig(save_path)
    except Exception as e:
        print(f"Error analyzing data for question 1: {e}")


def analyse_data2():
    try:
        # Load the Excel file using your specified path
        df_path = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question2.xlsx"
        )
        df_skill_level = pd.read_excel(df_path)

        # Define the skill levels and specific age bands to focus on
        skill_levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4']
        specific_age_bands_updated = ['21-26', '36-41', '56-61']

        # Setting up a 2x2 grid of subplots with a single x-axis at the bottom
        fig, axs = plt.subplots(
            2, 2, figsize=(16, 12), sharey=True, sharex=True
        )
        fig.suptitle(
            'Night Workers by Specified Age Bands for Skill Levels 1, 2, 3, '
            'and 4'
        )

        # Flatten the axs array for easier iteration
        axs = axs.flatten()

        # Plot each skill level as a grouped bar chart
        # by the specified age bands
        for i, skill_level in enumerate(skill_levels):
            try:
                # Filter data for the specific skill level and age bands
                skill_data = df_skill_level[
                    (df_skill_level['Skill level'] == skill_level) &
                    (
                        df_skill_level['Age band'].isin(
                            specific_age_bands_updated
                        )
                    )
                ]
                # The folowing plot method was suggested by Microsoft Copilot
                skill_age_trends = skill_data.groupby(['Year', 'Age band'])[
                    'Weighted count'].sum().reset_index()

                # Pivot data to get Age bands as columns for plotting
                skill_age_pivot = skill_age_trends.pivot(
                    index='Year', columns='Age band', values='Weighted count'
                ).fillna(0)

                # Plotting grouped bar chart for each skill level
                # in its respective subplot
                skill_age_pivot.plot(kind='bar', width=0.8, ax=axs[i])

                # Adding labels and title for each subplot
                axs[i].set_title(f'Skill Level {skill_level}')
                axs[i].set_ylabel('Weighted Count of Night Workers')
                axs[i].legend(title='Age Band')
                axs[i].grid(axis='y', linestyle='--', alpha=0.7)
            except Exception as e:
                print(f"Error plotting for skill level {skill_level}: {e}")

        # Hide x-axis labels on the top row
        for ax in axs[:2]:
            ax.set_xlabel('')

        # Set x-axis label only on the bottom row
        for ax in axs[2:]:
            ax.set_xlabel('Year')

        # Save the plot as an image
        save_path = Path(__file__).parent.parent.parent.joinpath(
            "data", 'question2.png'
        )
        plt.savefig(save_path)
    except Exception as e:
        print(f"Error analyzing data for question 2: {e}")


def analyse_data3():
    try:
        # Load the Excel file using the specified path format
        df_path = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers_question3.xlsx"
        )
        df = pd.read_excel(df_path)

        # Convert the 'Year' column to datetime format
        df['Year'] = pd.to_datetime(df['Year'])

        # Separate the data by Sex
        male_data = df[df['Sex'] == 'Male']
        female_data = df[df['Sex'] == 'Female']

        # Plotting the trend of night workers over the years for each sex
        plt.figure(figsize=(10, 6))
        plt.plot(
            male_data['Year'], male_data['Weighted count'],
            label='Male', marker='o'
        )
        plt.plot(
            female_data['Year'], female_data['Weighted count'],
            label='Female', marker='o'
        )

        # Labeling the plot
        plt.title('Trends in Number of Night Workers by Sex Over the Years')
        plt.xlabel('Year')
        plt.ylabel('Weighted Count of Night Workers')
        plt.legend()
        plt.grid(True)

        # Save the plot as an image
        save_path = Path(__file__).parent.parent.parent.joinpath(
            "data", 'question3.png'
        )
        plt.savefig(save_path)
    except Exception as e:
        print(f"Error analyzing data for question 3: {e}")


def main():
    try:
        # Define the path to the Excel file
        excel_path = Path(__file__).parent.parent.parent.joinpath(
            "data", "Night_workers.xlsx"
        )
        # Describe each sheet in the file (excpte the first)
        describe_dataframe(excel_path)
        # Read the Disability sheet specifically for preparation
        # without skipping rows
        df = pd.read_excel(excel_path, sheet_name="Disability")
        df = prepare_dataframe_question1(df)
        # Read the Age and skill sheets for preparation
        df = pd.read_excel(excel_path, sheet_name="Age and skill")
        prepare_dataframe_question2(df)
        # Read the Sex sheets for preparation
        df = pd.read_excel(excel_path, sheet_name="Sex")
        prepare_dataframe_question3(df)
        # Analyse the data for each question
        analyse_data1()
        analyse_data2()
        analyse_data3()
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
