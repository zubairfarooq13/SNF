import os
import mysql.connector

class DataPreprocessing:
    cursor = ""
    cnx = ""
    var= ""
    def __init__(self):
         os.environ["HTTP_PROXY"]="<yourproxy>"         #--play with firewalls
         self.cnx = mysql.connector.connect(host='127.0.0.1',
                              database='web_data',
                              user='root', 
                              password='admin',
                              use_pure=True
                              )
         self.cursor = self.cnx.cursor(prepared=True)
         self.cursor = self.cnx.cursor(buffered=True)
         
    def get_Content(self):
        result_content="SELECT news_id, content_preprocess FROM news_detail"
        self.cursor.execute(result_content)
        self.get_news_content=self.cursor.fetchall()
        return self.get_news_content
    
        
