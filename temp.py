from asyncio.log import logger
import csv
import requests
from bs4 import BeautifulSoup
import logging

Course_Page_Url = "http://guide.berkeley.edu/courses/"
University = "University of California Berkeley"
Abbreviation = "UCB"
University_Homepage = "https://www.berkeley.edu/"

# Below fields didn't find in the website
Prerequisite = None
References = None
Scores = None
Projects = None
Professor_Homepage = None
output_file = None
course_count = 0


def save_course_data(university, abbreviation, department_name, course_title, unit_count, professor,
                        objective, prerequisite, required_skills, outcome, references, scores, description, projects,
                        university_homepage, course_homepage, professor_homepage):
    try:
        output_file.writerow([university, abbreviation, department_name, course_title, unit_count, professor,
                                    objective, prerequisite, required_skills, outcome, references, scores,
                                    description, projects, university_homepage, course_homepage, professor_homepage])

        course_count += 1
    except Exception as e:
        logger.error(
            f"{abbreviation} - {department_name} - {course_title}: An error occurred while saving course data: {e}"
        )


def get_course_data(course):
    Course_Title = course.find(class_="title").text

    Unit_Count = course.find(class_="hours").text
    Unit_Count = Unit_Count[:-5].rstrip()

    Description = course.find(class_='courseblockdesc').text

    course_sections = course.find_all(class_='course-section')

    Objective = None
    Outcome = None
    Professor = None
    Required_Skills = None

    for section in course_sections:
        inner_sections = section.find_all('p')
        for inner_section in inner_sections:
            inner_section_title = inner_section.find('strong')

            if inner_section_title.text == "Course Objectives:":
                inner_section_title.decompose()
                Objective = inner_section.text.strip()

            if inner_section_title.text == "Student Learning Outcomes:":
                inner_section_title.decompose()
                Outcome = inner_section.text.strip()

            if inner_section_title.text == "Instructor:":
                inner_section_title.decompose()
                Professor = inner_section.text.strip()

            if inner_section_title.text == "Prerequisites:":
                inner_section_title.decompose()
                Required_Skills = inner_section.text.strip()

    return Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description

def get_courses_of_department(department):
    a_element = department.find('a')
    Department_Name = a_element.text
    # print(a_element.text)
    department_url = "http://guide.berkeley.edu" + a_element.get('href')
    Course_Homepage = department_url

    department_page_content = requests.get(department_url).text
    department_soup = BeautifulSoup(department_page_content, 'html.parser')

    courses = department_soup.find_all(class_='courseblock')
    print("******************************************")
    print(courses)
    
    return courses, Department_Name, Course_Homepage


output_file = csv.writer(open(f'output_file.csv', 'w', encoding='utf-8', newline=''))
output_file.writerow(
    ['University', 'Abbreviation', 'Department', 'Course title', 'Unit', 'Professor', 'Objective',
        'Prerequisite', 'Required Skills', 'Outcome', 'References', 'Scores', 'Description', 'Projects',
        'University Homepage', 'Course Homepage', 'Professor Homepage']
)
html_content = requests.get(Course_Page_Url).text
soup = BeautifulSoup(html_content, 'html.parser')

departments = soup.find(id='atozindex').find_all('li')
# print(departments[0])
for department in departments:
    courses, Department_Name, Course_Homepage = get_courses_of_department(department)
    for course in courses:
        Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description = get_course_data(
            course)

        save_course_data(
            University, Abbreviation, Department_Name, Course_Title, Unit_Count,
            Professor, Objective, Prerequisite, Required_Skills, Outcome, References, Scores,
            Description, Projects, University_Homepage, Course_Homepage, Professor_Homepage
        )

    logger.info(f"{Abbreviation}: {Department_Name} department's data was crawled successfully.")

logger.info(f"{Abbreviation}: Total {course_count} courses were crawled successfully.")
