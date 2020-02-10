import bs4
import requests
import os
import PT_Db_Handler

class PakistanToday_Crawler:
#    url="https://www.pakistantoday.com.pk/national/page/14/"
    url="https://www.pakistantoday.com.pk/sports/page/8/"
    data=""
    inner_html_for_getting_urls=""
    url_list = []
    inner_html_for_data=""
    header_html_container=""
    heading=""
    author=""
    web_name=""
    timestamp=""
    categories=""
    content_list= []
    my_content=""
    
    
    def __init__(self):
        os.environ["HTTP_PROXY"]="<yourproxy>"         #--play with firewalls
        self.get_Inner_html()
        
    def get_Inner_html(self):
        data=requests.get(self.url)
        self.inner_html_for_getting_urls=bs4.BeautifulSoup(data.text,'html.parser')
        self.get_urls()
        
    def get_urls(self):
        news_container = self.inner_html_for_getting_urls.find_all('div', class_="content-inner")
        layer=news_container[0]
        article=layer.find_all('article', class_="has-thumbnail")
        for container in article:
            link =  container.h2.a['href']
#            print(link)
            self.url_list.append(link)
            
    def get_header(self):
        header_html_heading=self.inner_html_for_data.find('header',class_="entry-header")
        #---------------Heading------------------#
        self.heading=header_html_heading.h1.text
        #self.heading=heading.replace(": source","")
        print("Heading: "+self.heading)
        self.get_author()
        
    def get_author(self):
        self.header_html_author=self.inner_html_for_data.find('header',class_="entry-header")
        #---------------Author------------------#
        author_html=self.header_html_author.find("div", class_="entry-meta capital")
        author=author_html.text.split('(')[0]#replace("by","").strip().replace("(Last Updated ","").replace(")","")
        self.author=author.replace("by","").replace(",","")
        #self.author=author_n[:-36]
        
        print("Author Name:  "+self.author)
        self.get_timestamp()
        
    def get_timestamp(self):
        self.header_html_timestamp=self.inner_html_for_data.find('header',class_="entry-header")
        #---------------TimeStamp------------------#
        timestamp_html=self.header_html_timestamp.find("div", class_="entry-meta capital").text
        self.timestamp=timestamp_html[timestamp_html.find(","):].replace(", (Last Updated ","").replace(")","")
        print("Time: "+ self.timestamp)
        self.get_categories()
        
    def get_categories(self):
        self.categories="Sport"
#        print("Catrogry "+self.categories)
        self.get_content()
        
    def get_webName(self):
        self.web_name=self.inner_html_for_data.find('a',class_="small-logo").text#.text.strip().replace("/n","")
        print("web name"+self.web_name)
        self.get_content()
        
    def get_content(self):
#        content_html_container=self.inner_html_for_data.find('header',class_="entry-header")
        content=self.inner_html_for_data.find_all('div', class_="entry-content")

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
Crawler=PakistanToday_Crawler() 
inc=0
while inc<len(Crawler.url_list):
    link_loop=Crawler.url_list[inc]
    url_loop=link_loop
    data_loop=requests.get(url_loop)
    Crawler.inner_html_for_data=bs4.BeautifulSoup(data_loop.text, 'html.parser')
    Crawler.get_header()
#    print("Main-category" + Crawler.categories)
#    print("Main-author" + Crawler.author)
#   print("Main-heading" + Crawler.heading)
#   print("Main-date" + Crawler.timestamp)
    insertion=PT_Db_Handler.PT_Db_Handler(Crawler.heading,Crawler.author,Crawler.timestamp,Crawler.categories,Crawler.my_content,Crawler.web_name)
    insertion.insert_authors()
    insertion.insert_categories()
    insertion.insert_webName()
    insertion.insert_newsDetail()
    
    
#    print(Crawler.my_content)
    
    Crawler.my_content=""
    Crawler.content_list.clear()
    
    inc=inc+1 
    
    