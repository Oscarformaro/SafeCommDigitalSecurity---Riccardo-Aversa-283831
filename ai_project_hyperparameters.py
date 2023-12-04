# -*- coding: utf-8 -*-
"""AI_project_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P-KKIyAkc2ZMIYfJaUa4OveVYSw3-TxO
"""

#first, we do EDA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
path="./sms.csv"
sms_df = pd.read_csv(path)

#now we check for the missing values
missing_values=sms_df.isnull().sum()
print("Missing values:")
print(missing_values)

column_to_analyze = 'Fraudolent'

sns.histplot(sms_df, x = column_to_analyze, hue='Fraudolent', multiple = 'stack')

#we check if there is a correlation between the lenght of a message and if it is fraudolent or not
# Create a new feature for the length of each message
sms_df['message_length'] = sms_df['SMS test'].apply(len)

# Create a new feature for the number of words in each message
sms_df['word_count'] = sms_df['SMS test'].apply(lambda x: len(str(x).split()))

sns.histplot(sms_df, x='message_length', hue='Fraudolent', multiple='stack')
plt.show()

sns.histplot(sms_df, x='word_count', hue='Fraudolent', multiple='stack')
plt.show()

sms_df['Date and Time'] = pd.to_datetime(sms_df['Date and Time'])
# Create a new feature for the hour of the day
sms_df['hour'] = sms_df['Date and Time'].dt.hour

# Create a new feature for the day of the week
sms_df['day_of_week'] = sms_df['Date and Time'].dt.dayofweek

sns.histplot(sms_df, x='hour', hue='Fraudolent', multiple='stack')
plt.show()

sns.histplot(sms_df, x='day_of_week', hue='Fraudolent', multiple='stack')
plt.show()

print(sms_df.columns)

from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer

# Tokenize the text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sms_df['SMS test'])

# Now, apply OneHotEncoder
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X.toarray())

# X_encoded will now be a numpy array. You can convert it back to DataFrame if you want:
X_encoded_df = pd.DataFrame(X_encoded.toarray())

print(X_encoded_df)

#now we have to use OneHotEncoder to encode the categorical features
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
categorical_features=["SMS test"]
encoder=OneHotEncoder()
transformer = ColumnTransformer([('encocder',
                                   encoder,
                                   categorical_features)],
                                   remainder="drop")
transformed_sms_df = transformer.fit_transform(sms_df)
# transformed_sms_df will now be a numpy array. You can convert it back to DataFrame if you want:
transformed_sms_df = pd.DataFrame(transformed_sms_df)

# Preprocessing the text data
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sms_df['SMS test'])

# Converting the target column to numpy array
y = sms_df['Fraudolent'].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Computing Accuracy, Precision, Recall and F1 Score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print("Accuracy =", accuracy_score(y_test,y_pred))
print("Precision =", precision_score(y_test,y_pred))
print("Recall =", recall_score(y_test,y_pred))
print("F1 Score =", f1_score(y_test,y_pred))

print("Confusion Matrix:")
print(cm)

from sklearn.preprocessing import StandardScaler


# Vectorizing the email texts
tfidf_vectorizer = TfidfVectorizer(max_features=500)  # Limiting to 500 features for simplicity
X_text = tfidf_vectorizer.fit_transform(sms_df['SMS test']).toarray()

# Combining text features with Email Length
X_length = sms_df[['message_length']].values
X = np.hstack((X_text, X_length))

# Target variable
y = sms_df['Fraudolent']

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Feature Scaling - Important for Logistic Regression
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Creating the Logistic Regression model
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Computing Accuracy, Precision, Recall, and F1 Score
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Outputting the results
print("Confusion Matrix:\n", cm)
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)

from sklearn.ensemble import RandomForestClassifier
classifier=RandomForestClassifier(n_estimators=100, random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

cm=confusion_matrix(y_test, y_pred)

print("Accuracy =", accuracy_score(y_test,y_pred))
print("Precision =", precision_score(y_test,y_pred))
print("Recall =", recall_score(y_test,y_pred))
print(cm)

# Function to plot the results
def plot_results(X, y, y_pred, title):
    plt.figure(figsize=(10, 6))
    plt.scatter(X[y == 0], y[y == 0], color='green', label='Not Fraudolent', alpha=0.5)
    plt.scatter(X[y == 1], y[y == 1], color='red', label='Fraudolent', alpha=0.5)
    plt.scatter(X[y_pred != y], y_pred[y_pred != y], color='blue', label='Misclassified', alpha=0.5)
    plt.title(title)
    plt.xlabel('Email Length')
    plt.ylabel('Class')
    plt.legend()
    plt.show()

# Predicting for the training set
y_train_pred = classifier.predict(X_train)
# Plotting for the training set
plot_results(X_train[:, -1], y_train, y_train_pred, 'Random Forest - Training Set')

# Plotting for the test set
plot_results(X_test[:, -1], y_test, y_pred, 'Random Forest - Test Set')

from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

cm=confusion_matrix(y_test, y_pred)
print("Accuracy =", accuracy_score(y_test,y_pred))
print("Precision =", precision_score(y_test,y_pred))
print("Recall =", recall_score(y_test,y_pred))
print("F1 Score =", f1_score(y_test,y_pred))
print(cm)

from sklearn.model_selection import GridSearchCV

# Define the parameter grid
param_grid = {
    'penalty': ['l1', 'l2', 'elasticnet', 'none'],
    'C': np.logspace(-4, 4, 20),
    'solver': ['lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga'],
    'max_iter': [100, 1000,2500, 5000]
}

# Create a base model
logistic = LogisticRegression(random_state=0)

# Instantiate the grid search model
grid_search = GridSearchCV(estimator=logistic, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best parameters: ", best_params)

# Train the model using the best parameters
best_model = LogisticRegression(**best_params)
best_model.fit(X_train, y_train)

# Make predictions using the best model
y_pred_best = best_model.predict(X_test)

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Define the parameter grid
param_grid = {
    'n_estimators': [100, 200, 300, 400, 500],
    'max_features': ['auto', 'sqrt'],
    'max_depth': [10, 20, 30, 40, 50, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

# Create a base model
rf = RandomForestClassifier(random_state=0)

# Instantiate the grid search model
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best parameters: ", best_params)

# Train the model using the best parameters
best_model = RandomForestClassifier(**best_params)
best_model.fit(X_train, y_train)

# Make predictions using the best model
y_pred_best = best_model.predict(X_test)

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# Define the parameter grid
param_grid = {
    'C': [0.1, 1, 10, 100, 1000],
    'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
    'kernel': ['rbf']
}

# Create a base model
svc = SVC(random_state=0)

# Instantiate the grid search model
grid_search = GridSearchCV(estimator=svc, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best parameters: ", best_params)

# Train the model using the best parameters
best_model = SVC(**best_params)
best_model.fit(X_train, y_train)

# Make predictions using the best model
y_pred_best = best_model.predict(X_test)

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Define the model
classifier = RandomForestClassifier(random_state=0)

# Define the parameters to tune
param_grid = {
    'n_estimators': [50, 100, 200],  # Number of trees in the forest
    'max_depth': [None, 10, 20, 30],  # Maximum depth of the tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
    'bootstrap': [True, False]  # Method for sampling data points
}

# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=classifier, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# Fit GridSearchCV to the training data
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best parameters: ", best_params)

# Get the best score
best_score = grid_search.best_score_
print("Best score: ", best_score)

# Predicting the Test set results with the best estimator
y_pred = grid_search.best_estimator_.predict(X_test)

# Compute Accuracy, Precision, Recall and F1 Score
print("Accuracy =", accuracy_score(y_test,y_pred))
print("Precision =", precision_score(y_test,y_pred))
print("Recall =", recall_score(y_test,y_pred))
print("F1 Score =", f1_score(y_test,y_pred))

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

# Define the model
classifier = LogisticRegression(random_state=0)

# Define the parameters to tune
param_grid = {
    'penalty': ['l1', 'l2', 'elasticnet', 'none'],  # Specify the norm used in the penalization
    'C': np.logspace(-4, 4, 20),  # Inverse of regularization strength
    'solver': ['lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga'],  # Algorithm to use in the optimization problem
    'max_iter': [100, 1000, 2500, 5000]  # Maximum number of iterations taken for the solvers to converge
}

# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=classifier, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# Fit GridSearchCV to the training data
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best parameters: ", best_params)

# Get the best score
best_score = grid_search.best_score_
print("Best score: ", best_score)

# Predicting the Test set results with the best estimator
y_pred = grid_search.best_estimator_.predict(X_test)

# Compute Accuracy, Precision, Recall and F1 Score
print("Accuracy =", accuracy_score(y_test,y_pred))
print("Precision =", precision_score(y_test,y_pred))
print("Recall =", recall_score(y_test,y_pred))
print("F1 Score =", f1_score(y_test,y_pred))

#trying randomized search to get fewer candidates
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression

# Define the model
classifier = LogisticRegression(random_state=0)

# Define the parameters to tune
param_distributions = {
    'penalty': ['l1', 'l2', 'elasticnet', 'none'],
    'C': np.logspace(-4, 4, 20),
    'solver': ['lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga'],
    'max_iter': [100, 1000, 2500, 5000]
}

# Initialize RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=classifier, param_distributions=param_distributions, n_iter=100, cv=3, n_jobs=-1, verbose=2, random_state=0)

# Fit RandomizedSearchCV to the training data
random_search.fit(X_train, y_train)

# Get the best parameters
best_params = random_search.best_params_
print("Best parameters: ", best_params)

# Get the best score
best_score = random_search.best_score_
print("Best score: ", best_score)

# Predicting the Test set results with the best estimator
y_pred = random_search.best_estimator_.predict(X_test)

# Compute Accuracy, Precision, Recall and F1 Score
print("Accuracy =", accuracy_score(y_test,y_pred))
print("Precision =", precision_score(y_test,y_pred))
print("Recall =", recall_score(y_test,y_pred))
print("F1 Score =", f1_score(y_test,y_pred))

#Best parameters:  {'C': 10, 'gamma': 0.001, 'kernel': 'rbf'}