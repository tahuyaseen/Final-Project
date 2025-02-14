# -*- coding: utf-8 -*-
"""Maternal health risk predictions

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/152jbSPi8tQGWSizqthPo3PP3I2Jo79hG

Importing Libraries
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GridSearchCV

"""Loading dataset"""

# Load the dataset
data = pd.read_csv('/content/Maternal Health Risk Data Set.csv')

"""Datasets"""

data.shape

data.dtypes

# Display the first few rows of the dataset
print(data.head())

# Display basic information about the dataset
print(data.info())

# Check for missing values
print(data.isnull().sum())

# Describe the dataset for statistical overview
print(data.describe())

"""Data Preprocessing"""

# Check for missing values
print("Missing values:\n", data.isnull().sum())

# Handle missing values
data = data.dropna()

# Handle outliers (e.g., using IQR)
numerical_cols = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
Q1 = data[numerical_cols].quantile(0.25)
Q3 = data[numerical_cols].quantile(0.75)
IQR=Q3-Q1

# Only apply the filtering to numerical columns
outlier_condition = ~((data[numerical_cols] < (Q1 - 1.5 * IQR)) | (data[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)
data = data[outlier_condition]

# Check the number of records after outlier removal
print(f"Number of records after outlier removal: {data.shape[0]}")

# Normalize the numerical features
scaler = StandardScaler()
data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

# Display the first few rows of the preprocessed dataset
print(data.head())

"""Exploring data analysis"""

# Plot histograms for each feature
data.hist(figsize=(12, 10))
plt.show()

# Calculate correlation matrix for numerical columns only
correlation_matrix = data[numerical_cols].corr()

# Plot correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# Plot risk level distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='RiskLevel', data=data)
plt.show()

"""Feature Engineering"""

# Create interaction terms (example)
data['Age_SystolicBP'] = data['Age'] * data['SystolicBP']
data['Age_DiastolicBP']= data['Age']*data['DiastolicBP']

# Polynomial features
data['Age_squared'] = data['Age'] ** 2

# Binning continuous variables
data['Age_binned'] = pd.cut(data['Age'], bins=5,labels=False)

# Display the first few rows of the dataset with new features
print(data.head())

"""Model Building"""

# Split the data
X = data.drop('RiskLevel', axis=1)
y = data['RiskLevel']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
y_pred_logreg = logreg.predict(X_test)
print("Logistic Regression:\n", classification_report(y_test, y_pred_logreg))
print("Accuracy:", accuracy_score(y_test,y_pred_logreg))

# Support Vector Classifier
svc = SVC()
svc.fit(X_train, y_train)
y_pred_svc = svc.predict(X_test)
print("Support Vector Classifier:\n", classification_report(y_test, y_pred_svc))
print("Accuracy:", accuracy_score(y_test, y_pred_svc))

"""Model evaluation and selection"""

# Compare models based on accuracy or other metrics
from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.1, 1, 10, 100], 'solver': ['liblinear']}
grid_search = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_logreg = grid_search.best_estimator_

# Evaluate the fine-tuned model
y_pred_best_logreg = best_logreg.predict(X_test)
print("Fine-tuned Logistic Regression:\n", classification_report(y_test, y_pred_best_logreg))
print("Accuracy:", accuracy_score(y_test, y_pred_best_logreg))

""""Project Overview:

Developing a machine learning model to predict maternal health complication risk levels by analyzing a dataset of pregnant women's health metrics. The goal is to classify each case into low, medium, or high-risk categories with an accuracy rate above 60%. This innovative solution aims to support healthcare providers in early identification and management of potential risks, ultimately improving maternal health outcomes."
"""