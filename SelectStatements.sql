-- Retrieve Member and Staff information together
SELECT 
    'Members' AS Category, 
    Name, SSN, CampusAddress AS Address, PhoneNumber, MemberID, ExpiryDate, Is_prof AS IsProfessional, IsMemberActive AS IsActive
FROM 
    Member
UNION ALL
SELECT 
    'Staff', 
    '' AS Name, SSN, Position AS Address, '' AS PhoneNumber, StaffID AS MemberID, '' AS ExpiryDate, '' AS IsProfessional, '' AS IsActive
FROM 
    Staff;

-- Retrieve Book and Author information together
SELECT 
    'Books' AS Category, 
    Title, SubjectArea, Description, BookType, IsLendable, Language, Binding, Edition, b.ISBN, a.AuthorName AS Author
FROM 
    Book b
INNER JOIN 
    Author a ON b.AuthorID = a.AuthorID
UNION ALL
SELECT 
    'Author', 
    '' AS Title, '' AS SubjectArea, '' AS Description, '' AS BookType, '' AS IsLendable, '' AS Language, '' AS Binding, '' AS Edition, '' AS ISBN, AuthorName AS Author
FROM 
    Author;

-- Retrieve BookAvailable and BookIssue information together
SELECT 
    'Book Availability' AS Category, 
    ba.ISBN, ba.TotalCopies, ba.AvailableCopies, bi.IssueID, bi.IssueDate, bi.DueDate, bi.NoticeDate, bi.IsReturned
FROM 
    BookAvailable ba
LEFT JOIN 
    BookIssue bi ON ba.ISBN = bi.ISBN;
