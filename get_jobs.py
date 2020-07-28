#################################
#  This module will create a file that scrap for jobs from some of the main job searching websites
#  Based on experience and habbit, I choose to use Indeed and Workopolis
#  
# Design thinking: 
# What are the key words, how to filter for information that I need
# Which language shall I use? Is SQL a better choice for storing data?
# 
#################################
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

data = pd.DataFrame(['Title','Company', 'Description', 'Salary', 'Date Posted', 'Remote'])

def cleaned(tag): return tag.text.replace('\n', '').replace('-',' ').strip()

fdate = date.today()

for i in range(0, 100, 10):
    driver.get(
        'https://ca.indeed.com/jobs?q=Analyst&sort=date&l=Toronto%2C+ON&fromage=14&start='+str(i))
    driver.implicitly_wait(4)

    all_jobs = driver.find_elements_by_class_name('row')

    for job in all_jobs:

        soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
        
        try:
            title = cleaned(soup.find(name="a", attrs={"data-tn-element": "jobTitle"}))
        except:
            title = 'None'

        try:
            company = cleaned(soup.find(class_="company"))
        except:
            company = 'None'

        try:
            salary = int(cleaned(soup.find(class_="salary")))
        except:
            salary = 'None'

        try:
            days = cleaned(soup.find('span',{'class': 'date'}))
        except:
            days = 'None'

        try:
            remote = cleaned(soup.find(class_="remote"))
        except:
            remote = 'None'
            
        
        sum_div = job.find_elements_by_class_name('summary')[0]
        try:
            sum_div.click()
        except:
            close_button = driver.find_elements_by_class_name(
                'popover-x-button-close')[0]
            close_button.click()
            sum_div.click()

        job_desc = driver.find_element_by_id('vjs-desc').text.strip()

        data = data.append({'Title': title, 'Company': company, 'Description': job_desc, \
                            'Salary': salary,'Date Posted': days, 'Remote': remote},ignore_index=True)

# store data into csv format
data.to_csv(f'Analyst Jobs-{fdate}.csv')

if __name__=='__main__':
    file = get_jobs(date, link)
