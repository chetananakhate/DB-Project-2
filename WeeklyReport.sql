-- Replace 'start_date' and 'end_date' with the desired week's start and end dates
SET @start_date := '2023-11-01';
SET @end_date := '2023-11-30';

SELECT
    B.SubjectArea,
    A.AuthorName,
    COUNT(BI.ISBN) AS CopiesBorrowed,
    AVG(DATEDIFF(BI.DueDate, BI.IssueDate)) AS AvgDaysLoanedOut
FROM
    BookIssue BI
JOIN
    Book B ON BI.ISBN = B.ISBN
JOIN
    Author A ON B.AuthorID = A.AuthorID
WHERE
    BI.IssueDate BETWEEN @start_date AND @end_date
GROUP BY
    B.SubjectArea,
    A.AuthorName;


