from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import codecs
from bs4 import BeautifulSoup

def getClasses(html):
    span = html.split('<span class="')
    allClasses = []
    for s in span:
        allClasses.append(s.split('"')[0])
    return list(set(allClasses[1:]))

def cleanValue(value):
    return value.replace(u'\uE0C8','').replace(u'\uE0AF','').lstrip().rstrip()


def getValues(soup,classNames):
    dict = {}
    for className in classNames:
        allValues = soup.find_all("span",class_=className)
        if len(allValues) > 1:
            dict[className] = [cleanValue(value.text) for value in allValues]
        else:
            dict[className] = cleanValue(allValues[0].text)
    return dict

"""
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

browser.get("https://justjoin.it/all/data")
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
df = pd.DataFrame(data=getValues(soup,classes), columns=classes)
#if 'remote' not in df.columns:
#    df.
df.to_csv('rawDataExample.csv',';')




#for key,value in dict.items():
#    if type(value) is list:
#        print(key+ " : " + ", ".join(value))
#    else:
#        print(key + " : "+value)
#title = soup.find_all("span",class_="title")
#for t in title:
#    print(t.text)
    #do magic wtih bs4
    #save as dataframe + datesb
    #dataframe to db then

""""
file_object = codecs.open("site.txt", "w", "utf-8")
html = browser.page_source
file_object.write(html)
"""
#with open("site.txt", "w+", "utf-8") as f:
#    f.write(page)
