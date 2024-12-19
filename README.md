# Import Data from Excel to SQLite

This application is designed for importing data from Excel (.xlsx) or CSV files into a SQLite database. It provides a simple graphical interface based on Tkinter for selecting files and databases, then transferring data into the database.

## Features

- Read data from Excel (.xlsx) or CSV files.
- Connect to a SQLite database.
- Automatically create a table (`orders`) in the database if it doesn’t exist.
- Insert new data or update existing records based on `order_id`.
- Display database content in a table within the graphical interface.
- Simple and user-friendly interface for selecting files and databases.

## How It Works

### File and Database Selection
1. Use the "Choose File" button to select an Excel or CSV file.
2. Use the "Choose Database" button to select a SQLite database file.

### Data Import Process
1. The application reads the data from the selected file.
2. It connects to the selected SQLite database.
3. If the `orders` table doesn’t exist, it creates the table.
4. Data from the file is added to the database. If a record with the same `order_id` already exists, it is updated.

### Table Display
- The database content is displayed in a table within the application interface.

## Installation and Usage

### Prerequisites
- Python 3.x
- Required Python libraries:
  - `pandas`
  - `sqlite3` (built-in)
  - `tkinter` (built-in)

### Installation
1. Clone or download this repository.
2. Install the required libraries using pip:
   ```bash
   pip install pandas
