# COMP0035 2024-25 Computer coursework

This repository contains the coursework1 for COMP0035 2024-25, focusing on analysing demographic data of night workers in London. This project examines various aspects, including disability status, age groups, skill levels, and gender categories, preparing data for analysis, generating visualisations, and saving outputs in the `data` directory.

This repository contains the coursework 2 for COMP0035 2024-25, focusing on designing, implementing, and testing a Python-based web application that builds upon the demographic data of night workers in London prepared in coursework 1. This project includes requirements analysis, interface and application design, database testing, and unit testing to create a functional, testable application using the SQLite database from coursework 1. Outputs include a comprehensive report, Python code files, and updates to the project repository for version control.

## Instructions for using this repository

1. **Clone the Repository**: Start by cloning this repository and navigating into the project directory:
   ```bash
   git clone https://github.com/yaoqid/COMP0035-coursework.git
   cd COMP0035-coursework
   ```

3. **Set Up a Virtual Environment**: It is recommended to use a virtual environment for managing dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate    # For macOS/Linux
    .venv\Scripts\activate       # For Windows
    ```

4. **Install Dependencies: Install the necessary packages with**:
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```
    
5. **Data Preparation: Ensure that the data/ directory contains the main input file:**
    Night_workers.xlsx: This Excel file should have multiple sheets representing different data categories on night workers.

## Activity instructions for coursework1 and code files

1. **Run Section 1 Analysis: Execute the first script to process data**:
   ```bash
    python my_python_project/coursework1/section1.py
   ```

3. **Run Section 2 Analysis: Execute the second script to process data to gennrate database**:
   ```bash
    python my_python_project/coursework1/section2.py
   ```

## Code files

1. [section1](my_python_project/coursework1/section1.py)
2. [section2](my_python_project/coursework1/section2.py)

## Activity instructions for coursework2 and code files

1. **Run Query Analysis: Execute the script to perform SQL queries and generate insights**:
   ```bash
    python my_python_project/coursework2/night_worker_queries.py
   ```
3. **Run Unit Tests: Execute the test suite to validate database queries and application functionality**:
   ```bash
    python -m pytest
   ```
## Code files

1. [section3.1](my_python_project/coursework2/night_worker_queries.py)
2. [section3.2](my_python_project/coursework2/tests/conftest.py)
3. [section3.2](my_python_project/coursework2/tests/test_queries.py)
