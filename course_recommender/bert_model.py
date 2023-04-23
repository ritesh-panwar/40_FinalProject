from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np


def sim_score(rank_list, input, courses, df, model):
    text_list = []
    # score = []
    code_not_detected = []
    for code in rank_list:
        if code not in courses:
            for course in courses:
                if code in course:
                    text_list.append(df.loc[df['Course']==course]["Description"].to_string())
                    # print(code)
        else:
            text_list.append(df.loc[df['Course']==code]["Description"].to_string())
    
    if len(text_list) == 0:
        return 0
    
    input_desc = ""
    if input not in courses:
        for course in courses:
                if input in course:
                    input_desc = df.loc[df['Course']==course]["Description"].to_string()
    else:
        input_desc = df.loc[df['Course']==input]["Description"].to_string()

    if input_desc == "":
        return 0
    
    given_text = model.encode(text_list)
    given_vector = np.mean(given_text, axis=0)
    # print(given_vector.shape)
    # given_vector = np.mean(embeddings, axis=0)
    input_embedding = model.encode(input_desc)
    # print(input_embedding)
    cosine_score = (np.dot(given_vector,input_embedding)/(norm(given_vector)*norm(input_embedding)))
    score = ((cosine_score + 1)/2)*100
    
    return np.round(score, 2)

def matching_score(input_course, courses_list):
    # print(input_course, courses_list)
    df = pd.read_csv("course_recommender/course_descriptions.csv")
    # print(df.shape)
    df = df.dropna(subset=['Name', 'Course', 'Description'])
    courses = list(df["Course"].unique())
    for idx, course in enumerate(courses):
        courses[idx] = courses[idx].replace(" ", "")
    model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
    # courses_list = ['CSE101', 'CSE201', 'MTH203', 'CSE641', 'SSH325', 'CSE564']
    # input_course = 'CSE350'
    # print(df)
    score = sim_score(courses_list, input_course, courses, df, model)
    # print(score)
    return score

# matching_score("SSH700", ['CSE101', 'ECE111', 'CSE102', 'CSE112', 'SOC101', 'SSH101', 'CSE121', 'CSE201', 'CSE231', 'MTH203', 'CSE202', 'CSE222', 'MTH204', 'MTH377', 'CSE200A', 'BTP499', 'CSE343', 'CSE556', 'ESC207A', 'BIP399', 'BTP499', 'CSE344', 'CSE641', 'ECO201', 'SSH235'])
