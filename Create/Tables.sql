CREATE TABLE Member (Name varchar(50), SSN varchar(10), CampusAddress varchar(100), HomeAddress varchar(100), PhoneNumber varchar(10), MemberID varchar(20), ExpiryDate date, Is_prof varchar(1), IsMemberActive varchar(1), PRIMARY KEY(SSN)); 

CREATE TABLE Staff (StaffID varchar(10), SSN varchar(10), Position varchar(40), PRIMARY KEY(StaffId), FOREIGN KEY f1 (SSN) REFERENCES Member(SSN));

CREATE TABLE Author (AuthorID varchar(10), AuthorName varchar(50), PRIMARY KEY (AuthorID));

CREATE TABLE Book (ISBN varchar(13), Title varchar(50), AuthorID varchar(50), SubjectArea varchar(50), Description varchar(500), BookType Varchar(20), IsLendable varchar(1), Language varchar(20), Binding varchar(20), Edition varchar(20), PRIMARY KEY (ISBN), FOREIGN KEY f2 (AuthorID) REFERENCES Author(AuthorID));

CREATE TABLE BookAvailable (ISBN varchar(13), TotalCopies varchar(10), AvailableCopies varchar(10), FOREIGN KEY f6 (ISBN) REFERENCES Book(ISBN));

CREATE TABLE BookIssue (IssueID varchar(10), SSN varchar(10), StaffID varchar(10), ISBN varchar(13), IssueDate date, DueDate date, NoticeDate date, IsReturned varchar(1), PRIMARY KEY (IssueID), FOREIGN KEY f3 (SSN) REFERENCES Member(SSN), FOREIGN KEY f4 (StaffID) REFERENCES Staff(StaffID), FOREIGN KEY f5 (ISBN) REFERENCES Book(ISBN));

CREATE TABLE BookRequired (ISBN varchar(13), TotalBookRequired varchar(10), FOREIGN KEY f7 (ISBN) REFERENCES Book(ISBN));