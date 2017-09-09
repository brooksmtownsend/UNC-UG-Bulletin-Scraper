import re

# REGEX Sample
# ENEC 511. Stable Isotopes in the Environment. 3 Credits.
# Introduction to the theory, methods, and applications of stable isotopes
# to environmental problems. Primary focus will be on the origin, natural
# abundance, and fractionation of carbon, hydrogen, oxygen, and nitrogen
# isotopes.
# Requisites: Prerequisite, CHEM 102.
# Grading status: Letter grade
# Same as: GEOL 511.

ugradBulletin = open("./ugradBull")

departmentOdd = "[A-Z]{3}"
department = "[A-Z]{4}"
courseNum = "[0-9]{3}."

departmentAndNumPattern = re.compile(department + "\s" + courseNum + "\s")
gradingStatusPattern = re.compile("Grading status:")

foundCourse = False
stringArray = []

for line in ugradBulletin:
    if foundCourse:
        match = gradingStatusPattern.match(line)
        if match:
            stringArray.append(match.string)
            stringArray = []
            foundCourse = False
        else:
            stringArray.append(line)
    else:
        match = departmentAndNumPattern.match(line)
        if match:
            stringArray.append(match.string)
            foundCourse = True