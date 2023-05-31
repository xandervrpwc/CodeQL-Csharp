import matplotlib.pyplot as plt
import pandas as pd
import joblib
import numpy as mp

# Load the saved model and vectorizer
model = joblib.load("/app/lr_model.pkl")
vectorizer = joblib.load("/app/vectorizer.pkl")

# Prepare labels & types to map model results
labels = {
    0: "not sensitive",
    1: "barely sensitive",
    2: "moderately sensitive",
    3: "highly sensitive",
    4: "extremely sensitive"
}
types = {
    0: "method",
    1: "comment",
    2: "class",
    3: "import",
    4:"commit message"
}

# Read JSON data from file
json_data = pd.read_json('/data.json')

# Extract "results" column as DataFrame
code_ql_frame = pd.DataFrame(json_data['results'].tolist(), columns=['input', 'sourcefile','type'])

# prepare input data
input_data = code_ql_frame['input'] + code_ql_frame['sourcefile']
# Preprocess the input data
X_test = np.concatenate((vectorizer.transform(input_data).toarray(), code_ql_frame['type'].values.reshape(-1, 1)), axis=1) 

# Predict on the test data
y_pred_test = model.predict(X_test)
confidence_scores = model.predict_proba(X_test).max(axis=1)

# Create a dataframe to store the results
results_df = pd.DataFrame({'Code': input_data,
                           'Type':code_ql_frame['type'],
                           'Source':code_ql_frame['sourcefile'],
                           'Predicted Label': [labels[prediction] for prediction in y_pred_test],
                           'Confidence': [confidence * 100 for confidence in confidence_scores]})

#Replace numerical values in the "Type" column with corresponding strings
results_df['Type'] = results_df['Type'].map(types)

#Saving results .csv
results_df.to_csv('/app/prediction_results.csv')

#Bar chart showing the frequency of predicted labels
# Count the frequency of predicted labels
label_counts = results_df['Predicted Label'].value_counts()


# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(label_counts.index, label_counts.values)
plt.xlabel('Predicted Labels')
plt.ylabel('Frequency')
plt.title('Frequency of Predicted Labels')

# Save the bar chart as a PNG file
plt.savefig('/app/predicted_results.png')
