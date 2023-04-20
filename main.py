# from typing import Union
from fastapi import FastAPI, UploadFile, File
import shutil
import os
from course_recommender import main

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}

@app.post("/fetch-course-recommendations")
def fetch_couse_recommendation(file: UploadFile = File(...)):
    file_location = f"course_recommender/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    response = main.main()
    os.remove(file_location)
    
    return {"success": True, "data": response}
    

