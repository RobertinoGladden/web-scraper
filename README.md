# ETL Pipeline

This is a simple ETL (Extract, Transform, Load) pipeline project designed to scrape fashion product data from https://fashion-studio.dicoding.dev/, transform it, and save it to both a CSV file and Google Sheets.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Running the Pipeline](#running-the-pipeline)
- [Running Tests](#running-tests)
- [Coverage Test Results](#coverage-test-results)
- [Contributing](#contributing)
- [License](#license)

## Description
This project implements an ETL pipeline to extract data from a fashion website, clean and transform the data (converting prices from USD to IDR), and load it into a CSV file and Google Sheets. It includes unit tests to ensure reliability and code coverage analysis.

## Features
- Extracts 1000 product records from 50 pages of https://fashion-studio.dicoding.dev/.
- Transforms data by converting prices (1 USD = 16,000 IDR), handling invalid values, and ensuring proper data types.
- Loads data into `products.csv` and a Google Sheet with public edit access.
- Includes comprehensive unit tests with coverage reporting.
- Modular design with separate modules for extract, transform, and load operations.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Dicoding ETL Pipeline Sederhana
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your Google Service Account JSON file as `google-sheets-api.json` in the project root for Google Sheets authentication.

## Usage
To run the ETL pipeline:
```bash
python main.py
```
- This will extract data, transform it, and save it to `products.csv` and Google Sheets (`ETL_Pipeline_Results`).

## Project Structure
```bash
├── tests
│   ├── __init__.py
│   ├── test_extract.py
│   ├── test_load.py
│   ├── test_transform.py
├── utils
│   ├── __init__.py
│   ├── extract.py
│   ├── load.py
│   ├── transform.py
├── main.py
├── products.csv
├── requirements.txt
├── google-sheets-api.json
├── submission.txt
├── pytest.ini
└── README.md
```

## Requirements
- Python 3.12+
- Required packages (listed in `requirements.txt`):
  - pandas
  - requests
  - beautifulsoup4
  - gspread
  - google-auth
  - pytest
  - pytest-cov

## Running the Pipeline
1. Ensure all dependencies are installed.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Check the output files:
   - `products.csv` for local storage.
   - Google Sheets (`ETL_Pipeline_Results`) for cloud storage (accessible via the shared link).

## Running Tests
To run unit tests and check code coverage:
```bash
pytest --cov=utils tests/ --cov-report term-missing
```
This command executes all tests in the `tests/` directory and generates a coverage report.

## Coverage Test Results
```bash
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
utils\__init__.py        0      0   100%
utils\extract.py        71      6    92%   83-85, 102-104
utils\load.py           61     10    84%   51-52, 70-72, 77-79, 82-83
utils\transform.py      43      0   100%
--------------------------------------------------
TOTAL                  175     16    91%
```

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any improvements or bug fixes. Ensure tests pass and coverage remains high.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details (if applicable).