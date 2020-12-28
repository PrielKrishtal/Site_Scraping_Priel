import csv

from bs4 import BeautifulSoup

from selenium import webdriver 

from webdriver_manager.chrome import ChromeDriverManager




def get_url(search_text):
    
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    product = search_text.replace(' ', '+')
    
    
    url = template.format(product)
    
    
    url += '&page{}'
        
    return url

def extract_record(item):
    """Extract and return data from a single record"""
    
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    try:
        
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
        
    result = (description, price, rating, review_count, url)
    
    return result






def main(search_term):
    
    # opening chrome tab
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    records = []
    url = get_url(search_term)
    
    #collecting info from each page
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    
    driver.close()
    
    #saving the results to the table
    with open('SearchResultTable.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Review Amount', 'Link'])
        writer.writerows(records)


    with open('SearchResultTable.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      prices=[]
      for row in reader:
          rw_price=(float(row[('Price')].replace("$", "")))
          prices.append(rw_price)
       
      print(" ")
      print("out of ", len(prices) , " results")
      print ("The highest price is : ", max(prices),"$")
      print ("The lowest price is : ", min(prices),"$")
      print("The avg price is : ", round(sum(prices) / len(prices), 2),"$")
     

     
   
  



        


 # enter the product you want to search
main("adidas shoes")














