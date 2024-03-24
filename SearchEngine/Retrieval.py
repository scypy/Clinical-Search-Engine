import json
import pickle
import sqlite3
import nltk
from nltk.corpus import stopwords
from rank_bm25 import BM25Okapi
from collections import defaultdict
from Indexing import IndexingModule


class RetrievalModule:

    def search(self, query):
        query_tokens = query.split()
        # load cached index
        with open('bm25result', 'rb') as bm25result_file:
            bm25result = pickle.load(bm25result_file)
        with open('docids', 'rb') as doc_ids:
            doc_ids = pickle.load(doc_ids)
        scores = bm25result.get_scores(query_tokens)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        ranked_doc_ids = [doc_ids[i] for i in ranked_indices]
        return ranked_doc_ids[:10]
