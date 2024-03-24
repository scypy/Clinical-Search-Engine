import sqlite3
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class DataPreprocessor:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.tokenizer = word_tokenize
        self.stopwords = set(stopwords.words('english'))

    def preprocess(self, text):
        # remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # convert to lowercase
        text = text.lower()
        # tokenize
        tokens = self.tokenizer(text)
        # remove stopwords
        tokens = [t for t in tokens if t not in self.stopwords]
        # join tokens back into text
        text = " ".join(tokens)
        return text

    def update_database(self, data, conn):
        c = conn.cursor()
        c.executemany("UPDATE documents SET text=? WHERE id=?", [(text, id_) for id_, text in data])
        conn.commit()

    def process_documents(self):
        conn = sqlite3.connect('new_documents.db')
        c = conn.cursor()
        c.execute("SELECT id, text FROM documents")
        for row in c.fetchall():
            id_, text = row
            processed_text = self.preprocess(text)
            c.execute("UPDATE documents SET text = ? WHERE id = ?", (processed_text, id_))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    processor = DataPreprocessor('new_documents.db')
    processor.process_documents()
