#################################
#  This module will create a file that scrap for jobs from some of the main job searching websites
#  Based on experience and habbit, I choose to use Indeed and Workopolis
#  
# Design thinking: 
# What are the key words, how to filter for information that I need
# Which language shall I use? Is SQL a better choice for storing data?
# 
#################################
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

# if webdriver exist
# driver = webdriver.Chrome(PATH='YOUR_LOCAL_PATH')

# In my case, can't find it at first
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())


def cleaned(tag): return tag.text.replace('\n', '').strip()

def get_jobs(title):    
    
    data = pd.DataFrame(['Title','Company', 'Description', 'Salary', 'Date Posted', 'Remote'])
    
    for i in range(0, 3950, 10):
    
        driver.get(
            'https://ca.indeed.com/jobs?q='+title+'&sort=date&l=Toronto%2C+ON&fromage=14&start='+str(i))
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

if __name__=='__main__':
    from datetime import date
    fdate = date.today()
    job_title = input("Enter your desired job title here:")
    data = get_jobs(job_title)
    data.to_csv(f'{job_title} Jobs-{fdate}.csv')
