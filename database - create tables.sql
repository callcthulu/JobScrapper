 CREATE DATABASE JobsDB
 GO

 USE jobsDB
 GO
 
 CREATE SCHEMA o
 GO

 CREATE TABLE o.website
 (
	  ID int IDENTITY(1,1)
CONSTRAINT PK_website PRIMARY KEY NONCLUSTERED (ID)
	, name nvarchar(256)
	, url nvarchar(max)
	--,siteCode 
);

 CREATE TABLE o.tag
 (
	 ID int IDENTITY(1,1)
CONSTRAINT PK_tag PRIMARY KEY NONCLUSTERED (ID)
	,tag nvarchar(1024)
 );

CREATE TABLE o.category
(
	  ID int IDENTITY(1,1)
CONSTRAINT PK_category PRIMARY KEY NONCLUSTERED (ID)
	, category nvarchar(256)
);

CREATE TABLE o.JobTitle
(
	  ID int IDENTITY(1,1)
CONSTRAINT PK_jobTitle PRIMARY KEY NONCLUSTERED (ID)
	, title nvarchar(1024)
	--in future jobtitle unifier
);

CREATE TABLE o.currency
(
	    ID int IDENTITY(1,1)
CONSTRAINT PK_currency PRIMARY KEY NONCLUSTERED (ID)
	  , code nvarchar(3) 
	  --in future - currency converter
);

CREATE TABLE o.company
(
	  ID int IDENTITY(1,1)
CONSTRAINT PK_company PRIMARY KEY NONCLUSTERED (ID)
	, name nvarchar(max)
	, street nvarchar(max)
	, building nvarchar(max)
	, city nvarchar(max)
);
 
 CREATE TABLE o.jobOffer
 (
      ID int IDENTITY(1,1)
CONSTRAINT PK_jobOffer PRIMARY KEY NONCLUSTERED (ID)
	, websiteID int
CONSTRAINT FK_website FOREIGN KEY (websiteID)
	REFERENCES o.website (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
	, categoryID int
CONSTRAINT FK_category FOREIGN KEY (categoryID)
	REFERENCES o.category (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
	, jobTitleID int
CONSTRAINT FK_jobTitle FOREIGN KEY (jobTitleID)
	REFERENCES o.jobTitle (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
	, currencyID int
CONSTRAINT FK_currency FOREIGN KEY (currencyID)
	REFERENCES o.currency (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
	, companyID	int
CONSTRAINT FK_company FOREIGN KEY (companyID)
	REFERENCES o.company (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
	, salaryMin decimal(18,2)
	, salaryMax decimal(18,2)
	, postingDate datetime
	, retrievingDate datetime
	, ifRemote bit
 );


 CREATE TABLE o.jobOfferTag
(
	  jobOfferID int
CONSTRAINT FK_jobOffer FOREIGN KEY (jobOfferID)
	REFERENCES o.jobOffer (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
	, tagID int
CONSTRAINT FK_tag FOREIGN KEY (tagID)
	REFERENCES o.tag (ID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);


CREATE SCHEMA sort
GO

SELECT
		website.name AS websiteName
		,website.url AS websiteUrl
		,tag.tag AS tagTag
		,category.category AS categoryCategory
		,JobTitle.title AS JobTitleTitle
		,currency.code AS currencyCode
		,company.building AS companyBuilding
		,company.city AS companyCity
		,company.name AS companyName
		,company.street AS companyStreet
		,jobOffer.ifRemote AS ifRemote
		,jobOffer.postingDate AS postingDate
		,jobOffer.retrievingDate AS retrievingDate
		,jobOffer.salaryMax AS salaryMax
		,jobOffer.salaryMin AS salaryMin
INTO sort.unsortedData
FROM o.jobOffer
JOIN o.currency ON currency.ID = jobOffer.currencyID
JOIN o.company ON company.ID = jobOffer.companyID
JOIN o.JobTitle ON JobTitle.ID = jobOffer.jobTitleID
JOIN o.website ON website.ID = jobOffer.websiteID
JOIN o.jobOfferTag jot ON jot.jobOfferID = jobOffer.ID
JOIN o.tag ON tag.ID = jot.tagID
JOIN o.category ON category.ID = jobOffer.categoryID
WHERE 1=2

;

/*
SELECT ','+TABLE_NAME+'.'+COLUMN_NAME+' AS '+
	CASE WHEN TABLE_NAME != 'jobOffer'
	THEN TABLE_NAME+UPPER(LEFT(COLUMN_NAME,1))+SUBSTRING(COLUMN_NAME,2,400)
	ELSE COLUMN_NAME
	END
FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'o' AND COLUMN_NAME not like '%ID'
*/