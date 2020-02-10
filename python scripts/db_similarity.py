import db_data
import mysql.connector
data = []
ids = []
getter = db_data.DataPreprocessing()
old_data = getter.get_Content()
for i in old_data:
#       j = data_preprocessing.cleaning(i[1])
#       j = data_preprocessing.get_token(i[1])
#       j = data_preprocessing.get_stopWords(i[1])
#       j = data_preprocessing.get_stemming(i[1])
        ids.append(i[0])
        data.append(i[1])

cnx = mysql.connector.connect(host='127.0.0.1',
                              database='web_data',
                              user='root', 
                              password='admin',
                              use_pure=True
                              )
cursor = cnx.cursor(prepared=True)
cursor = cnx.cursor(buffered=True)
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data)
from sklearn.metrics.pairwise import cosine_similarity
print("total post", len(data))
for i in range(0, len(data)):
    for j in range(0, len(data)):
        if i!=j:
            simi = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[j:j+1])
            scraped_id = ids[i]
            db_post_id = ids[j]
            result_content="insert into similarity (scrapednewsID, othersnewsID, score) VALUES (%s, %s, %s)"
            insert_simi = (scraped_id, db_post_id, float(simi[0][0]))
            cursor.execute(result_content, insert_simi)
cnx.commit()