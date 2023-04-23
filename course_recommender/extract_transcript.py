import time
import pydocparser
import pandas as pd
import numpy as np


def pdf_to_df(path):
        label = "ERP_parser"
        id = "jwuxrqbvaxlj"

        rule_table = "rule_for_erp_parser"
        rule_name = "rule_for_name"
        rule_rollNo = "rule_for_roll_no"
        rule_branch = "rule_for_branch"
        parser = pydocparser.Parser()
        parser.login("21e83163025206134f045989ca9287b70c9e55b8")

        parsers = parser.list_parsers()
        # print(parsers)

        document_id = parser.upload_file_by_path(path, label)
        time.sleep(7)
        data = parser.get_multiple_results(label)
        data = [data[0]]

        df = pd.DataFrame(data[0][rule_table][1:])
        name = data[0]["rule_for_name"]
        rollNo = data[0]["rule_for_roll_no"]
        branch = data[0]["rule_for_branch"]

        print(name)
        print(rollNo)
        print(branch)

        #Drop the last row containing total credits
        df.drop(df.index[-1], inplace=True)

        df.rename(columns={"key_0":"Semester", "key_1":"Code", "key_2":"Title of the Course", "key_3":"Credit", "key_4":"Grade"}, 
                        inplace=True)
        total_sem = []
        for index, row in df.iterrows():
        # print(row['Semester'])
                if row['Semester'] not in total_sem and row['Semester'] != "":
                        total_sem.append(row['Semester'])
                        # print(index, total_sem)
                if row['Semester']=="":
                        df.iloc[index]['Semester'] = total_sem[-1]
        # dict_map = {}
        # for idx,sem in enumerate(total_sem):
        #         dict_map[sem] = idx + 1
        # df['Semester'] = df['Semester'].map(dict_map)
        pattern = r'[^a-zA-Z0-9\s]|(?<![IVXLCDM])\b[IVXLCDM]+\b'

        #Dropping rows with empty Code value
        df['Code'].replace('', np.nan, inplace=True)
        df.dropna(subset=['Code'], inplace=True)
        df.reset_index(inplace=True)
        df.drop(['index'], axis=1, inplace=True)

        df.dropna(inplace=True)
        df['Code'] = df['Code'].str.replace(pattern, '')
        df['Title of the Course'] = df['Title of the Course'].str.replace(pattern, '')
        df['Grade'] = df['Grade'].replace({"At":"A+", "Cc":"C", "Bb":"B", "Ss":"S", "Xx":"X", "Aa":"A", "Dd":"D", "$":"S", "be":"A-"})
        # df['Code'] = df['Code'].replace({"CQM301A": "COM301A", "ESC207A_": "ESC207A"})
        df['Level'] = df.apply(lambda x: int(x['Code'][3]), axis=1)
        df['Credit'] = df.apply(lambda x: int(x['Credit']), axis=1)

        #Preprocessing Parsing anomalies
        for i in df.index:
                df.at[i, 'Code'] = df.at[i, 'Code'].replace("-", "")
                df.at[i, 'Code'] = df.at[i, 'Code'].replace("_", "")
                df.at[i, 'Code'] = df.at[i, 'Code'].replace("Q", "O")

                df.at[i, 'Title of the Course'] = df.at[i, 'Title of the Course'].replace("-", "")
                df.at[i, 'Title of the Course'] = df.at[i, 'Title of the Course'].replace("_", "")
                df.at[i, 'Title of the Course'] = df.at[i, 'Title of the Course'].replace("=", "")
                df.at[i, 'Title of the Course'] = df.at[i, 'Title of the Course'].replace("|", "I")

                if "S" in df.at[i, 'Grade']:
                        df.at[i, 'Grade'] = "S"


        #Numbering Semesters
        base_year = int(df['Semester'][0].split(" ")[1])
        def sem_index(x, base_year):
                [sem, year] = x['Semester'].split(" ")
                if sem == "Monsoon":
                        return 2*(int(year)-base_year+1) - 1
                elif sem == "Winter":
                        return 2*(int(year)-base_year)
                else:
                        return 2*(int(year)-base_year) + 0.5

        df['Semester'] = df.apply(lambda x: sem_index(x, base_year), axis=1)

        student_info = {"name": name, "rollNo": rollNo, "branch": branch}

        return df, student_info
     