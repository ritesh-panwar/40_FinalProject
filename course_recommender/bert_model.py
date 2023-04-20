from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
df = pd.read_csv("course_descriptions.csv", encoding= 'ISO-8859-1', low_memory=False, error_bad_lines=False)
courses = list(df["Course"].unique())
model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')

def sim_score(course_list, input):
    text_list = []
    for course in course_list:
        if course not in course_list:
            continue
        text_list.append(df.iloc[course]["Description"])
    embeddings = model.encode(text_list)
    given_vector = np.mean(embeddings, axis=0)
    input_embedding = model.encode(df.iloc[input]["Description"])
    return np.dot(given_vector,input_embedding)/(norm(given_vector)*norm(input_embedding))

def main():
    courses_list = ['CSE101', 'CSE201', 'MTH203', 'CSE641', 'SSH325', 'CSE564']
    input_course = 'CSE643'
    score = sim_score(courses_list, input_course)
    print("Course Score:", score)

if __name__ == '__main__':
    main()