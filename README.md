# Python DB Management CLI
*Python DB Management CLI* is a personal learning project developed in Python to manage a SQL Server database via Command-Line Interface (CLI). The project was created to practice and deepen my skills in Python, working with databases, and creating a functional CLI tool.  It allows to add, retrieve, and delete books from a database, with user input validated and localized for different languages.

While the project was designed for learning purposes, others are welcome to use or experiment with it.

## 📂 Project Structure
- `/cli/cli.py` -> Main CLI handler
- `/cli/commands.py` -> Command definitions
- `/database/dbconnection.py` -> Connection details and logic to interact with SQL Server
- `/localization/localization.py` -> Localization logic and JSON loading
- `/validation/validation.py` -> Functions for validating user inputs
- `MyLibraryCLI.py` -> Main file to run the CLI
- `MyLibraryCLI_default.json` -> Default localization file
- `MyLibraryCLI_en.json` -> English localization file
- `MyLibraryCLI_pt.json` -> Portuguese localization file

## 🚀 About This Project
### Key Features:
- CLI to interact with the system
- Multi-language support using JSON files for localization
- Data validation to ensure correct user input
- SQL Server connection to interact with an existing database
- Error handling using custom exceptions

### What I Learned:
- Building a CLI program with Python
- Handling data validation and exceptions effectively
- Using regex for data validation
- Implementing localization with JSON files
- Connecting Python with a SQL Server database, allowing to simple CRUD operations

## ⚙️ Prerequisites
- Python 3.6+ (recommended)
- SQL Server (installed and running)
- SQL Server connection information (input manually on `dbconnection.py`)
- Required Python libraries:

    `pyodbc`: To connect to SQL Server

    `argparse`: For parsing command-line arguments
    
    `regex`: For advanced regular expression handling 

Install the required dependencies with the following command:
```
pip install pyodbc argparse regex
```

### 🗃️ Database
The database used for this project can be found in the [here](link). You can set it up and test the functionality if you wish.

## 📝 Usage
This project is designed to be used via the command line. To get more information about the available commands and arguments, simply run:
```
python MyLibraryCLI.py -h
```
This will display all the available options and commands.

### Some command examples:
- Change Language:
```
cd path\to\your\project MyLibraryCLI.py changeLanguage -pt
```
- Add Book:
```
cd path\to\your\project MyLibraryCLI.py addBook -sn 1234567890123 -title "Book Title" -year 2020 -fine 1.5 -publisherID 1 -amount 10 -availableAmount 5 -categoryID 2 -author "Author Name"
```
- Query Book:
```
cd path\to\your\project MyLibraryCLI.py getBook -sn 1234567890123
```
```
cd path\to\your\project MyLibraryCLI.py getBook -title "Book Title" -author "Author Name"
```
-Delete Book:
```
cd path\to\your\project MyLibraryCLI.py delBook -sn 1234567890123 -condition "bad"
```

## 🔧 Actual Commands and Parameters
- *changeLanguage*: Changes the CLI language:

    `-en`: English

    `-pt`: Portuguese
- *addBook*: Adds a book to the database with the following required parameters:

    `-sn`: Book serial number (13 digits)

    `-title`: Title of the book

    `-year`: Year of publication

    `-fine`: Daily fine for late return

    `-publisherID`: Publisher ID

    `-amount`: Total number of copies

    `-availableAmount`: Number of available copies

    `-categoryID`: Category ID

    `-author`: Author of the book

- *getBook*: Retrieves books based on the given criteria:

    `-sn`: Serial number

    `-title`: Title of the book

    `-publisher`: Publisher name

    `-category`: Category name

    `-author`: Author name

- *delBook*: Deletes a book from the database:

    `-sn`: Serial number

    `-copyID`: Copy ID

    `-condition`: Condition of the book(s) (e.g., "good", "as new")

## 🐞 Bug Notes
There's an issue with *delete book*: The `delBook` command might not be functioning correctly. I’m aware of the issue and plan to fix it in the future!