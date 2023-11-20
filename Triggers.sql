-- Trigger to Notify a Member about Outstanding Overdue Book:
DELIMITER //
CREATE TRIGGER NotifyOverdueBook
AFTER INSERT ON BookIssue
FOR EACH ROW
BEGIN
    DECLARE issue_date DATE;
    DECLARE due_date DATE;
    DECLARE ssn_var VARCHAR(10);
    DECLARE member_expired DATE;

    SELECT IssueDate, DueDate, SSN INTO issue_date, due_date, ssn_var
    FROM BookIssue
    WHERE IssueID = NEW.IssueID;

    SELECT ExpiryDate INTO member_expired
    FROM Member
    WHERE SSN = ssn_var;

    IF NEW.DueDate < CURDATE() AND member_expired > CURDATE() THEN
        INSERT INTO Notification (SSN, Message, NotificationDate)
        VALUES (ssn_var, 'Your book with ISBN ' || NEW.ISBN || ' is overdue. Please return it as soon as possible.', CURDATE());
    END IF;
END;
//
DELIMITER ;


-- Trigger to Notify a Member about Membership Renewal:
DELIMITER //
CREATE TRIGGER NotifyMembershipRenewal
BEFORE INSERT ON BookIssue
FOR EACH ROW
BEGIN
    DECLARE expiry_date DATE;
    DECLARE ssn_var VARCHAR(10);

    SELECT ExpiryDate, SSN INTO expiry_date, ssn_var
    FROM Member
    WHERE SSN = NEW.SSN;

    IF expiry_date = NEW.IssueDate THEN
        INSERT INTO Notification (SSN, Message, NotificationDate)
        VALUES (ssn_var, 'Your membership is expiring soon. Please renew it to continue borrowing books.', CURDATE());
    END IF;
END;
//
DELIMITER ;
