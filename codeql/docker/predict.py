import matplotlib.pyplot as plt
import pandas as pd
import joblib
import numpy as np

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

#replace string values of types to numerical
code_ql_frame['type'].replace('method',0, inplace=True) 
code_ql_frame['type'].replace('comment',1,inplace=True) 
code_ql_frame['type'].replace('class',2,inplace=True) 
code_ql_frame['type'].replace('import',3,inplace=True) 
code_ql_frame['type'].replace('commit message',4,inplace=True)

# prepare input data
input_data = code_ql_frame['input'] + ' ' + code_ql_frame['sourcefile']
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

# Calculate the percentages and confidence values
input_len = len(results_df)
non_sensitive_len = len(results_df[results_df['Predicted Label'] == 'not sensitive'])
non_sensitive_code_percentage = non_sensitive_len * 100 / input_len
sensitive_code_percentage = 100 - non_sensitive_code_percentage
average_confidence_non_sensitive = results_df['Confidence'][results_df['Predicted Label'] == 'not sensitive'].mean()
average_confidence_sensitive = results_df['Confidence'][results_df['Predicted Label'] != 'not sensitive'].mean()

# Create a pie chart with the percentages
labels = ['Sensitive Code', 'Non-sensitive Code']
sizes = [sensitive_code_percentage, non_sensitive_code_percentage]
colors = ['#ff7f0e', '#1f77b4']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures the circle shape

# Add labels for the confidence levels under each label
confidence_labels = [
    f'Confidence: {average_confidence_sensitive:.2f}%',
    f'Confidence: {average_confidence_non_sensitive:.2f}%'
]
plt.text(-0.5, 0.18, confidence_labels[0], horizontalalignment='center', verticalalignment='center', fontsize=9)
plt.text(0.5, -0.39, confidence_labels[1], horizontalalignment='center', verticalalignment='center', fontsize=9)

# Set the title and display the plot
plt.title('Sensitive vs. Non-sensitive Code')

# Save the bar chart as a PNG file
plt.savefig('predicted_results.png')
