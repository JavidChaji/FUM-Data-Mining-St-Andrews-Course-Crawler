from ast import Not
from asyncio.log import logger
import csv
import re
from ssl import Options
import outcome
import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

Course_Page_Url = "https://www.st-andrews.ac.uk/subjects/reqs/2021-22/list.html?v=ug"
University = "University of St Andrews"
Abbreviation = "UOSA"
University_Homepage = "https://www.st-andrews.ac.uk/"


Prerequisite = None
References = None
Scores = None
Projects = None
output_file = None
Professor_Homepage = None
course_count = 0


def save_course_data(university, abbreviation, department_name, course_title, unit_count, professor,
                        objective, prerequisite, required_skills, outcome, references, scores, description, projects,
                        university_homepage, course_homepage, professor_homepage):
    try:
        output_file.writerow([university, abbreviation, department_name, course_title, unit_count, professor,
                                    objective, prerequisite, required_skills, outcome, references, scores,
                                    description, projects, university_homepage, course_homepage, professor_homepage])
        global course_count
        course_count += 1
    except Exception as e:
        logger.error(
            f"{abbreviation} - {department_name} - {course_title}: An error occurred while saving course data: {e}"
        )


def get_course_data(course):

    course_url = course.get('href') 
    course_page_content = requests.get(course_url).text
    course_soup = BeautifulSoup(course_page_content, 'html.parser')
    print("######################################################")
    print(course)


    Course_Title = course_soup.find(class_="page-heading").text
    print("######################################################")
    print(Course_Title)

    Unit_Count = int(course_soup.find(id="key-information").findNext('div').find("p").text)/2

    print("######################################################")
    print(Unit_Count)

    Description = course_soup.find(id='description').findNext('p').text
    print("######################################################")
    print(Description)

    Objective = None
    Outcome = None
    Professor = None
    Prerequisite = None
    Required_Skills = None
    Scores = None
    Professor_Homepage = None

    if course_soup.find(id='outcomes') is not None : 
        Outcome = course_soup.find(id='outcomes').findNext('ul').find_all("li")

    print("######################################################")
    print(Outcome)


    if (course_soup.find(id="relationship") is not None) and (course_soup.find(id="relationship").findNext('div').find("h3").text.strip() == "Pre-requisites"):
        Prerequisite = course_soup.find(id="relationship").findNext('div').find("p").text.strip()
    
    print("######################################################")
    print(Prerequisite)


    if (course_soup.find(id="relationship") is not None) and (course_soup.find(id="relationship").findNext('div').find("h3").text.strip() == "Anti-requisites"):
        Required_Skills = course_soup.find(id="relationship").findNext('div').find("p").text.strip()
    
    print("######################################################")
    print(Required_Skills)


    if course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module coordinator')) is not None:
        if course_soup.find(id="key-information").findNext('div').find("a") is not None:
            Professor = course_soup.find(id="key-information").findNext('div').find("a").text.strip()
            Professor_Homepage = course_soup.find(id="key-information").findNext('div').find("a").get('href')
        else:
            Professor = course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module coordinator')).findNext('p').text.strip()
    else:
        if course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module Staff')) is not None:
            Professor = course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module Staff')).findNext('p').text.strip()
        
    print("######################################################")
    print(Professor)

    print("######################################################")
    print(Professor_Homepage)


    Scores = course_soup.find(id="assessment").findNext('div').find("p").text.strip()
    print("######################################################")
    print(Scores)

    return Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description

def get_courses_of_department(department):
    #Get Department Name
    a_element = department.find("a")
    Department_Name = a_element.text.strip()

    print("##########################################################")
    print(Department_Name)
    # print(a_element)

    print("1*******************************************")

    #Get Course Homepage
    department_url = "https://www.st-andrews.ac.uk/subjects/reqs/2021-22/" + a_element.get('href')
    Course_Homepage = department_url

    #Get Courses of department
    courses = []

    department_page_content = requests.get(department_url).text
    department_soup = BeautifulSoup(department_page_content, 'html.parser')

    courses = department_soup.find_all('a', {"title":"Opens in a new tab/window"})
    for cours in courses:
        if len(cours.text) > 8:
            courses.remove(cours)

    
    return courses, Department_Name, Course_Homepage


output_file = csv.writer(open(f'data/output_file.csv', 'w', encoding='utf-8', newline=''))
output_file.writerow(
    ['University', 'Abbreviation', 'Department', 'Course title', 'Unit', 'Professor', 'Objective',
        'Prerequisite', 'Required Skills', 'Outcome', 'References', 'Scores', 'Description', 'Projects',
        'University Homepage', 'Course Homepage', 'Professor Homepage']
)

html_content = requests.get(Course_Page_Url).text
soup = BeautifulSoup(html_content, 'html.parser')

departments = soup.find_all('tr')

for department in departments:
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(department)
    courses, Department_Name, Course_Homepage = get_courses_of_department(department)
    
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(courses)
    # for course in courses:
    #     print(course)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(len(courses))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    for course in courses:
        Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description = get_course_data(course)

        save_course_data(
            University, Abbreviation, Department_Name, Course_Title, Unit_Count,
            Professor, Objective, Prerequisite, Required_Skills, Outcome, References, Scores,
            Description, Projects, University_Homepage, Course_Homepage, Professor_Homepage
        )

    logger.info(f"{Abbreviation}: {Department_Name} department's data was crawled successfully.")

logger.info(f"{Abbreviation}: Total {course_count} courses were crawled successfully.")
