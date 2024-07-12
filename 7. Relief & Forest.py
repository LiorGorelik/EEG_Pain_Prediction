import os
import pandas as pd
from skrebate import ReliefF
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

def relief_feature_ranking_and_classification(file_path, target_column, results_df):
    # Read your data from the Excel file
    data = pd.read_excel(file_path)

    # Fill missing values with mean of column
    data.fillna(data.mean(), inplace=True)

    # Separate features and target variable
    X = data.drop(columns=[target_column, 'Patient'])
    y = data[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Reset index of y_train
    y_train = y_train.reset_index(drop=True)

    # Initialize the ReliefF algorithm
    relief = ReliefF(n_features_to_select=100)

    # Fit the algorithm on the training data
    relief.fit(X_train.values, y_train.values)

    # Get the top features from the training data
    top_features = [feature for feature, _ in sorted(zip(X_train.columns, relief.feature_importances_), key=lambda x: -x[1])[:100]]

    # Use the top features for classification
    X_train_selected = X_train[top_features]
    X_test_selected = X_test[top_features]

    # Initialize the RandomForestClassifier
    clf = RandomForestClassifier()

    # Train the classifier on the training data
    clf.fit(X_train_selected, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test_selected)

    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy for {file_path}: {accuracy}")

    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix for {file_path}:\n{cm}")

    # Compute F1 score
    f1 = f1_score(y_test, y_pred)
    print(f"F1 Score for {file_path}: {f1}")

    # Compute sensitivity (recall)
    sensitivity = cm[1, 1] / (cm[1, 1] + cm[1, 0])
    print(f"Sensitivity for {file_path}: {sensitivity}")

    # Compute specificity
    specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    print(f"Specificity for {file_path}: {specificity}")

    # Extract the part of the path after "Final_b4_ML_"
    result_file_name = file_path.replace('Final_b4_ML_', '')

    # Append the results to the DataFrame
    results_df = results_df._append({
        'File': result_file_name,
        'Accuracy': accuracy,
        'F1 Score': f1,
        'Sensitivity': sensitivity,
        'Specificity': specificity,
        'Confusion Matrix': str(cm),
    }, ignore_index=True)

    return results_df

if __name__ == "__main__":
    # Define the folder path containing the Excel files
    folder_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output'

    # Define the target column
    target_column = 'Painful/Nonpainful'

    # Create an empty DataFrame to store the results
    results_df = pd.DataFrame(columns=['File', 'Accuracy', 'F1 Score', 'Sensitivity', 'Specificity', 'Confusion Matrix'])

    # Get a list of all Excel files that start with "Final_b4_ML_" in the specified folder
    files = [file for file in os.listdir(folder_path) if file.startswith('Final_b4_ML_') and file.endswith('.xlsx')]

    # Iterate through each file
    for file in files:
        # Construct the full file path
        file_path = os.path.join(folder_path, file)

        # Perform relief feature ranking, classification, and evaluation for each file
        results_df = relief_feature_ranking_and_classification(file_path, target_column, results_df)

    # Save the results to an Excel file
    results_path = os.path.join(folder_path, 'results_summary_same_100_2_all.xlsx')
    results_df.to_excel(results_path, index=False)
    print(f"Results saved to {results_path}")
