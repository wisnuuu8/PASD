from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import pandas as pd

app = Flask(__name__)
app.secret_key = "rahasia123"  # untuk session login

# Load model dan encoder
model      = joblib.load("detak_jantung_model.pkl")
le_gender  = joblib.load("encoder_gender.pkl")
le_target  = joblib.load("encoder_target.pkl")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            return redirect(url_for("form"))
        else:
            error = "Username atau password salah."
    return render_template("login.html", error=error)

# Logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

# Form Input
@app.route("/", methods=["GET", "POST"])
def form():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    error = None
    if request.method == "POST":
        nama = request.form["nama"].strip()
        try:
            usia   = int(request.form["usia"])
            gender = request.form["gender"]
            rest   = int(request.form["rest"])
            maxb   = int(request.form["maxb"])
            sys    = int(request.form["sys"])
            dia    = int(request.form["dia"])

            if rest >= maxb:
                raise ValueError("Detak jantung istirahat harus lebih kecil dari detak jantung maksimum.")

            # Encode dan prediksi
            ge = le_gender.transform([gender])[0]
            df = pd.DataFrame([[usia, ge, rest, maxb, sys, dia]],
                              columns=["Usia", "Jenis Kelamin", "Detak Jantung Istirahat (bpm)",
                                       "Detak Jantung Maksimum (bpm)", "Tekanan Darah Sistolik (mmHg)",
                                       "Tekanan Darah Diastolik (mmHg)"])

            pred = model.predict(df)[0]
            cat  = le_target.inverse_transform([pred])[0]

            zones = {
                "Resting": "<50% max HR (Zone 1)",
                "Warm Up": "50-60% (Zone 2)",
                "Fat Burn": "60-70% (Zone 3)",
                "Cardio": "70-80% (Zone 4)",
                "Extreme": ">80% (Zone 5)"
            }
            zona = zones.get(cat, "N/A")

            return redirect(url_for("result", nama=nama, kategori=cat, zona=zona))

        except Exception as e:
            error = str(e)

    return render_template("form.html", error=error)

# Hasil Prediksi
@app.route("/result")
def result():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    nama     = request.args.get("nama", "")
    kategori = request.args.get("kategori", "")
    zona     = request.args.get("zona", "")
    return render_template("result.html", nama=nama, kategori=kategori, zona=zona)

if __name__ == "__main__":
    app.run(debug=True)
