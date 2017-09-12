import re
import json

ugradBulletin = open("./ugradBull")

departmentOdd = "[A-Z]{3}"
department = "[A-Z]{4}"
courseNum = "[0-9]{3}."

departmentAndNumPattern = re.compile(department + "\s" + courseNum + "\s")
departmentOddAndNumPattern = re.compile(departmentOdd + "\s" + courseNum + "\s")
gradingStatusPattern = re.compile("Grading status:")
genEdPattern = re.compile("Gen Ed:")
requisitesPattern = re.compile("Requisites:")

foundCourse = False
stringArray = []
coursesArray = []

class Course(object):
    arrayOfAttributes = []
    department = ""
    courseNum = 0
    description = ""
    requirements = ""
    genEds = ""
    gradingStatus = ""

    # str should be a string array of the attributes of a course
    def __init__(self, properties):
        self.arrayOfAttributes = properties
        self.extractInformation()
        # self.printAttributes()

    def extractInformation(self):
        departmentAndNum = self.arrayOfAttributes[0][:8]
        self.department = departmentAndNum[:4]
        self.courseNum = int(departmentAndNum[-3:])

        for attr in self.arrayOfAttributes:
            if gradingStatusPattern.match(attr):
                self.gradingStatus = attr[16:]
            else:
                if requisitesPattern.match(attr):
                    self.requirements = attr[12:]
                else:
                    if genEdPattern.match(attr):
                        self.genEds = attr[8::1]
                    else:
                        self.description += attr

    def printAttributes(self): # For debug purposes only
        for attr in self.arrayOfAttributes:
             print(attr)


for line in ugradBulletin:
    if foundCourse:
        match = gradingStatusPattern.match(line)
        if match:
            stringArray.append(match.string)
            coursesArray.append(Course(stringArray))
            stringArray = []
            foundCourse = False
        else:
            stringArray.append(line)
    else:
        match = departmentAndNumPattern.match(line)
        if match:
            stringArray.append(match.string)
            foundCourse = True


# Outputting to departments.json
text_file = open("departments.json", "w")
jsonCourse = []

for course in coursesArray:
     dict = {'department': course.department,
      'number': course.courseNum,
      'gen eds': course.genEds,
      'requirements': course.requirements,
      'description': course.description[10:]
      }
     jsonCourse.append(dict)

json.dump(jsonCourse, text_file)

text_file.close()
