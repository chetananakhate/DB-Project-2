import mysql.connector

conn = mysql.connector.connect(
    host='your_host',
    user='your_username',
    password='your_password',
    database='your_database'
)

def add_new_member(name, ssn, campus_address, home_address, phone_number, member_id, expiry_date, is_prof, is_member_active):
    try:
        cursor = conn.cursor()

        add_member_query = """
        INSERT INTO Member (Name, SSN, CampusAddress, HomeAddress, PhoneNumber, MemberID, ExpiryDate, Is_prof, IsMemberActive)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        member_data = (name, ssn, campus_address, home_address, phone_number, member_id, expiry_date, is_prof, is_member_active)
        
        cursor.execute(add_member_query, member_data)
        conn.commit()

        print("New member added successfully")

    except mysql.connector.Error as error:
        print(f"Error adding new member: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def add_new_book(isbn, title, author_id, subject_area, description, book_type, is_lendable, language, binding, edition):
    try:
        
        cursor = conn.cursor()

        add_book_query = """
        INSERT INTO Book (ISBN, Title, AuthorID, SubjectArea, Description, BookType, IsLendable, Language, Binding, Edition)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        book_data = (isbn, title, author_id, subject_area, description, book_type, is_lendable, language, binding, edition)
        
        cursor.execute(add_book_query, book_data)
        conn.commit()

        print("New book added successfully")

    except mysql.connector.Error as error:
        print(f"Error adding new book: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def borrow_book(member_ssn, staff_id, isbn, issue_date, due_date):
    try:
        cursor = conn.cursor()

        # Check if the book is available for borrowing
        check_book_query = "SELECT AvailableCopies FROM BookAvailable WHERE ISBN = %s"
        cursor.execute(check_book_query, (isbn,))
        available_copies = cursor.fetchone()

        if available_copies and int(available_copies[0]) > 0:
            # Decrement available copies in BookAvailable table
            update_available_copies_query = "UPDATE BookAvailable SET AvailableCopies = AvailableCopies - 1 WHERE ISBN = %s"
            cursor.execute(update_available_copies_query, (isbn,))
            conn.commit()

            # Insert the book borrowing information in BookIssue table
            insert_borrow_query = """
            INSERT INTO BookIssue (SSN, StaffID, ISBN, IssueDate, DueDate, IsReturned)
            VALUES (%s, %s, %s, %s, %s, 'N')
            """
            borrow_data = (member_ssn, staff_id, isbn, issue_date, due_date)
            cursor.execute(insert_borrow_query, borrow_data)
            conn.commit()

            print("Book borrowed successfully")
        else:
            print("The book is not available for borrowing")

    except mysql.connector.Error as error:
        print(f"Error borrowing book: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def return_book(issue_id, return_date):
    try:

        cursor = conn.cursor()

        # Check if the book was borrowed and not returned
        check_issue_query = "SELECT * FROM BookIssue WHERE IssueID = %s AND IsReturned = 'N'"
        cursor.execute(check_issue_query, (issue_id,))
        issue_data = cursor.fetchone()

        if issue_data:
            # Update BookIssue table with return information
            update_return_query = "UPDATE BookIssue SET IsReturned = 'Y', ReturnDate = %s WHERE IssueID = %s"
            cursor.execute(update_return_query, (return_date, issue_id))
            conn.commit()

            # Increase available copies in BookAvailable table
            update_available_copies_query = "UPDATE BookAvailable SET AvailableCopies = AvailableCopies + 1 WHERE ISBN = %s"
            cursor.execute(update_available_copies_query, (issue_data[3],))
            conn.commit()

            # Get book and member details for receipt
            get_book_details_query = "SELECT * FROM Book WHERE ISBN = %s"
            cursor.execute(get_book_details_query, (issue_data[3],))
            book_details = cursor.fetchone()

            get_member_details_query = "SELECT * FROM Member WHERE SSN = %s"
            cursor.execute(get_member_details_query, (issue_data[1],))
            member_details = cursor.fetchone()

            # Print return receipt
            print("Return Receipt")
            print("---------------")
            print(f"Issue ID: {issue_data[0]}")
            print(f"Book ISBN: {issue_data[3]}")
            print(f"Book Title: {book_details[1]}")
            print(f"Borrower SSN: {issue_data[1]}")
            print(f"Borrower Name: {member_details[0]}")
            print(f"Issue Date: {issue_data[4]}")
            print(f"Due Date: {issue_data[5]}")
            print(f"Return Date: {return_date}")
            print("---------------")
            print("Book returned successfully")

        else:
            print("No such book borrowed or already returned")

    except mysql.connector.Error as error:
        print(f"Error returning book: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def renew_membership(member_ssn, new_expiry_date):
    
    try:
        cursor = conn.cursor()

        # Update the membership expiry date for the member
        update_membership_query = "UPDATE Member SET ExpiryDate = %s WHERE SSN = %s"
        cursor.execute(update_membership_query, (new_expiry_date, member_ssn))
        conn.commit()

        print("Membership renewed successfully")

    except mysql.connector.Error as error:
        print(f"Error renewing membership: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



# ------------------------

add_new_member(
    'John Doe',
    '1234567890',
    'Campus Address',
    'Home Address',
    '9876543210',
    'M001',
    '2024-11-30',
    'N',
    'Y'
)

add_new_book(
    '9780123456789',
    'Sample Book Title',
    'A001',
    'Sample Subject Area',
    'Sample Description',
    'Textbook',
    'Y',
    'English',
    'Hardcover',
    '1st Edition'
)

borrow_book(
    '123456789',  
    'S001',       
    '9780123456789',
    '2023-11-19',   
    '2023-12-03'
)


return_book('BI001', '2023-11-30')  # Provide IssueID and Return Date (YYYY-MM-DD)


renew_membership('123456789', '2024-12-31')  # Provide Member SSN and New Expiry Date (YYYY-MM-DD)