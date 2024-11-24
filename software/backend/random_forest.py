import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


# Read the CSV file
file_path = "Codejam14Data.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

# Feature and label preparation
X = data.iloc[:, :-1].values  # All columns except the last are features
y = data.iloc[:, -1].values   # The last column is the label

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))

#saving the model 


from joblib import dump

# Save the trained model to a file
dump(classifier, 'TremorSeverityPrediction.joblib')



from joblib import load

def ML_predict(array):
    # Load the model from the file
    classifier = load('TremorSeverityPrediction.joblib')
    prediction = classifier.predict(array)

    return prediction

    # Use the loaded model for predictions
    #new_y_pred = classifierImported.predict(X_test)
    #cm = confusion_matrix(y_test, new_y_pred)
    #print(cm)
    #print(accuracy_score(y_test, new_y_pred))



