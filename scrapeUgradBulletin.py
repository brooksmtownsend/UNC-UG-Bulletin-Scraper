import re
import json
import sys

file = open(sys.argv[1])

departmentOdd = "[A-Z]{3}"
department = "[A-Z]{4}"
courseNum = "[0-9]{2,3}"
endOfCourse = "[L H .][\s .]"

departmentAndNumPattern = re.compile(department + "\s" + courseNum + endOfCourse)
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
    modifier = ""
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
        departmentAndNum = self.arrayOfAttributes[0][:9]
        self.department = departmentAndNum[:4]
        if (departmentAndNum[-1:] == "." or departmentAndNum[-2:] == ". "):
            if (departmentAndNum[-2:] == "H."
                or departmentAndNum[-2:] == "L."):
                self.modifier = departmentAndNum[-2:][:-1]
                self.courseNum = int(departmentAndNum[-4:][:-2])
            else:
                if (departmentAndNum[-4:][-2:] == ". "):
                    self.courseNum = int(departmentAndNum[-4:][:2])
                else:
                    self.courseNum = int(departmentAndNum[-4:][:3])
        else:
            if (departmentAndNum[-1:] == "H"
                or departmentAndNum[-1:] == "L"):
                self.modifier = departmentAndNum[-1:]
                self.courseNum = int(departmentAndNum[-4:][:-1])

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


for line in file:
    if foundCourse:
        match = gradingStatusPattern.search(line)
        if match:
            stringArray.append(match.string)
            coursesArray.append(Course(stringArray))
            stringArray = []
            foundCourse = False
        else:
            stringArray.append(line)
            if len(stringArray) > 15:
                foundCourse = False
                stringArray = []
    else:
        match = departmentAndNumPattern.match(line)
        if match:
            stringArray.append(match.string)
            foundCourse = True


# Outputting to *.json
text_file = open(sys.argv[2], "w")
jsonCourse = []

for course in coursesArray:
     dict = {'department': course.department,
      'number': course.courseNum,
      'modifier': course.modifier,
      'gen eds': course.genEds,
      'requirements': course.requirements,
      'description': course.description[10:]
      }
     jsonCourse.append(dict)

json.dump(jsonCourse, text_file)

text_file.close()
