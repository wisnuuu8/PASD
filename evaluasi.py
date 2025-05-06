import joblib
from sklearn.metrics import classification_report, accuracy_score
from getData import load_data
from preprocessing import preprocess_data
from sklearn.model_selection import train_test_split

# Load dan preprocessing
df = load_data("detak_jantung_dataset.csv")
X, y, _, le_target = preprocess_data(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load model
model = joblib.load('detak_jantung_model.pkl')
y_pred = model.predict(X_test)

# Evaluasi
print("Akurasi:", accuracy_score(y_test, y_pred))
print("Laporan Klasifikasi:\n", classification_report(y_test, y_pred, target_names=le_target.classes_))
