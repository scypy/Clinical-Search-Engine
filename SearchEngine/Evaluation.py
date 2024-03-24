import sqlite3
from pytrec_eval import RelevanceEvaluator


class EvaluatorModule:
    def __init__(self, qrels_path='data/relevancejudgement.txt', db_path='queries.db'):
        self.qrels_path = qrels_path
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect('queries.db')

    def get_all_queries(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT topic_num, summary FROM queries")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def load_qrels(self):
        with open('data/relevancejudgement.txt', 'r') as f:
            qrels_lines = f.readlines()

        qrels = {}
        for line in qrels_lines:
            split_line = line.strip().split()
            topic_no = split_line[0]
            pmcid = split_line[2]
            #print(pmcid)
            score = int(split_line[3])
            if topic_no not in qrels:
                qrels[topic_no] = {}
            qrels[topic_no][pmcid] = score

        return qrels


    def evaluate(self, retrieval, metrics=['recall', 'map', 'ndcg']):
        queries = self.get_all_queries()
        qrels = self.load_qrels()
        evaluator = RelevanceEvaluator(qrels, metrics)
        run = {}
        for qid, query in queries:
            topic_no = str(qid)
            ranked_doc_ids = retrieval.search(query)
            if topic_no not in run:
                run[topic_no] = {}
            for rank, doc_id in enumerate(ranked_doc_ids, 1):
                run[topic_no][str(doc_id)] = rank
        results = evaluator.evaluate(run)
        return results




