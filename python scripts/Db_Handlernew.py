import mysql.connector


class Db_Handler:
    cursor = ""
    cnx = ""
    heading=""
    author=""
    timestamp=""
    categories=""
    my_content=""
    my_preprocess_content = ""
    web_name=""
    authors_id=0
    categories_id=0
    web_id=0
    get_news_content=""
    
    def __init__(self,heading,author,timestamp,categories,my_content,my_preprocess_content,web_name):
        self.cnx = mysql.connector.connect(host='127.0.0.1',
                              database='web_data',
                              user='root', 
                              password='admin',
                              use_pure=True
                              )
        self.cursor = self.cnx.cursor(prepared=True)
        self.cursor = self.cnx.cursor(buffered=True)
        self.heading=heading
        self.author=author
        self.timestamp=timestamp
        self.categories=categories
        self.my_content=my_content
        self.my_preprocess_content=my_preprocess_content
        self.web_name=web_name
#        print("db class"+self.my_content)
   
    def insert_authors(self):
        #---------------  Authors   -------------------#
        authors_query="SELECT COUNT(name_authors) FROM authors where name_authors='"+self.author + "'"
        self.cursor.execute(authors_query)
        result_count_authors=self.cursor.fetchone()
        if(result_count_authors[0] == 0):
          sql_insertion_author = "INSERT INTO authors (name_authors) VALUES (%s)"
          insert_author = (self.author,)
          self.result_author  = self.cursor.execute(sql_insertion_author, insert_author)
          self.authors_id=self.cursor.lastrowid
          self.cnx.commit()
        else:
          result_id_authors="SELECT (id_authors) FROM authors where name_authors='"+self.author + "'"
          self.cursor.execute(result_id_authors)
          get_author_id=self.cursor.fetchone()
          self.authors_id=get_author_id[0]
             
    def insert_categories(self):
        #-----------------  Categories   -------------------#
        categories_query="SELECT COUNT(name_categories) FROM categories where name_categories='"+self.categories + "'"
        self.cursor.execute(categories_query)
        result_count_categories=self.cursor.fetchone()
        if(result_count_categories[0] == 0):
          sql_insertion_categories = "INSERT INTO categories (name_categories) VALUES (%s)"
          insert_categories = (self.categories,)
          self.result_categories  = self.cursor.execute(sql_insertion_categories, insert_categories)
          self.categories_id=self.cursor.lastrowid
          self.cnx.commit()
        else:
          result_categories_id="SELECT (id_categories) FROM categories where name_categories='"+self.categories + "'"
          self.cursor.execute(result_categories_id)
          get_categories_id=self.cursor.fetchone()
          self.categories_id=get_categories_id[0]
          
    def insert_webName(self):
        #-----------------  Categories   -------------------#
        web_query="SELECT COUNT(website_name) FROM web_name where website_name='"+self.web_name + "'"
        self.cursor.execute(web_query)
        result_count_web=self.cursor.fetchone()
        if(result_count_web[0] == 0):
          sql_insertion_web = "INSERT INTO web_name (website_name) VALUES (%s)"
          insert_web = (self.web_name,)
          self.result_web  = self.cursor.execute(sql_insertion_web, insert_web)
          self.web_id=self.cursor.lastrowid
          self.cnx.commit()
        else:
          result_name_id="SELECT (name_id) FROM web_name where website_name='"+self.web_name + "'"
          self.cursor.execute(result_name_id)
          get_name_id=self.cursor.fetchone()
          self.web_id=get_name_id[0]
#          print(self.web_id)
   
    def insert_newsDetail(self):
        news_detail_query="INSERT INTO news_detail (`date`, heading, content, id_authors, id_categories,id_web, content_preprocess) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        insert_news=(self.timestamp,self.heading,self.my_content,self.authors_id,self.categories_id,self.web_id,self.my_preprocess_content)
        self.result  = self.cursor.execute(news_detail_query, insert_news)
        self.cnx.commit()
        
    

               
        
        
        
        
        
        