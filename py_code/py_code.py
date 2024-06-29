import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report

# read the csv file as DataFrame
df = pd.read_csv('./atlas-higgs-challenge-2014-v2.csv')

# drop the event0
event_0 = df[['DER_mass_transverse_met_lep', 'DER_mass_vis', 'DER_pt_ratio_lep_tau',
        'DER_pt_ratio_lep_tau', 'PRI_tau_pt', 'DER_sum_pt', 'PRI_tau_eta']].loc[0].values
eventToPredict = pd.DataFrame([event_0]) 

df.drop([0], inplace=True)

# select the features and the target
X = df[['DER_mass_transverse_met_lep', 'DER_mass_vis', 'DER_pt_ratio_lep_tau',
        'DER_pt_ratio_lep_tau', 'PRI_tau_pt', 'DER_sum_pt', 'PRI_tau_eta']].to_numpy()
y = df['Label'] # Series

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# declare the models
model1 = LinearDiscriminantAnalysis()
model2 = KNeighborsClassifier()

# train model1 and compute its roc curve
print("LinearDiscriminantAnalysis model")
model1.fit(X_train, y_train)
score1 = model1.score(X_test, y_test)
print(f'score = {score1}')
pred1 = model1.predict(X_test)
pred1_prob = model1.predict_proba(X_test)[:,1]
fpr1, tpr1, thresholds1 = roc_curve(y_test.map({'s':1, 'b':0}), pred1_prob)
roc_auc1 = auc(fpr1, tpr1)
print(classification_report(y_test, pred1))

# train model2 and compute its the roc curve
print("KNeighborsClassifier model")
model2.fit(X_train, y_train)
score2 = model2.score(X_test, y_test)
print(f'score = {score2}')
pred2 = model2.predict(X_test)
pred2_prob = model2.predict_proba(X_test)[:,1]
fpr2, tpr2, thresholds2 = roc_curve(y_test.map({'s':1, 'b':0}), pred2_prob)
roc_auc2 = auc(fpr2, tpr2)
print(classification_report(y_test, pred2))


# go in the proper directory we want to save te files
current_dir = os.getcwd()
subfolder = 'pythonImages'
subfolder_path = os.path.join(current_dir, subfolder)


# show the roc curves
plt.figure()
plt.plot(fpr1, tpr1, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc1:.2f})')
plt.plot(fpr2, tpr2, color='blue', lw=2, label=f'ROC curve (area = {roc_auc2:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve')
plt.legend(loc='lower right')
ROC_path = os.path.join(subfolder_path, 'ROC_curve.png')
plt.savefig(ROC_path)

# compute the confusion matrices
cm1 = confusion_matrix(y_test, pred1)
cm2 = confusion_matrix(y_test, pred2)

# show the confusion matrix for model1
plt.figure(figsize=(8, 6))
sns.heatmap(cm1, annot=True, fmt='d', cmap='Oranges', xticklabels=['Predicted b', 'Predicted s'], yticklabels=['True b', 'True s'])
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Confusion Matrix LDA')
cm1_path = os.path.join(subfolder_path, 'confusion_matrix_LDA.png')
plt.savefig(cm1_path)

# show the confusion matrix for model2
plt.figure(figsize=(8, 6))
sns.heatmap(cm2, annot=True, fmt='d', cmap='Blues', xticklabels=['Predicted b', 'Predicted s'], yticklabels=['True b', 'True s'])
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Confusion Matrix KNN')
cm2_path = os.path.join(subfolder_path, 'confusion_matrix_KNN.png')
plt.savefig(cm2_path)

# predict the class of event0 using the two different model trained before
predictedClass_1 = model1.predict(eventToPredict)
predictedClass_2 = model2.predict(eventToPredict)

print(f'The event to predict we know to be of type s and the LDA model predict it as type {predictedClass_1}')
print(f'The event to predict we know to be of type s and the KNN model predict it as type {predictedClass_2}')
