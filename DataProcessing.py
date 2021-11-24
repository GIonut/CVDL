import csv
import numpy as np

s = []
with open('data/student/student-mat.csv', newline='') as csvfile:
    students = csv.reader(csvfile, delimiter=';', quotechar='"')
    students.__next__()
    s = np.asarray([s for s in students])

with open('data/student/student-por.csv', newline='') as csvfile:
    students = csv.reader(csvfile, delimiter=';', quotechar='"')
    students.__next__()
    s = np.concatenate((s, np.asarray([s for s in students])))

print(s)

