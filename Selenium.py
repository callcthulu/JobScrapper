from unittest.mock import inplace

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import codecs
from bs4 import BeautifulSoup
import MSDBConnector as mdc

columnList = ['company-address', 'age new', 'title', 'company-info', 'tag', 'salary',
              'company-name', 'salary-row', 'remote']


def getClasses(html):
    span = html.split('<span class="')
    allClasses = []
    for s in span:
        allClasses.append(s.split('"')[0])
    return list(set(allClasses[1:]))


def getValues(soup, classNames):
    def cleanValue(value):
        return value.replace(u'\uE0C8', '').replace(u'\uE0AF', '').lstrip().rstrip()

    dict = {}
    for className in classNames:
        allValues = soup.find_all("span", class_=className)
        if len(allValues) > 1:
            dict[className] = [cleanValue(value.text) for value in allValues]
        else:
            dict[className] = cleanValue(allValues[0].text)
    return dict


def prepareDataToDB(df):
    def checkIfAllColumnsExisting(checkedDF):
        for column in columnList:
            if column not in checkedDF.columns:
                checkedDF[column] = None
        return checkedDF

    def getNumber(string):
        return int(''.join([char for char in string.split() if char.isdigit()]))

    def getSalary(string):
        if '-' in string:
            result = [getNumber(salary) for salary in string.split('-')] + [string.split(' ')[-1].upper()]
        elif any(char.isdigit() for char in string):
            result = [getNumber(string), getNumber(string), string.split(' ')[-1]]
        else:
            result = [None, None, None]
        return pd.Series(result, index=['salaryMin', 'salaryMax', 'currency'])

    df = checkIfAllColumnsExisting(df)
    df['jobTitle'] = df['title']
    df[['salaryMin', 'salaryMax', 'currency']] = df['salary'].apply(lambda x: getSalary(x) if x is not None else None)
    df['name'] = df['company-name']
    df[['street', 'city']] = df['company-address'].str.split(",", n=1, expand=True)
    df['postingDate'] = df['age new'].apply(lambda x: str(pd.to_datetime('today') - pd.Timedelta(days=getNumber(x)))[0:-7] \
        if x[0].isdigit() else str(pd.to_datetime('today'))[0:-7])
    df['tags'] = df['tag'].apply(lambda x: x.lower() if x is not None else None)
    df['ifRemote'] = df['remote'].apply(lambda x: 0 if x is None else 1)
    df.drop(columns=columnList, axis=1, inplace=True)

    return df


"""
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

#to-do - start from main site, get categories, iterate over categories
"""
url = "https://justjoin.it/all/"
category = "data"
currentUrl = url+category
site = url.split("/")[2]

""""
browser.get(currentUrl)
offers = browser.find_elements_by_class_name("item")
for o in offers:
    html = o.get_attribute('innerHTML')
"""
html = """  <div class="company-logo-container">
    <img class="company-logo" ng-src="https://bucket.justjoin.it/offers/company_logos/thumb/1bf2daba450dc8892f8547f6f2fbfb65ca2e58cb.png?1559640748" src="https://bucket.justjoin.it/offers/company_logos/thumb/1bf2daba450dc8892f8547f6f2fbfb65ca2e58cb.png?1559640748">
  </div>
  <div class="item-row">
    <div class="primary-line">
      <span class="title">
        Data Engineer
      </span>
      <!---->
      <div class="flex-right">
        <span class="salary-row">
          <!----><span class="salary" ng-if="::$ctrl.offer.salaryFrom!=null">13 000 - 20 000 PLN</span><!---->
          <!---->
        </span>
        <span class="age new" ng-class="::{ 'new':$ctrl.offer.isNew() }">New</span>
      </div>
    </div>
    <div class="secondary-line">
      <span class="company-info">
        <span class="company-name">
          <i class="material-icons company-icon">
            
          </i>
          Showpad
        </span>
        <span class="company-address">
          <i class="material-icons marker-icon">
            
          </i>
          1 Swobodna Street, Wrocław
        </span>
      </span>
      <div class="tags">
        <!---->
        <!----><span class="tag" ng-repeat="skill in ::$ctrl.offer.skills">MongoDB</span><!----><span class="tag" ng-repeat="skill in ::$ctrl.offer.skills">Spark</span><!----><span class="tag" ng-repeat="skill in ::$ctrl.offer.skills">Hadoop</span><!---->
      </div>
    </div>
  </div> """

classes = getClasses(html)
soup = BeautifulSoup(html)
df = pd.DataFrame(data=getValues(soup, classes), columns=classes)
df.insert(loc=len(df.columns), column='site', value=site)
df.insert(loc=len(df.columns), column='url', value=currentUrl)
df.insert(loc=len(df.columns), column='category', value=category)
df = prepareDataToDB(df)
# print(df)

df.to_csv('rawDataExample.csv', ';')

path = 'C:/Users/oleli/Desktop/jobScrapper/settings.txt'
con = mdc.MSDBConnector()
con.setPath(path)

# test
# con.setSQL("SELECT @@SERVERNAME")
# result = con.connect(get=1)
# print(result)

sql = """
        INSERT INTO [JobsDB].[sort].[unsortedData] (
           [websiteName]
          ,[websiteUrl]
          ,[categoryCategory]
          ,[JobTitleTitle]
          ,[salaryMin]
          ,[salaryMax]
          ,[currencyCode]
          ,[companyName]
          ,[companyStreet]
          ,[companyCity]
          ,[postingDate]
          ,[tagTag]
          ,[ifRemote] )
        VALUES (
                %s
                );
        """
for row in df.iterrows():
    values = ''
    for item in row[1]:
        values = values + ",'" + str(item) + "'"
    #print(sql % (values[1:],))
    con.setSQL((sql % (values[1:],)))
    con.connect()
    """site;url;category;category;jobTitle;salaryMin;salaryMax;currency;name;street;city;postingDate;tags;ifRemote"""
    # print(row)
    # for col, item in row:
    #      values = values + ",'" + str(item) + "'"
    # print(values)
    # con.setSQL((sql %(values[1:0],)))
    # con.connect()


# for key,value in dict.items():
#    if type(value) is list:
#        print(key+ " : " + ", ".join(value))
#    else:
#        print(key + " : "+value)
# title = soup.find_all("span",class_="title")
# for t in title:
#    print(t.text)
# do magic wtih bs4
# save as dataframe + datesb
# dataframe to db then

""""
file_object = codecs.open("site.txt", "w", "utf-8")
html = browser.page_source
file_object.write(html)
"""
# with open("site.txt", "w+", "utf-8") as f:
#    f.write(page)
