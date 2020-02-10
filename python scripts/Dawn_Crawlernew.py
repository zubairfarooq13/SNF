import bs4
import requests
import os
import time
import Db_Handlernew
import Preprocessingnew

class Dawn_Crawler:
#    url="https://www.dawn.com/newspaper/national/2019-04-01/"
#    url="https://www.dawn.com/newspaper/sport/2019-02-03"
    data=""
    inner_html_for_getting_urls=""
    url_list = []
    inner_html_for_data=""
    header_html_container=""
    heading=""
    author=""
    timestamp=""
    categories=""
    web_name=""
    content_list= []
    myheading = ""
    my_content=""
    a = 2 #2
    
    b = 0
    b = ('%02d' % a) #02
    
    
    def __init__(self):
        os.environ["HTTP_PROXY"]="<yourproxy>"         #--play with firewalls
        while(True):
            self.url="https://www.dawn.com/newspaper/sport/2019-03-{}/".format(self.b)
            print(self.url)
            self.a = self.a + 1
            self.b = ('%02d' % self.a)
            
            print(self.b)
            if(self.a is 10):
                break
            self.get_Inner_html()
        
    def get_Inner_html(self):
        data=requests.get(self.url)
        self.inner_html_for_getting_urls=bs4.BeautifulSoup(data.text,'html.parser')
        self.get_urls()
        
    def get_urls(self):
        news_container = self.inner_html_for_getting_urls.find_all('div', class_="row no-gutters")
        layer=news_container[1]
        article=layer.find_all('article')
        for container in article:
            link =  container.h2.a['href']
#            print(link)
            self.url_list.append(link)
            
    def get_header(self):
        try:
            #---------------Heading------------------#
            self.heading=self.inner_html_for_data.find('div',class_="template__header").h2.a.text.replace(": source","")
            print(self.heading)
            self.get_author()
        except:
           print(self.inner_html_for_data)
           self.heading=self.inner_html_for_data.find('div',class_="template__header").find('h2', class_="story__title").text.replace(": source","") 
           print("heading" + link_loop)
           self.get_author()
        
    def get_author(self):
        self.header_html_author=self.inner_html_for_data.find('div',class_="template__header")
        #---------------Author------------------#
        try:
            author=self.header_html_author.find("span", class_="story__byline").a.text.replace("'s","").replace(" | ","")
            print(author)
            self.get_timestamp()
        except:
            print("Author not found" + link_loop)
            self.get_timestamp()
        
    def get_timestamp(self):
        self.header_html_timestamp=self.inner_html_for_data.find('div',class_="template__header")
        #---------------TimeStamp------------------#
        try:
            self.timestamp=self.header_html_timestamp.find("span", class_="story__time").text.replace("Updated ","")
    #        print(timestamp)
            self.get_categories()
        except:
            print("Timestamp" + link_loop)
            self.get_categories()
        
    def get_categories(self):
        self.categories="National"
#        print(self.categories)
        self.get_webName()
    
    def get_webName(self):
        self.web_name=self.inner_html_for_data.find('h1',class_="text-hide").text.strip().replace("/n","")
        print(self.web_name)
        self.get_content()
        
    def get_content(self):
        content_html_container=self.inner_html_for_data.find('div', class_="template__main")
        content=content_html_container.find_all('div',class_="story__content")

        for list_p in content:
            p=list_p.find_all('p')
            for li in p:
                  p=li.text
#                  print(p)
                  self.content_list.append(p)
        #---------retrieve content from list and concatenate-----------#
        increment=0          
        while increment<len(self.content_list):
            p_loop=self.content_list[increment]
            self.my_content=self.my_content+" "+p_loop
#            print(self.my_content)
            increment=increment+1
            
            
            
    # -------------- Main Start ----------------#
Crawler=Dawn_Crawler() 

inc=0
while inc<len(Crawler.url_list):
    link_loop=Crawler.url_list[inc]
    print("url  " + link_loop)
    data_loop=requests.get(link_loop)
    time.sleep(2)
    Crawler.inner_html_for_data=bs4.BeautifulSoup(data_loop.text, 'html.parser')
    Crawler.get_header()
    scraped_content = Preprocessingnew.cleaning(Crawler.my_content)
    scraped_content = Preprocessingnew.get_token(scraped_content)
    scraped_content = Preprocessingnew.get_stopWords(scraped_content)
    scraped_content = Preprocessingnew.get_stemming(scraped_content)
    
    insertion=Db_Handlernew.Db_Handler(Crawler.heading,Crawler.author,Crawler.timestamp,Crawler.categories,Crawler.my_content,scraped_content,Crawler.web_name)
    insertion.insert_authors()
    insertion.insert_categories()
    insertion.insert_webName()
    insertion.insert_newsDetail()
    Crawler.my_content=""
    Crawler.content_list.clear()
    
    inc=inc+1 
    
    