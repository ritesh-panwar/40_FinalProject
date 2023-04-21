# from typing import Union
from fastapi import FastAPI, UploadFile, File, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from starlette.responses import RedirectResponse
from typing import List, Optional
import shutil
import os
from course_recommender import main

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

courseRequest = {"status": "initial", "data": {}}

@app.get("/", response_class=RedirectResponse)
async def home(request: Request):
    response = templates.TemplateResponse("index.html", {"request": courseRequest})
    courseRequest['status'] = "init"
    courseRequest['data'] = {}
    return response

@app.post("/fetch-course-recommendations")
async def fetch_couse_recommendation(request: Request, file: UploadFile = File(...), checkboxCSE: str = Form(default=None), checkboxECE: str = Form(default=None), checkboxMTH: str = Form(default=None), checkboxBIO: str = Form(default=None), checkboxDES: str = Form(default=None), checkboxSSH: str = Form(default=None), checkboxOTHERS: str = Form(default=None)):
    #Saving Uploaded File
    file_location = f"course_recommender/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    #Interest Departments List
    interest_departments = []
    if checkboxCSE:
        interest_departments.append(checkboxCSE)
    if checkboxECE:
        interest_departments.append(checkboxECE)
    if checkboxMTH:
        interest_departments.append(checkboxMTH)
    if checkboxBIO:
        interest_departments.append(checkboxBIO)
    if checkboxDES:
        interest_departments.append(checkboxDES)
    if checkboxSSH:
        interest_departments.append(checkboxSSH)
    if checkboxOTHERS:
        interest_departments.append(checkboxOTHERS)

    #User Input Display
    print("Uploaded File Name:", file.filename)
    print("Interest Departments", interest_departments)

    #Passing the input in the course recommender function
    try:
        response = main.main(file.filename, interest_departments)
        print(response)
        courseRequest['status'] = 'success'
        courseRequest['data'] = response
    except:
        courseRequest['status'] = "fail"

    #Removing current file
    os.remove(file_location)

    redirect_url = request.url_for('home')
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)  

@app.post("/user-input/")
def user_input(file: UploadFile = File(...), checkboxCSE: str = Form(default=None), checkboxECE: str = Form(default=None), checkboxMTH: str = Form(default=None), checkboxBIO: str = Form(default=None), checkboxDES: str = Form(default=None), checkboxSSH: str = Form(default=None), checkboxOTHERS: str = Form(default=None)):
    print(file.filename)
    print("checkBoxCSE", checkboxCSE)
    print("checkBoxECE", checkboxECE)
    print("checkBoxMTH", checkboxMTH)
    print("checkBoxBIO", checkboxBIO)
    print("checkBoxDES", checkboxDES)
    print("checkBoxSSH", checkboxSSH)
    print("checkBoxOTHERS", checkboxOTHERS)
    return {"success": True}
    

