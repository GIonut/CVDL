from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
import pickle
from joblib import dump, load

# Initialize the Flask application
app = Flask(__name__)

app.config['SECRET_KEY'] = "caircocoders-ednalan"
# student = {"sex": 'F',
#                               'age': '15',
#                               'address': 'U',
#                               'Pstatus': 'T',
#                               'famsize': 'GT3',
#                               'Medu': '4',
#                               'Fedu': '4',
#                               'traveltime': '0',
#                               'studytime': '0',
#                               'failures': '0',
#                               'schoolsup': 'yes',
#                               'famsup': 'yes',
#                               'activities': 'yes',
#                               'higher': 'yes',
#                               'romantic': 'yes',
#                               'paid': 'yes',
#                               'famrel': '0',
#                               'freetime': '5',
#                               'goout': '5',
#                               'Dalc': '5',
#                               'Walc': '5',
#                               'health': '0',
#                               'absences': '50',
#                               'G1': '10',
#                               'G2': '10',
#                               'Mjob_health': 1,
#                               'Mjob_other': 0,
#                               'Mjob_services': 0,
#                               'Mjob_teacher': 0,
#                               'Fjob_health': 1,
#                               'Fjob_other': 0,
#                               'Fjob_services': 0,
#                               'Fjob_teacher': 0,
#                               'reason_home': 1,
#                               'reason_other': 0,
#                               'reason_reputation': 0,
#                               'guardian_mother': 1,
#                               'guardian_other': 0}
#
# with open('/home/ionut/workspace/UNI/CVDL/Project/flaskr/student.txt', 'wb') as handle:
#       pickle.dump(student, handle)
class Feature():
    def __init__(self, feature_name, values):
        self.feature_name = feature_name
        self.values = values

"""
1 school - student's school (binary: "GP" - Gabriel Pereira or "MS" - Mousinho da Silveira)
2 sex - student's sex (binary: "F" - female or "M" - male)
3 age - student's age (numeric: from 15 to 22)
4 address - student's home address type (binary: "U" - urban or "R" - rural)
5 famsize - family size (binary: "LE3" - less or equal to 3 or "GT3" - greater than 3)
6 Pstatus - parent's cohabitation status (binary: "T" - living together or "A" - apart)
7 Medu - mother's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
8 Fedu - father's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)

//
9 Mjob - mother's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
10 Fjob - father's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
11 reason - reason to choose this school (nominal: close to "home", school "reputation", "course" preference or "other")
12 guardian - student's guardian (nominal: "mother", "father" or "other")
//

13 traveltime - home to school travel time (numeric: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour)
14 studytime - weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)
15 failures - number of past class failures (numeric: n if 1<=n<3, else 4)
16 schoolsup - extra educational support (binary: yes or no)
17 famsup - family educational support (binary: yes or no)
18 paid - extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)
19 activities - extra-curricular activities (binary: yes or no)
20 nursery - attended nursery school (binary: yes or no)
21 higher - wants to take higher education (binary: yes or no)
22 internet - Internet access at home (binary: yes or no)
23 romantic - with a romantic relationship (binary: yes or no)
24 famrel - quality of family relationships (numeric: from 1 - very bad to 5 - excellent)
25 freetime - free time after school (numeric: from 1 - very low to 5 - very high)
26 goout - going out with friends (numeric: from 1 - very low to 5 - very high)
27 Dalc - workday alcohol consumption (numeric: from 1 - very low to 5 - very high)
28 Walc - weekend alcohol consumption (numeric: from 1 - very low to 5 - very high)
29 health - current health status (numeric: from 1 - very bad to 5 - very good)
30 absences - number of school absences (numeric: from 0 to 93)

# these grades are related with the course subject, Math or Portuguese:
31 G1 - first period grade (numeric: from 0 to 20)
31 G2 - second period grade (numeric: from 0 to 20)
32 G3 - final grade (numeric: from 0 to 20, output target)
"""
# 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
#        'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid',
#        'activities', 'higher', 'romantic', 'famrel', 'freetime', 'goout',
#        'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'Mjob_health',
#        'Mjob_other', 'Mjob_services', 'Mjob_teacher', 'Fjob_health',
#        'Fjob_other', 'Fjob_services', 'Fjob_teacher', 'reason_home',
#        'reason_other', 'reason_reputation', 'guardian_mother',
#        'guardian_other'
def get_dropdown_values():
    features = [Feature("sex", ['F', 'M']),
     Feature('age', ['15', '16', '17', '18']),
     Feature('address', ['U', 'R']),
     Feature('famsize', ['LE3', 'GT3']),
     Feature('Pstatus', ['T', 'A']),
     Feature('Medu', ['0',  '1', '2', '3', '4']),
     Feature('Fedu', ['0',  '1', '2', '3', '4']),
     Feature('traveltime', ['0',  '1', '2', '3', '4']),
     Feature('studytime', ['0',  '1', '2', '3', '4']),
     Feature('failures', ['0',  '1', '2', '3', '4']),
     Feature('schoolsup', ['yes',  'no']),
     Feature('famsup', ['yes',  'no']),
     Feature('paid', ['yes',  'no']),
     Feature('activities', ['yes',  'no']),
     Feature('higher', ['yes',  'no']),
     Feature('romantic', ['yes',  'no']),
     Feature('famrel', ['0',  '1', '2', '3', '4', '5']),
     Feature('freetime', ['0',  '1', '2', '3', '4', '5']),
     Feature('goout', ['0',  '1', '2', '3', '4', '5']),
     Feature('Dalc', ['0',  '1', '2', '3', '4', '5']),
     Feature('Walc', ['0',  '1', '2', '3', '4', '5']),
     Feature('health', ['0',  '1', '2', '3', '4', '5']),
     Feature('absences', ['0',  '10', '20', '30', '40', '50', '60', '70', '80', '90']),
     Feature('G1', ['0',  '2', '4', '6', '8', '10', '12', '14', '16', '18', '20']),
     Feature('G2', ['0',  '2', '4', '6', '8', '10', '12', '14', '16', '18', '20']),
     Feature('Mjob_health', ["0", "1"]),
     Feature('Mjob_other', ["0", "1"]),
     Feature('Mjob_services', ["0", "1"]),
     Feature('Mjob_teacher', ["0", "1"]),
     Feature('Fjob_health', ["0", "1"]),
     Feature('Fjob_other', ["0", "1"]),
     Feature('Fjob_services', ["0", "1"]),
     Feature('Fjob_teacher', ["0", "1"]),
     Feature('reason_home', ["0", "1"]),
     Feature('reason_other', ["0", "1"]),
     Feature('reason_reputation', ["0", "1"]),
     Feature('guardian_mother', ["0", "1"]),
     Feature('guardian_other', ["0", "1"]),
     ]

    # Create an empty dictionary
    myDict = {}
    for p in features:
        key = p.feature_name
        q = p.values
        myDict[key] = q

    class_entry_relations = myDict
                        
    return class_entry_relations


@app.route('/_update_dropdown')
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)

    with open('/home/ionut/workspace/UNI/CVDL/Project/flaskr/student.txt', 'rb') as handle:
          student = pickle.loads(handle.read())

    student[selected_class] = selected_entry

    with open('/home/ionut/workspace/UNI/CVDL/Project/flaskr/student.txt', 'wb') as handle:
      pickle.dump(student, handle)

    loaded_model = load('/home/ionut/workspace/UNI/CVDL/Project/flaskr/model.joblib')
    for key in student.keys():
        student[key] = [student[key]]
    df = pd.DataFrame.from_dict(student)
    df = encode_binary(df)
    cols_when_model_builds = loaded_model.feature_names_in_
    df = df[cols_when_model_builds]

    y_pred = loaded_model.predict(df)
    return jsonify(student=student, prediction=int(y_pred[0]))

@app.route('/')
def index():
    """
    initialize drop down menus
    """
    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    with open('/home/ionut/workspace/UNI/CVDL/Project/flaskr/student.txt', 'rb') as handle:
          student = pickle.loads(handle.read())

    return render_template('index.html',
                       all_classes=default_classes,
                       all_entries=default_values,
                       student=student)

def encode_binary(X):
  X['sex'].replace({'F':1, 'M':0}, inplace=True)
  X['address'].replace({'U':1, 'R':0}, inplace=True)
  X['famsize'].replace({'GT3':1, 'LE3':0},inplace=True)
  X['Pstatus'].replace({'T':1, 'A':0}, inplace=True)
  X['schoolsup'].replace({'yes':1, 'no':0}, inplace=True)
  X['famsup'].replace({'yes':1, 'no':0}, inplace=True)
  X['paid'].replace({'yes':1, 'no':0}, inplace=True)
  X['activities'].replace({'yes':1, 'no':0}, inplace=True)
  X['higher'].replace({'yes':1, 'no':0}, inplace=True)
  X['romantic'].replace({'yes':1, 'no':0}, inplace=True)
  return X

# #encode nominal features
# def encode_nominal(X):
#   nominal_features = ['Mjob', 'Fjob', 'reason', 'guardian']
#   new_features = pd.get_dummies(X[nominal_features], drop_first=True)
#   X = X.drop(nominal_features, axis=1)
#   X = pd.concat([X, new_features], axis=1)
#   return X

if __name__ == '__main__':
    app.run(debug=True)