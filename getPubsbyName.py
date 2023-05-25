from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#function that given an name input, open up chrome and retrive all the public records

#For each auther, We need to store the following information: People and work
#1. author name
#2. author's all paper details
#3. author's collaboration network
#4. author's citation network

def getPubKeys(scholar_name):
    print('Starting the web scapper...')
    #open Chrome
    driver= webdriver.Chrome()
    driver.get(f"https://scholar.google.com/")
    search_field = driver.find_element(By.ID, 'gs_hdr_tsi')
    #In put the name in the search box
    search_field.send_keys(scholar_name)
    # Perform the search by pressing Enter
    search_field.send_keys(Keys.RETURN)
    #wait for the google research result page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'gs_res_ccl')))
    #locate the author page link
    author_page=driver.find_elements(By.LINK_TEXT,scholar_name)
    #click on the author page
    author_page[0].click()
    #wait for the author detail page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'YEAR')))
    #selenium click on the "SHOW MORE" button
    show_more=driver.find_elements(By.ID,'gsc_bpf_more')
    #click until the bottom of search is reached
    while show_more[0].is_enabled():
        show_more[0].click()
        time.sleep(5)
        show_more=driver.find_elements(By.ID,'gsc_bpf_more')
    
    #Each paper needs storage for the following information:
    #1. paper title
    #2. author names
    #3. publication date
    #4. Publish venue
    #5. Description:Abstract
    #6. cited number
    author_name_all={}
    Paper_details={}

    #click on each paper to get paper details page
    p_detail=driver.find_elements(By.CLASS_NAME,'gsc_a_at')
    print(len(p_detail))

    #create a for loop to get the each paper details
    for p in p_detail:
        #click on the paper
        #print(p.text)
        p.click()
        print('click')
        #wait for the paper detail page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'gsc_oci_table')))
        #get the paper title
        pub_title=driver.find_elements(By.ID,'gsc_oci_title')

        publication_details=driver.find_elements(By.ID,'gsc_oci_table')

        #split the publication details by \n
        publication_details=publication_details[0].text.split('\n')

        #create a for loop to check the column name and store the data in the map
        for i in range(len(publication_details)):
            if publication_details[i]=='Authors':
                pub_authors=publication_details[i+1]
            elif publication_details[i]=='Publication date':
                pub_date=publication_details[i+1]
            elif publication_details[i]=='Total citations':
                pub_citation=publication_details[i+1]
            elif publication_details[i]=='Publisher':
                pub_venue=publication_details[i+1]
            elif publication_details[i]=='Description':
                pub_abstract=publication_details[i+1]
        author_name=pub_authors.split(',')
        #get rid of the space in the front and end of the name
        author_name=[name.strip() for name in author_name]

        #add the author names to the list
        for name in author_name:
            if name in author_name_all:
                author_name_all[name]+=1
            else:
                author_name_all[name]=1

        #store the paper details in the map
        Paper_details[pub_title[0].text]={'title':pub_title[0].text,'Authors':pub_authors,'Publication date':pub_date,'Total citations':pub_citation,'Publisher':pub_venue,'Description':pub_abstract}
        
        driver.back()
        wait = WebDriverWait(driver, 100)
       

    #print the paper details
    print(Paper_details)

    #find the paper list
    papers=driver.find_elements(By.CLASS_NAME,'gsc_a_tr')
    #print the count of papers
    print(len(papers))
    #store all the author names and count the numbers as maps
    #create a map to store all the author names
    
    #print the author name map sorting from the most related
    print(sorted(author_name_all.items(), key=lambda x: x[1], reverse=True))


    time.sleep(10)
    driver.quit()
    return Paper_details




if __name__ == "__main__":
    getPubKeys("Heather Culbertson")


