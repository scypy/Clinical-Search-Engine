import os
from Preprocessor import DataPreprocessor
from Indexing import IndexingModule
from Retrieval import RetrievalModule
from Evaluation import EvaluatorModule


#Instructions Available in README


print("Loading...")
print("---------------------")

#Query taken from topics.db (topic nr. 2)
query = "An elderly female with past medical history of right hip " \
        "arthroplasty presents after feeling a snap of her right leg and falling to the ground."

#tokenized_query = query.split(" ")
preprocessor = DataPreprocessor('new_documents.db')
tokenized_query = preprocessor.preprocess(query)


#Index already cached in pickle file, uncomment if you wish to create a new one

indexer = IndexingModule()
#indexer.index_documents()


#Initialize RetrievalModule and search with query

print("---------------------")
print("Retrieved Documents: \n")
retrieval = RetrievalModule()
results = retrieval.search(tokenized_query)
print(results)

print("---------------------")
print("Evaluation: \n")
# Initialize evaluation module
evaluation = EvaluatorModule()
results = evaluation.evaluate(retrieval)
print(results)


