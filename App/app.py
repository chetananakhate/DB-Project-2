from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Assuming 'index.html' is your homepage

# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="library"
)

def add_member_to_db(name, ssn, campus_address, home_address, phone_number, member_id, expiry_date, is_prof, is_member_active):
    # Create a cursor object to execute queries
    mycursor = mydb.cursor()

    # SQL query to insert member data
    sql = "INSERT INTO Member (Name, SSN, CampusAddress, HomeAddress, PhoneNumber, MemberID, ExpiryDate, Is_prof, IsMemberActive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, ssn, campus_address, home_address, phone_number, member_id, expiry_date, is_prof, is_member_active)

    try:
        # Execute the query
        mycursor.execute(sql, val)

        # Commit changes to the database
        mydb.commit()

        return True  # Return True on successful insertion
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False on error
    
def add_book_to_db(isbn, title, author_id, subject_area, description, book_type, is_lendable, language, binding, edition):
    try:
        mycursor = mydb.cursor()

        # SQL query to insert book data
        sql = "INSERT INTO Book (ISBN, Title, AuthorID, SubjectArea, Description, BookType, IsLendable, Language, Binding, Edition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (isbn, title, author_id, subject_area, description, book_type, is_lendable, language, binding, edition)

        # Execute the query
        mycursor.execute(sql, val)

        # Commit changes to the database
        mydb.commit()

        return True  # Return True on successful insertion
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False on error

def add_borrow_to_db(issue_id, ssn, staff_id, isbn, issue_date, due_date, notice_date, is_returned):
    # Create a cursor object to execute queries
    mycursor = mydb.cursor()

    # SQL query to insert borrow data
    sql = "INSERT INTO BookIssue (IssueID, SSN, StaffID, ISBN, IssueDate, DueDate, NoticeDate, IsReturned) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (issue_id, ssn, staff_id, isbn, issue_date, due_date, notice_date, is_returned)

    try:
        # Execute the query
        mycursor.execute(sql, val)

        # Commit changes to the database
        mydb.commit()

        return True  # Return True on successful insertion
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False on error


def return_book_to_db(issue_id):
    try:
        # Create a cursor object to execute queries
        mycursor = mydb.cursor()

        # SQL query to update IsReturned status and return date in BookIssue table
        sql = "UPDATE BookIssue SET IsReturned = 'Y', ReturnDate = CURDATE() WHERE IssueID = %s"
        val = (issue_id,)

        # Execute the query
        mycursor.execute(sql, val)

        # Commit changes to the database
        mydb.commit()

        return True  # Return True on successful update
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False on error
    
def renew_membership_in_db(ssn, new_expiry_date):

    try:
        # Create a cursor object to execute queries
        mycursor = mydb.cursor()

        # SQL query to update the expiry date for the specified member
        sql = "UPDATE Member SET ExpiryDate = %s WHERE SSN = %s"
        val = (new_expiry_date, ssn)

        # Execute the query
        mycursor.execute(sql, val)

        # Commit changes to the database
        mydb.commit()

        return True  # Return True on successful update
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False on error


@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        ssn = request.form['ssn']
        campus_address = request.form['campus_address']
        home_address = request.form['home_address']
        phone_number = request.form['phone_number']
        member_id = request.form['member_id']
        expiry_date = request.form['expiry_date']
        is_prof = request.form['is_prof']
        is_member_active = request.form['is_member_active']

        # Error handling for missing or incorrect form data
        if not all([name, ssn, campus_address, home_address, phone_number, member_id, expiry_date, is_prof, is_member_active]):
            error = 'Please fill in all the fields.'
            return render_template('add_member.html', error=error)

        # Simulate adding member to database (replace this with your DB insertion logic)
        success = add_member_to_db(name, ssn, campus_address, home_address, phone_number, member_id, expiry_date, is_prof, is_member_active)
        if success:
            return "Member added successfully!"  # Redirect or display success message
        else:
            error = 'Failed to add member. Please try again.'
            return render_template('add_member.html', error=error)

    return render_template('add_member.html')


# Transaction 2: Add Information about a New Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author_id = request.form['author_id']
        subject_area = request.form['subject_area']
        description = request.form['description']
        book_type = request.form['book_type']
        is_lendable = request.form['is_lendable']
        language = request.form['language']
        binding = request.form['binding']
        edition = request.form['edition']

        # Error handling for missing or incorrect form data
        if not all([isbn, title, author_id, subject_area, description, book_type, is_lendable, language, binding, edition]):
            error = 'Please fill in all the fields.'
            return render_template('add_book.html', error=error)

        # Simulate adding book to database (replace this with your DB insertion logic)
        success = add_book_to_db(isbn, title, author_id, subject_area, description, book_type, is_lendable, language, binding, edition)
        if success:
            return "Book added successfully!"  # Redirect or display success message
        else:
            error = 'Failed to add book. Please try again.'
            return render_template('add_book.html', error=error)

    return render_template('add_book.html')


# Transaction 3: Add Information about a New Borrow (Loan)
@app.route('/add_borrow', methods=['GET', 'POST'])
def add_borrow():
    if request.method == 'POST':
        issue_id = request.form['issue_id']
        ssn = request.form['ssn']
        staff_id = request.form['staff_id']
        isbn = request.form['isbn']
        issue_date = request.form['issue_date']
        due_date = request.form['due_date']
        notice_date = request.form['notice_date']
        is_returned = request.form['is_returned']

        # Error handling for missing or incorrect form data
        if not all([issue_id, ssn, staff_id, isbn, issue_date, due_date, is_returned]):
            error = 'Please fill in all the fields.'
            return render_template('add_borrow.html', error=error)

        # Simulate adding borrow to database (replace this with your DB insertion logic)
        success = add_borrow_to_db(issue_id, ssn, staff_id, isbn, issue_date, due_date, notice_date, is_returned)
        if success:
            return "Borrow added successfully!"  # Redirect or display success message
        else:
            error = 'Failed to add borrow. Please try again.'
            return render_template('add_borrow.html', error=error)

    return render_template('add_borrow.html')


# Transaction 4: Handle the return of a book
@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        issue_id = request.form['issue_id']

        # Error handling for missing or incorrect form data
        if not issue_id:
            error = 'Please provide the Issue ID.'
            return render_template('return_book.html', error=error)

        # Simulate returning book to database (replace this with your DB logic)
        success = return_book_to_db(issue_id)
        if success:
            return "Book returned successfully!"  # Redirect or display success message
        else:
            error = 'Failed to return the book. Please try again.'
            return render_template('return_book.html', error=error)

    return render_template('return_book.html')


# Transaction 5: Renew Membership
@app.route('/renew_membership', methods=['GET', 'POST'])
def renew_membership():
    if request.method == 'POST':
        ssn = request.form['ssn']
        new_expiry_date = request.form['expiry_date']

        # Error handling for missing or incorrect form data
        if not all([ssn, new_expiry_date]):
            error = 'Please fill in all the fields.'
            return render_template('renew_membership.html', error=error)

        # Simulate membership renewal (replace this with your logic to update the database)
        success = renew_membership_in_db(ssn, new_expiry_date)
        if success:
            return "Membership renewed successfully!"  # Redirect or display success message
        else:
            error = 'Failed to renew membership. Please try again.'
            return render_template('renew_membership.html', error=error)

    return render_template('renew_membership.html')


if __name__ == '__main__':
    app.run(debug=True)
