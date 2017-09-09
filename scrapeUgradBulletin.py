import re

ugradBulletin = open("./ugradBull")

departmentOdd = "[A-Z]{3}"
department = "[A-Z]{4}"
courseNum = "[0-9]{3}."

departmentAndNumPattern = re.compile(department + "\s" + courseNum + "\s")
departmentOddAndNumPattern = re.compile(departmentOdd + "\s" + courseNum + "\s")
gradingStatusPattern = re.compile("Grading status:")

foundCourse = False
stringArray = []
coursesArray = []

class Course(object):
    arrayOfAttributes = []
    department = ""
    courseNum = 0
    title = ""
    credits = ""
    description = ""
    requirements = ""
    genEds = ""
    gradingStatus = ""

    # str should be a string array of the attributes of a course
    def __init__(self, properties):
        self.arrayOfAttributes = properties
        self.extractInformation()
        self.printAttributes()

    def extractInformation(self):
        departmentAndNum = self.arrayOfAttributes[0][:8]
        self.department = departmentAndNum[:4]
        self.courseNum = int(departmentAndNum[-3:])

        # TODO: After retrieving a piece of information, remove it from the array.
        # TODO: Break down components using REGEX expressions with keywords
        # TODO: Eventually, only the description should be left.

    def printAttributes(self): # For debug purposes only
        # print(self.department)
        # print(self.courseNum)
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
        # match2 = departmentOddAndNumPattern.match(line)
        # implement check here for 3 letter departments if needed
        if match:
            stringArray.append(match.string)
            foundCourse = True


# This was code to write all of the distinct departments to a file, could be re-used in the future for other pieces of info
# text_file = open("departments.txt", "w")
#
# for course in coursesArray:
#     text_file.write(course.department + "\n")
#
# text_file.close()
