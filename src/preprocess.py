import pandas as pd

def load_and_preprocess_data(filepath="data/student_data.csv"):
    # Step 1: Load data
    df = pd.read_csv(filepath)
    print("Original Data Shape:", df.shape)
    print(df.head())

    # Step 2: Check for missing values
    print("\nMissing values:\n", df.isnull().sum())

    # Step 3: Create a 'total_score' and 'average_score' column
    df['total_score'] = df['math score'] + df['reading score'] + df['writing score']
    df['average_score'] = df['total_score'] / 3

    # Step 4: Create target column -> Pass/Fail (assume 40 as passing average)
    df['result'] = df['average_score'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')

    # Step 5: Encode categorical columns
    df_encoded = pd.get_dummies(df, columns=[
        'gender',
        'race/ethnicity',
        'parental level of education',
        'lunch',
        'test preparation course'
    ], drop_first=True)

    # Step 6: Encode target column (Pass=1, Fail=0)
    df_encoded['result'] = df_encoded['result'].map({'Pass': 1, 'Fail': 0})

    print("\nProcessed Data Shape:", df_encoded.shape)
    print(df_encoded.head())

    return df_encoded


if __name__ == "__main__":
    processed_df = load_and_preprocess_data()
    processed_df.to_csv("data/processed_student_data.csv", index=False)
    print("\n✅ Processed data saved to data/processed_student_data.csv")