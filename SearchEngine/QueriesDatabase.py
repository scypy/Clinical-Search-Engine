import sqlite3
import xml.etree.ElementTree as ET

#This file used to parse the topics file published by TREC

conn = sqlite3.connect('queries.db')
conn.execute('''CREATE TABLE queries (topic_num INTEGER PRIMARY KEY, summary TEXT)''')

#dir must be pointing to "topics.nxml" file
tree = ET.parse('data/topics.nxml')
root = tree.getroot()

for topic in root.findall('.//topic'):
    topic_num = int(topic.get('number'))
    summary = topic.findtext('.//summary')
    conn.execute("INSERT INTO queries (topic_num, summary) VALUES (?, ?)", (topic_num, summary))
    conn.commit()

conn.close()

