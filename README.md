# CVDL
## Introduction
[Colabs Link](https://colab.research.google.com/drive/1MvkdSmtun9f3umaaF8InsxYD-Clny3zM) 

Students' Performance could be a good factor in predicting the economical level of different institutions.
The goal of this work is to track students' performance considering a set of external factors that could have both an effect of enhancing or of downgrading it.
The elements of the database [Student Performance Data Set](https://archive.ics.uci.edu/ml/datasets/student%2Bperformance#) could be modeled in such a way to obtain predictions upon the final grade of the student. Furthermore, it could predict how certain external factors would influence a student's performance or what would be a perfect combination of those factors that could yield an ideal performance.

## Reference Papers

The authors propose a new way of predicting students’ success based on the new concept of online education systems. Web-based systems hold consistent data about their users, giving the opportunity to apply data mining methods. The paper presents a classification of students in order to predict their success rate, using features extracted from logged data in a web-based system that is educationally inclined. It presents steps of designing, implementing, and evaluating classifiers on an online course dataset. A key aspect is that combining multiple classifiers leads to a significant improvement in classification performance. The use of a genetic algorithm (GA) resulted in having specific weights for the proposed features that improved prediction accuracy with about 10 to 12%  compared to a non-GA classifier. The aim is to identify at- risk students early, especially in large classes, so that they can be advised efficiently.

<sup>PREDICTING STUDENT PERFORMANCE: AN APPLICATION OF DATA MINING METHODS WITH THE EDUCATIONAL WEB-BASED SYSTEM LON-CAPA Behrouz Minaei-Bidgoli 1 , Deborah A. Kashy 2 , Gerd Kortemeyer 3 , William F. Punch 4</sup>


The present work approaches the study of students' achievements in secondary education using BI/DM techniques on real-world data (e.g. student grades, demographic, social and school related features). The data was modeled under binary/five-level classification and regression tasks, together with four DM models (i.e. Decision Trees, Random Forest, Neural Networks and Support Vector Machines) and three input selections (e.g. with and without previous grades). The results indicate the importance of some features (e. G. past evaluations, number of absences, parent’s job and education, alcohol consumption) in improving the overall prediction. As a direct outcome of this research, more efficient student prediction tools can be developed, improving the quality of education and enhancing school resource management.

<sup>USING DATA MINING TO PREDICT SECONDARY SCHOOL STUDENT PERFORMANCE Paulo Cortez and Alice Silva Dep. Information Systems/Algoritmi R&D Centre University of Minho</sup>

## Implementation

### Modeling Data
Tne first step is to remove some redundant features: 'school', 'internet', 'nursery'.
'school' feature, meaning the name of the school where sample students studied, is not concludent with our purpose.
'internet', or whether they have internet at home is not questionable nowadays.
'nursery' stays for sample students that followed a nursery programme. Like having internet at home, almost every student was prompted to go to a nursery school.

After dropping features that will most probably not bring high value to the model's prediction, a next step is to transform the data into data that can be interpreted by the model.
In this regards, the method `encode_binary` is mapping the binary data from {'T', 'F'} to {1, 0}. The nominal values in the dataset are replaced by dummy integer values provided by the `pandas.get_dummies` in the method `encode_nominal`.

### Classifying data
For classification, `sklearn.svm.SVC` linear classifier is trained on a batch from the dataset, X_train. The batch of samples was extracted with `sklearn.model_selection.train_test_split` method, with `test_size=0.1`.
The classifier was chosen because of it's high precission in predicting data with a lot of features.

### Prediction
The classifier was fed with the test data extracted with the same model_selection method used for the training data.

### Model Evaluation
The model was evaluated with `sklearn.metrics` methods, `classification_report` and `confusion_matrix` that prompted the best result:

|              	| precision 	| recall 	| f1_score 	| support 	|
|--------------	|-----------	|--------	|----------	|---------	|
| accuracy     	|           	|        	| 0.44     	| 105     	|
| macro avg    	| 0.43      	| 0.39   	| 0.39     	| 105     	|
| weighted avg 	| 0.47      	| 0.44   	| 0.43     	| 105     	|

the `poly` and `rbf` SVM classifiers were producing a slightly more poor score.  

### More work
Looking at the result, I have a hinch that the model is overfitting, so I will try to use Kfold fo separating data, get the mean error and plot the results of multiple models and try to overcome overfitting, if it figures out that my hinch is actually what is happening.


