**CSE508: Information Retrieval Final Project**

**Introduction** \
Our Information Retrieval Project is an online tool that enables users to identify relevant courses based on their preferences and areas of interest. FastAPI, a cutting-edge, quick web framework for Python 3.7+ API development that is based on common Python type hints, was used to construct the project. High performance, automated documentation, and simple connection with other programmes and libraries are just a few advantages offered by FastAPI. \

We were able to design this project with FastAPI and end up with a dependable, scalable, and user-friendly online application that offers users precise and individualised course suggestions. With the aid of FastAPI's capabilities, we were able to develop a strong recommendation system that can adjust to the user's preferences and deliver pertinent results in real-time.

**Requirements** \
To run the Information Retrieval Project, you will need: Python 3.7+, FastAPI, Uvicorn and more. \

To install the required packages, run: \
`pip install -r requirements.txt`

**Usage** \
To start the application, navigate to the project directory and run the following command: \
`uvicorn main:app --reload`


**File Structure** \
The project directory consists of main.py file containing primary fastapi framework implementation, course_recommender folder containing the whole course retrieval system mechanism files including transcript extraction and bert model. The static and templates contains the front-end framework files, and requirements.txt file contains the environment dependencies to run the system.

**API endpoints** \
The project consists of two primary API endpoints developed with fastapi framework to render home HTML page, and execute the course retrieval task based on the user inputs respectively.

**Data Processing** \
The programme is a Python script that extracts data from a PDF file containing a student's academic transcript using the pydocparser package. A Pandas DataFrame that represents the academic record is created once the extracted data has been analysed and sanitised.

**Machine Learning/Artificial Intelligence** \
This section of the code imports the relevant libraries, including SentenceTransformer, Pandas, and Numpy. SentenceTransformer is a library for sentence and text embeddings. Numpy is used for numerical operations, Pandas is used for data manipulation. Additionally, cosine similarity is taken into account while calculating course matching score.

**Front-End** \
The Information Retrieval Project's front-end was created to offer users a simple and entertaining user experience for registering their choices for courses and browsing suggested courses.

HTML, CSS, and Bootstrap were used to create the front-end. The webpage's HTML structure, CSS styling, and Bootstrap responsive design and other stylistic elements were all created using these three languages.

**Conclusion** \
The web-based application has a site where users may enter their transcript preferences and preferred courses. The user interface comprises of a form where the user may select their interest departments and submit their transcript.

After the user enters their choices, the application's backend creates a list of suggested courses that correspond to their input. The user may examine information about each course, including the title, code, and score, on the same page that lists the recommended courses.

In general, the Information Retrieval Project's front-end offers a simple-to-use and aesthetically pleasing user interface that improves the user experience and makes it simple to identify pertinent courses.

