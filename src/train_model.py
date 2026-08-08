import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load processed data
df = pd.read_csv("data/processed_student_data.csv")

# Features (X) and Target (y)
X = df.drop(columns=['result', 'total_score', 'average_score'])
y = df['result']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save column names (needed later for web app)
with open("models/columns.pkl", "wb") as f:
    pickle.dump(list(X.columns), f)

print("\n✅ Model saved to models/model.pkl")