from bs4 import BeautifulSoup # Import for Beautiful Soup
import requests # Import for requests
import lxml # Import for lxml parser
import datetime
from datetime import datetime
import csv
from csv import writer
import pandas as pd
import numpy as np
import re
from selenium.common.exceptions import NoSuchElementException
import boto3
from io import StringIO
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait as wait

class EventsWebScraper:
    def scrape_events_data(self, destinationIDs):
        def __init__(self, destinationIDs):
            self.destinationIDs = destinationIDs
        '''Scrape all event title and event URLs and add to df'''
        for destinationID in destinationIDs:
            global driver
            try:
                main_link = f"https://10times.com/{destinationID}"
                driver= webdriver.Chrome(r'C:/home/nileka/anaconda3/lib/python3.9/site-packages/selenium/webdriver/chrome/webdriver.py')
                driver.get(main_link)
                repeated = False
                while True:
                    # Scroll to the bottom of the page
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    # Check if the page has reached the end (no more scrolling possible)
                    end_of_page = driver.execute_script("return window.innerHeight + window.pageYOffset >= document.body.offsetHeight;")

                    driver.execute_script("window.scrollTo(0, 0);") #scroll up 
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll down again
                    time.sleep(2)
                    # Check if the page has reached the end (no more scrolling possible)
                    end_of_page = driver.execute_script("return window.innerHeight + window.pageYOffset >= document.body.offsetHeight;")
                    repeated = True
                    try:
                        driver.implicitly_wait(0)
                        button_element= driver.find_element("xpath", '/html/body/div[7]/div/div/div/div[1]/button')
                        driver.execute_script("arguments[0].click();",button_element)
                    except NoSuchElementException:
                        pass            
                    try:
                        driver.implicitly_wait(0)
                        button_element= driver.find_element("xpath", '/html/body/div[6]/div/div/div/div[1]/button')
                        driver.execute_script("arguments[0].click();",button_element)
                    except NoSuchElementException:
                        pass  

                    try:
                        driver.implicitly_wait(0)
                        button_element= driver.find_element("xpath", '/html/body/div/div[1]/div/div[2]/span')
                        driver.execute_script("arguments[0].click();",button_element)
                    except NoSuchElementException:
                        pass

                    try:
                        driver.implicitly_wait(0)
                        button_element2= driver.find_element("xpath", '/html/body/div[2]/button')
                        driver.execute_script("arguments[0].click();",button_element2)
                    except NoSuchElementException:
                        pass         

                    if end_of_page:
                        break                

                # Make it a soup
                soup = BeautifulSoup(driver.page_source,'html.parser')
                event_titles_df = pd.DataFrame(columns=['Event_Title','Event_URL', 'Event_Type'])    
                events= soup.find_all('a', class_='text-decoration-none c-ga xn')
                for event in events:
                    try:
                        url= event.get('href')
                    except:
                        pass
                    try:
                        name= event.get('data-ga-label')
                    except:
                        pass             
                    try:
                        event_type= event.get('data-ga-action')
                    except:
                        pass                


                    event_titles_df = event_titles_df.append({'Event_Title':name,'Event_URL': url, 'Event_Type': event_type}, ignore_index=True)
                event_titles_df = event_titles_df.dropna()
                event_titles_df= event_titles_df[event_titles_df["Event_Title"].str.contains("Event_Title")==False]
                event_titles_df["Event_Title"] = event_titles_df["Event_Title"].apply(lambda x: x.replace("To", ""))
                event_titles_df= event_titles_df.reset_index(drop=True)
                event_titles_df= event_titles_df[event_titles_df['Event_Type'] =='Event Listing | Event Snippet']
                event_titles_df=event_titles_df.drop('Event_Type', axis=1)
                event_titles_df['Event_URL'] = event_titles_df['Event_URL'].str.replace(' ', '')

                links = event_titles_df["Event_URL"]

                event_details_df = pd.DataFrame(columns=['Search_Date', 'Date', 'Labels', 'Turnout', 'Latitude', 'Longitude', 'Address', 'Event_URL'])

                for link in links:
                    try:
                        driver= webdriver.Chrome(r'C:/home/nileka/anaconda3/lib/python3.9/site-packages/selenium/webdriver/chrome/webdriver.py')
                        driver.get(link)
                        def click_button():
                            try:
                                driver.implicitly_wait(5)
                                button_element= driver.find_element("xpath", '/html/body/div/div[1]/div/div[2]/span')
                                driver.execute_script("arguments[0].click();",button_element)
                            except NoSuchElementException:
                                pass

                            try:
                                driver.implicitly_wait(5)
                                button_element2= driver.find_element("xpath", '/html/body/div[2]/button')
                                driver.execute_script("arguments[0].click();",button_element2)
                            except NoSuchElementException:
                                pass



                        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                        information=soup2.find('table', class_='table noBorder mng w-100 trBorder')
                        location=soup2.find('div', class_='row fs-14 box p-0')
                        currentDate = datetime.now().strftime("%m-%d-%Y")


                        event_link = link

                        repeated = False
                        while True:  
                            try:
                                turnout=information.find('a', class_='text-decoration-none').text
                            except NoSuchElementException:
                                pass
                            try:
                                labels=information.find(id='hvrout2').text
                            except NoSuchElementException:
                                pass
                            try:
                                latitude=location.find('span', id='event_latitude').text
                            except NoSuchElementException:
                                pass           
                            try:
                                longitude=location.find('span', id='event_longude').text
                            except NoSuchElementException:
                                pass
                            try:
                                venue=location.find('div', class_='mb-1').text
                            except NoSuchElementException:
                                pass

                            try:
                                eventDate=soup2.find('span', class_='ms-1').text
                            except NoSuchElementException:
                                pass

                            if eventDate.endswith("Followers"):
                                eventDate=soup2.find('div', class_='header_date position-relative text-orange me-5').text
                            else:
                                break


                            if eventDate.strip() == "" or turnout.strip() == "" or labels.strip() == "" or latitude.strip() == "" or longitude.strip() == "" or venue.strip() == "":
                                click_button()
                                repeated= True
                            else:
                                break



                        event_details_df=event_details_df.append({'Search_Date': currentDate, 'Date': eventDate, 'Labels': labels, 'Turnout': turnout, 'Latitude': latitude, 'Longitude': longitude, 'Address': venue, 'Event_URL': event_link}, ignore_index=True)     
                    except:
                        pass

                df2=event_details_df
                df2=df2.drop_duplicates()
                df2=df2.replace('N/A',np.NaN)
                df2['Address']=df2['Address'].str.slice(start=2)
                df2['Address'] = df2['Address'].str.replace("nue", "Venue")
                df2['Date'] = df2['Date'].str.replace('LIVE', '')
                df2 = df2.reset_index(drop=True)
                df2['Date']=df2['Date'].str.replace("Add a Review","")
                df2['Date']=df2['Date'].str.replace("Add a review","")

                #clean date column and define start date and end date 
                dateRange= pd.DataFrame(df2['Date'].str.split('-',1).to_list(),columns = ['Start date','End date'])
                dateRange['End date'].fillna(dateRange['Start date'], inplace=True)
                dateRange[['End day','End month','End year']] = dateRange['End date'].str.extract(r"^(.*)\s+(\S+)\s+(\d+)$", expand=True)
                dateRange[['Start day','Start month','Start year']] = dateRange['Start date'].str.extract(r"^(.*)\s+(\S+)*\s+(\d+)*$", expand=True)
                dateRange['Start day'].fillna(dateRange['Start date'], inplace=True)
                dateRange['Start month'].fillna(dateRange['End month'], inplace=True)
                dateRange['Start year'].fillna(dateRange['End year'], inplace=True)
                dateRange['Start']=dateRange['Start day'].astype(str)+ " "+ dateRange['Start month'].astype(str)+" "+ dateRange['Start year'].astype(str)
                dateRange['End']=dateRange['End day'].astype(str)+" "+dateRange['End month'].astype(str)+" "+dateRange['End year'].astype(str)
                df2['Start date']= pd.to_datetime(dateRange['Start'])
                df2['End date']= pd.to_datetime(dateRange['End'])
                del df2['Date']  


                df2['Labels']=df2['Labels'].str.replace("Category & Type","")

                df2['Category'] = df2['Labels'].str.extract('(Conference|Trade Show)', expand=False)

                df2['Labels']=df2['Labels'].str.replace("IT","Information Technology")
                df2['Labels']=df2['Labels'].str.replace('Conference', '')
                df2['Labels']=df2['Labels'].str.replace('Trade Show', '')
                df2['Labels'] = df2['Labels'].replace(r"(\w)([A-Z])", r"\1 | \2", regex=True)
                df2= df2.assign(Labels=df2['Labels'].str.split('|')).explode('Labels')
                df2.reset_index(inplace=True)
                df2.index = np.arange(1, len(df2) + 1)
                df2['Turnout']=df2['Turnout'].str.replace("&","").replace("([A-Z][a-z]+)", "").replace("IT", "")
                df2['Turnout']=df2['Turnout'].str.replace("([A-Z][a-z]+)", "", regex=True)
                df2['Turnout']=df2['Turnout'].str.replace("IT", "")
                df2['Turnout']=df2['Turnout'].replace(r'^\s*$', np.nan, regex=True)
                df2 = df2.rename(columns = {'index':'Event ID'})

                destination_events_df = pd.merge(event_titles_df, df2, on='Event_URL')
                currentDate = datetime.now().strftime("%m-%d-%Y")
                destination_events_df.to_csv(f"Events_in_{destinationID}_10TimesSite_{currentDate}.csv", index = False)

            except:
                pass


        driver.quit()

