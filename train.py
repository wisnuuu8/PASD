from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from getData import load_data
from preprocessing import preprocess_data

# Load dan preprocessing
df = load_data("detak_jantung_dataset.csv")
X, y, le_gender, le_target = preprocess_data(df)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save model dan encoder
joblib.dump(model, 'detak_jantung_model.pkl')
joblib.dump(le_gender, 'encoder_gender.pkl')
joblib.dump(le_target, 'encoder_target.pkl')
