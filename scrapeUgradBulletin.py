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
    # title = ""
    # credits = ""
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

        # TODO: After retrieving a piece of information, remove it from the array.
        # TODO: Break down components using REGEX expressions with keywords
        # TODO: Eventually, only the description should be left.

    def printAttributes(self): # For debug purposes only
        print(str(self.department) + str(self.courseNum))
        print(self.genEds)
        print(self.requirements)
        print(self.gradingStatus)
        # for attr in self.arrayOfAttributes:
        #     print(attr)

        # print("This many attributes: "+ str(len(self.arrayOfAttributes)))


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
        # match2 = departmentOddAndNumPattern.match(line)
        # implement check here for 3 letter departments if needed
        if match:
            stringArray.append(match.string)
            foundCourse = True

# for course in coursesArray:
#     print(str(course.department) + str(course.courseNum))
#     print("Gen eds: "+ course.genEds)
#     print("Requirements: " + course.requirements)
#     print("Description: " + course.description[10:])


# This was code to write all of the distinct departments to a file, could be re-used in the future for other pieces of info
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

# print(jsonCourse)

json.dump(jsonCourse, text_file)

text_file.close()
