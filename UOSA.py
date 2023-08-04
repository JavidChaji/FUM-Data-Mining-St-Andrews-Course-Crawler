from cgitb import handler
import requests
from bs4 import BeautifulSoup
import logging
from asyncio.log import logger
import csv
import re
import requests
from bs4 import BeautifulSoup
import logging

from BaseCrawler import BaseCrawler



logger = logging.getLogger('__main__')


class UOSA(BaseCrawler):

    Course_Page_Url = "https://www.st-andrews.ac.uk/subjects/reqs/2021-22/list.html?v=ug"
    University = "University of St Andrews"
    Abbreviation = "UOSA"
    University_Homepage = "https://www.st-andrews.ac.uk/"

# Below fields didn't find in the website
    Objective = None
    References = None
    Projects = None
    Required_Skills = None

    def get_courses_of_department(self, department):
        #Get Department Name
        a_element = department.find("a")
        Department_Name = a_element.text.strip()

        print("######################")
        print(Department_Name)

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

    def get_course_data(self, course):

        Description = None
        Outcome = None
        Professor = None
        prerequisite = None
        scores = None
        professor_Homepage = None
        Course_Title = None
        Unit_Count = None

        course_url = course.get('href') 
        course_page_content = requests.get(course_url).text
        course_soup = BeautifulSoup(course_page_content, 'html.parser')


        if course_soup.find(class_="page-heading") is not None:
            Course_Title = course_soup.find(class_="page-heading").text
        # print("#####################")
        # print(Course_Title)


        if (course_soup.find(id='description') is not None) and (course_soup.find(id='description').findNext('p') is not None):
            Description = course_soup.find(id='description').findNext('p').text
        # print("######################################################")
        # print(Description)

        if course_soup.find(id='outcomes') is not None : 
            Outcome = course_soup.find(id='outcomes').findNext('ul').find_all("li")

        # print("######################################################")
        # print(Outcome)


        if (course_soup.find(id="relationship") is not None) and (course_soup.find(id="relationship").findNext('div').find("h3",text = re.compile('Pre-requisites')) is not None) and (course_soup.find(id="relationship").findNext('div').find("p") is not None):
            prerequisite = course_soup.find(id="relationship").findNext('div').find("p").text.strip()
        
        # print("######################################################")
        # print(prerequisite)


        # if (course_soup.find(id="relationship") is not None) and (course_soup.find(id="relationship").findNext('div').find("h3").text.strip() == "Anti-requisites"):
        #     Required_Skills = course_soup.find(id="relationship").findNext('div').find("p").text.strip()
        
        # print("######################################################")
        # print(Required_Skills)

        if course_soup.find(id="key-information") is not None:
            if course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module coordinator')) is not None:
                if course_soup.find(id="key-information").findNext('div').find("a") is not None:
                    Professor = course_soup.find(id="key-information").findNext('div').find("a").text.strip()
                    professor_Homepage = course_soup.find(id="key-information").findNext('div').find("a").get('href')
                else:
                    if course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module coordinator')).findNext('p') is not None:
                        Professor = course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module coordinator')).findNext('p').text.strip()
            else:
                if course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module Staff')) is not None:
                    if course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module Staff')).findNext('p') is not None:
                        Professor = course_soup.find(id="key-information").findNext('div').find("h3",text = re.compile('Module Staff')).findNext('p').text.strip()  
            
            if course_soup.find(id="key-information").findNext('div').find("p") is not None:
                Unit_Count = float(course_soup.find(id="key-information").findNext('div').find("p").text)/2
            # print("###################")
            # print(Unit_Count)
        # print("###################")
        # print(Professor)

        # print("###################")
        # print(Professor_Homepage)


        if (course_soup.find(id="assessment") is not None) and (course_soup.find(id="assessment").findNext('div').find("p") is not None):
            scores = course_soup.find(id="assessment").findNext('div').find("p").text.strip()
        # print("####################")
        # print(Scores)

        return Course_Title, Unit_Count, Outcome, Professor, Description, prerequisite, professor_Homepage, scores

    def handler(self):
        html_content = requests.get(self.Course_Page_Url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        departments = soup.find_all('tr')

        for department in departments:
            courses, Department_Name, Course_Homepage = self.get_courses_of_department(department)

            print("<<<<<>>>>>")
            print(len(courses))

            for course in courses:
                Course_Title, Unit_Count, Outcome, Professor, Description, prerequisite, professor_Homepage, scores = self.get_course_data(course)

                self.save_course_data(
                    self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                    Professor, self.Objective, prerequisite, self.Required_Skills, Outcome, self.References, scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, professor_Homepage
                )

            logger.info(f"{self.Abbreviation}: {Department_Name} department's data was crawled successfully.")

        logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")


if __name__ == '__main__':
    d = UOSA()
    d.handler()