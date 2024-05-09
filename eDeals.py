#imports
import time
from bs4 import BeautifulSoup
import csv
import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])




#globals/filepaths

EXPORT = "export.xlsx"
EXPORT_CSV = "export.csv"
specials_page = []



def getspecials(url, StoreID):
    #Launch Chrome
    driver = webdriver.Chrome(service=service, options=options)
    

    # Go To Store Main Menu
    #URL = "https://www.papajohns.com/order/viewStoreMenu/CARRYOUT/BUSINESS/190/"
    driver.get(url)
    
    time.sleep(1)

    #Close Cookies Window
    #ccb = driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
    #ccb.click()
    #time.sleep(1)

    #Close LTO Window
    #cjb = driver.find_element(By.XPATH, '//*[@id="pizza-img"]/div[2]/div/button')
    #cjb.click()
    #time.sleep(2)

    #Go To Specials Page
    spl = driver.find_element(By.XPATH, '/html/body/div[2]/header/section[2]/nav/ul/li[2]/a')
    spl.click()

    time.sleep(3)

    #Locate & Parse Specials HTML
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    cards = soup.find_all('div',{'class':'card-details'})

    #Extract Offers & Prices
    for card in cards:
        data_dict              = {}
        data_dict['store']     = StoreID
        data_dict['offer']     = card.find('h2').text
        data_dict['description'] = card.find('p',{'class':'description'}).text
        try:
            data_dict['price']     = card.find('span',{'class':'price'}).text
        except:
            data_dict['price']     = card.find('span',{'class':'price'})
        specials_page.append(data_dict)
    time.sleep(1)
    driver.close()












#Get the store list
storeinput = input("Enter a list of stores seperated by a single space and/or commas, or enter the file path to a CSV file with all stores listed in the first column: ")

if ".csv" in storeinput:
    with open(storeinput,encoding='utf-8-sig') as storelist_file:
        storelist = []
        csv_reader = csv.reader(storelist_file,delimiter=',')
        for row in csv_reader:
            storelist.append(row[0])
elif ", " in storeinput:
    storelist = storeinput.split(", ")
elif "," in storeinput:
    storelist = storeinput.split(",")
else:
    storelist = storeinput.split(" ")


#Run the script at each store
for store in storelist:
    url = f"https://www.papajohns.com/order/viewStoreMenu/CARRYOUT/BUSINESS/" + str(store) +"/"
    print(f"Running store {store}...")
    getspecials(url, str(store))
    


#Save the export file
with open(EXPORT_CSV, mode='w',newline='') as csv_file:
    headers = ['store','offer','description','price']
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(specials_page)



#Wrapping up
print(f"Done! Saved the export to {EXPORT_CSV}")
input("Press enter to exit")