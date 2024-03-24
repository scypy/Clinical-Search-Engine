import pickle
import sqlite3
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
from rank_bm25 import BM25Okapi
import csv

import sqlite3
from rank_bm25 import BM25Okapi

class IndexingModule:
    def init(self, db_path='new_documents.db'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect('new_documents.db')

    def get_all_documents(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text FROM documents")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def index_documents(self):
        docs = self.get_all_documents()
        texts = [doc[1].split() for doc in docs]
        self.bm25 = BM25Okapi(texts)
        #Tunable parameters, leave at default
        #self.bm25.k1 = 1.2
        #self.bm25.b = 0.5
        self.doc_ids = [doc[0] for doc in docs]
        #cache index on disk
        with open('bm25result', 'wb') as bm25result_file:
            pickle.dump(self.bm25, bm25result_file)

        with open('docids', 'wb') as docid_file:
            pickle.dump(self.doc_ids, docid_file)

