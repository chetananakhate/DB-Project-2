# DB-Project-2

### Create Database and Tables
    `cd Create`
    `mysql -u root -p library < Tables.sql;`

### Load initial data
    In DataFiles
    `mysql -u root -p library < Member.sql;
    mysql -u root -p library < Staff.sql;
    mysql -u root -p library < Author.sql;
    mysql -u root -p library < Book.sql;
    mysql -u root -p library < BookAvailable.sql;
    mysql -u root -p library < BookIssue.sql;
    mysql -u root -p library < BookRequired.sql;`

### Print the data so that it is easy to understand
    Queries to retrieve and print all the data in database, that it is easy to understand (for example, print appropriate headings, such as: Authors, Book Title, Subject area etc.).
    `mysql -u root -p library < SelectStatements.sql;`

### Weekly Report
    Query that will prepare a report for weekly Borrowing activity by Subject area, by Author, number of copies and number of days loaned out.
    `mysql -u root -p library < WeeklyReport.sql;`

### Python script for update transactions:
    1. To add information about a new member.
    2. To add all the information about a new Book.
    3. To add all the information about a new Borrow (loan) (this must find the book from the catalog).
    4. To handle the return of a book. This transaction prints a return receipt with the details of the book and days when it was borrowed and returned etc.
    5. To renew the membership.
    `python UpdateTransactions.py`

### Triggers
    To notify a member about the outstanding overdue book.
    To notify a member about his membership renewal.
    `mysql -u root -p library < Triggers.sql;`


## Library Management APP

### Project Structure:
    App
    ├── `app.py` : Contains Flask application setup and routing logic.
    ├── templates
    │   ├── `index.html`
    │   ├── `add_member.html`
    │   ├── `add_book.html`
    │   ├── `add_borrow.html`
    │   ├── `return_book.html`
    │   └── `renew_membership.html`
    └── static
        └── `styles.css`

### Usage
    Install the required dependencies:
        `pip install Flask`
        `pip install mysql-connector-python `

    Run the application:
        `python app.py`
        Access the application in your browser at http://localhost:5000/.

### Routes
    /: Homepage with links to different functionalities.
    /add_member: Add new member information.
    /add_book: Add new book information.
    /add_borrow: Borrow a book.
    /return_book: Return a borrowed book.
    /renew_membership: Renew a membership.

