#Code for CSSS Branch
import pandas as pd
import numpy as np
import math
# import extract_transcript
from course_recommender import extract_transcript

import warnings
warnings.filterwarnings("ignore")


#Function to Handle SG and CW Credits
def fetch_SGCW_credits(df):

  sg_credits = len(df[ (df['Title of the Course'] == 'Self Growth') & (df['Grade'] == 'S')])
  df.drop(df[(df['Title of the Course'] == 'Self Growth') & (df['Grade'] == 'S')].index, inplace = True)

  cw_credits = len(df[ (df['Title of the Course'] == 'Community Work') & (df['Grade'] == 'S')])
  df.drop(df[(df['Title of the Course'] == 'Community Work') & (df['Grade'] == 'S')].index, inplace = True)

  if sg_credits > 2:
    sg_credits = 2
  if cw_credits > 2:
    cw_credits = 2

  df = df.reset_index()
  df.drop('index', axis =1, inplace=True)

  return sg_credits, cw_credits, df


#Function to Handle First Two Year Courses
def handle_first_two_year_courses(df):
  credits = 0
  courses = []
  backlogs = []

  for index, row in df.iterrows():
    if not row['Grade'] == 'F':
      credits += row['Credit']
      courses.append(row['Code'])
    else:
      backlogs.append(row['Code'])

  return credits, courses, backlogs


#Function to Handle Last Two Year Courses
def handle_last_two_year_courses(df, prev_courses, backlogs):
  credits = 0
  cse_credits = 0
  ssh_credits = 0
  eco_credits = 0
  courses = []
  
  two_level_courses = 0
  btp_terms = 0

  for index, row in df.iterrows():

    #Check if the course is an improvement or backlogs removal
    if row['Code'] in prev_courses:
      if row['Grade'] != "F":
        backlogs.remove(row['Code'])
      continue
    if row['Code'] in backlogs:
      credits += row['Credit']
      continue

    dep = row['Code'][:3]

    #Ignore course if F grade
    if row['Level'] == 2:
      two_level_courses += 1

    if row['Grade'] == "F" or two_level_courses > 4:
      continue

    if dep == "CSE" and row['Level'] > 2:
      cse_credits += row['Credit']
    elif (dep == "SSH" or dep == "SOC" or dep == "PSY" or dep == "MGT" or dep == "ENT") and row['Level'] > 2:
      ssh_credits += row['Credit']
    elif dep == "ECO":
      eco_credits += row['Credit']
    elif dep == "BTP" and row['Level']%1 == 0:
      btp_terms += 1

    isBTPDone = False
    if btp_terms >=2:
      isBTPDone = True


    credits += row['Credit']
    courses.append(row['Code'])

  
  return {
        "credits": credits,
        "cse_credits": cse_credits,
        "ssh_credits": ssh_credits,
        "eco_credits": eco_credits,
        "courses": courses,
        'backlogs': backlogs,
        "btp": isBTPDone
    }

#Core Function to Track Graduation Requirements and Retrieve Relevant Courses
def course_recommender(df, interest_deps):

  course_recom_response = {}
  course_recom_response['transcript_data'] = df.to_dict()
  #Fetching Semester to be considered for course suggestions
  req_sem = ""
  if len(df) != 0:
    sem_num = df["Semester"].iloc[-1]
    if(sem_num%2 == 0):
      req_sem = "Monsoon"
    else:
      req_sem = "Winter"
  else:
    req_sem = "Monsoon"

  #Fetching SG and CW Credits
  sg_credits, cw_credits, df = fetch_SGCW_credits(df)

  #First two year courses
  df1 = df[df['Semester'] < 5]

  #Last two year Courses
  df2 = df[df['Semester'] >= 5].reset_index()
  df2.drop('index', axis=1, inplace=True)

  #First Two Year Courses
  credits_F2, courses_F2, backlogs_F2 = handle_first_two_year_courses(df1)
  # print("Credits F2:", credits_F2)

  #Last Two Year Courses and Credits
  info_L2 = handle_last_two_year_courses(df2, courses_F2, backlogs_F2)
  backlogs = info_L2['backlogs']
  # print("Credits L2:", info_L2["credits"])

  grad_req_df = pd.DataFrame(columns = ["Credits", 'Required Credits', 'Completed Credits', "Remaining Credits", 'Status'])
  total_credits = credits_F2 + info_L2['credits'] + sg_credits + cw_credits

  #Normal Graduation Requirements Info
  grad_req_df = pd.concat([grad_req_df, pd.DataFrame({"Credits": "Total", 'Required Credits': 156, 'Completed Credits': total_credits, "Remaining Credits": 156-total_credits, 'Status': total_credits >= 156}, index=[0])], ignore_index=True)

  #Honors Graduation Requirement Info
  grad_req_df = pd.concat([grad_req_df, pd.DataFrame({"Credits": "Honors Total", 'Required Credits': 168, 'Completed Credits': total_credits, "Remaining Credits": 168-total_credits, 'Status': total_credits >= 168}, index=[0])], ignore_index=True)

  #CSE Graduation Requirement Info
  cse_credits = info_L2['cse_credits']
  grad_req_df = pd.concat([grad_req_df, pd.DataFrame({"Credits": "CSE", 'Required Credits': 16, 'Completed Credits': cse_credits, "Remaining Credits": 16-cse_credits, 'Status': cse_credits >= 16}, index=[0])], ignore_index=True)

  #SSH Graduation Requirement Info
  ssh_credits = info_L2['ssh_credits']
  grad_req_df = pd.concat([grad_req_df, pd.DataFrame({"Credits": "SSH", 'Required Credits': 28, 'Completed Credits': ssh_credits, "Remaining Credits": 28-ssh_credits, 'Status': ssh_credits >= 28}, index=[0])], ignore_index=True)

  #ECO Graduation Requirement Info
  eco_credits = info_L2['eco_credits']
  grad_req_df = pd.concat([grad_req_df, pd.DataFrame({"Credits": "ECO", 'Required Credits': 24, 'Completed Credits': eco_credits, "Remaining Credits": 24-eco_credits, 'Status': eco_credits >= 24}, index=[0])], ignore_index=True)

  print("Graduation Requirement Tracker\n-----------------------------------------")
  print(grad_req_df)
  print()

  course_recom_response['graduation_req_tracker'] = grad_req_df.to_dict()

  btp_status = "Incomplete"
  sg_status = "Incomplete"
  cw_status = "Incomplete"

  if(info_L2['btp']):
    btp_status = "Completed"
  if sg_credits >= 2:
    sg_status = "Completed"
  if cw_credits >= 2:
    cw_status = "Completed"

  print("BTP Credits:", btp_status)
  print("Self Growth Credits:", sg_status)
  print("Community Work Credits:", cw_status)

  course_recom_response['btp_status'] = btp_status
  course_recom_response['sg_status'] = sg_status
  course_recom_response['cw_status'] = cw_status

  dep_suggestions = []

  rem_graduation_conditions = []
  print("\nRemaining Graduation Conditions:\n---------------------------------------")
  if len(backlogs) != 0:
    condition = "- Complete backlogs/Improvements: " + str(backlogs)
    print(condition)
    rem_graduation_conditions.append(condition)

  if sg_status == "Incomplete":
    condition = "- Complete " +  str(2-sg_credits) + " SG credits"
    print(condition)
    rem_graduation_conditions.append(condition)

  if cw_status == "Incomplete":
    condition = "- Complete " + str(2-cw_credits) + " CW credits"
    print(condition)
    rem_graduation_conditions.append(condition)

  if cse_credits < 16:
    condition = "- Complete "+ str(16-cse_credits) + " CSE credits"
    print(condition)
    rem_graduation_conditions.append(condition)
    dep_suggestions.append("CSE")

  if eco_credits < 24 and ssh_credits < 28:
    condition = "- Complete " +  str(24-eco_credits) +  " ECO credits OR " + str(28-ssh_credits) + " SSH credits"
    print(condition)
    rem_graduation_conditions.append(condition)
    dep_suggestions.append("ECO")
    dep_suggestions.append("SSH")

  if total_credits < 156:
    condition = "- For graduation, complete " + str(156-total_credits) + " total credits"
    print(condition)
    rem_graduation_conditions.append(condition)
  else:
    condition = "- Graduation Requirements Completed"
    print(condition)
    rem_graduation_conditions.append(condition)

  if total_credits < 168:
    if btp_status == "Completed":
      condition = "- For honors graduation, complete " +  str(168-total_credits) + " total credits"
      print(condition)
      rem_graduation_conditions.append(condition)
    else:
      condition = "- For honors graduation, complete " + str(168-total_credits) + " total credits, and remaining BTP Credits"
      print(condition)
      rem_graduation_conditions.append(condition)
  else:
    condition = "- Honors Graduation Requirements Completed"
    print(condition)
    rem_graduation_conditions.append(condition)

  course_recom_response['graduation_conditions'] = rem_graduation_conditions

  print("\nAssociated Semester for Suggestions:", req_sem, "\n")
  course_recom_response['req_sem'] = req_sem

  #Retrieving course suggestions from database based on student's profile
  courses = courses_F2
  courses.extend(info_L2['courses'])
  print("\n Requirement Course Suggestions\n---------------------\n")
  course_recom_response['req_course_suggestions'] = fetch_database_courses(courses, req_sem, dep_suggestions)

  print("Additional Course Suggestions for Graduation Requirements Based on Interests:\n-------------------------------------------\n")
  course_recom_response['add_course_suggestions'] = fetch_database_courses(courses, req_sem, interest_deps)

  return course_recom_response


#Function to fetch courses from techtree database
def fetch_database_courses(courses, req_sem, dep_suggestions):
  db = pd.read_csv('course_recommender/techtree_database.csv')
  db = db.loc[(db['Semester'] == req_sem) | (db['Semester'] == 'Monsoon/Winter')]

  courses_response = {}
  
  #Fetching courses for each required department
  for dep in dep_suggestions:
    print(dep, "Suggestions:\n------------------")
    dep_df = db.loc[db['Department'] == dep]
    courses_df = pd.DataFrame(columns = ['Code', 'Name', 'Acronym', 'Semester'])

    for index, row in dep_df.iterrows():
      course_codes = preprocess_db_entry(row['Course Code'])
      if type(row['Prerequisites']) != str:
        prereqs = []
      else:
        prereqs = preprocess_db_entry(row['Prerequisites'])
      
      if type(row['Antirequisites']) != str:
        antireqs = []
      else:
        antireqs = preprocess_db_entry(row['Antirequisites'])

      #Check course already done or not
      it = set.intersection(set(courses),set(course_codes))
      if len(it) > 0:
        continue

      #Check if prequisites done or not
      it = set.intersection(set(courses),set(prereqs))
      if len(it) != len(prereqs) and len(it) < 2:
        continue
      
      #Check if prequisites done or not
      it = set.intersection(set(courses),set(antireqs))
      if len(it) > 0:
        continue

      # print("-",row['Course Code'], row['Course Name'], row['Course Acronym'], row['Semester'])
      courses_df = pd.concat([courses_df, pd.DataFrame({"Code": row['Course Code'], "Name": row['Course Name'], "Acronym": row['Course Acronym'], "Semester": row['Semester']}, index=[0])],
        ignore_index = True)

    print(courses_df)
    print()
    courses_response[dep] = courses_df.to_dict()

  return courses_response


#Function to preprocess techtree database data
def preprocess_db_entry(entry):
  # print(entry, type(entry))
  entry = entry.replace(" ", "")
  entry = entry.replace("or", ",")
  entry = entry.replace("and", ",")
  entry = entry.replace("&", ",")
  entry = entry.replace('/', ",")
  entry = entry.split(',')
  return entry

#Function to add missing data in fetched transcript data
def append_missing_data(df):
  missing_df = pd.DataFrame({
                    "Semester": [6, 6],
                    "Code": ["ECO201", "SSH235"],
                    "Title of the Course": ["Macroeconomics", "Ethics in AI"],
                    "Credit": [4, 4],
                    "Grade": ["A-", "A-"],
                    "Level": [2, 2]       
                })
  
  df = pd.concat([df, missing_df], ignore_index = True)
  return df


#Main Function
def main(filename, interest_deps):

  df = extract_transcript.pdf_to_df("course_recommender/"+filename)

  #Optional if certain data is missed in transcript fetching
  df = append_missing_data(df)

  print("Fetched Transcript Data:")
  print(df)
  print()

  # df.to_csv(filename)

  # df = pd.read_csv("tushar_data.csv")
  # print("Fetched Transcript Data:")
  # print(df)
  # print()

  response = course_recommender(df, interest_deps)
  return response

if __name__ == '__main__':
    main()