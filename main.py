from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# Kreiranje Flask aplikacije
app = Flask(__name__)

# Učitavanje modela i skalera
df = pd.read_excel('Nekretnine_Novi_Sad_Azurirano_v2.xlsx')

# One-Hot Encoding za kategorijske kolone
df_encoded = pd.get_dummies(
    df, columns=['Lokacija', 'Spratnost', 'Stanje', 'Blizina centra'], drop_first=True)

# Skaliranje podataka
scaler = StandardScaler()
X = df_encoded.drop('Cena (€)', axis=1)
y = df_encoded['Cena (€)']
scaler.fit(X)

# Kreiranje i treniranje Random Forest modela
model = RandomForestRegressor(n_estimators=300, max_depth=20,
                              min_samples_split=5, min_samples_leaf=2, random_state=42)
model.fit(X, y)

# Početna stranica


@app.route('/')
def home():
    return render_template('index.html')

# Ruta za predikciju


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Prikupljanje podataka iz forme
        kvadratura = float(request.form['kvadratura'])
        broj_soba = int(request.form['broj_soba'])
        godina_izgradnje = int(request.form['godina_izgradnje'])
        parking = int(request.form['parking'])
        lift = int(request.form['lift'])
        garaza = int(request.form['garaza'])
        terasa = int(request.form['terasa'])

        # Kreiranje niza za predikciju
        input_data = np.array([[kvadratura, broj_soba, godina_izgradnje,
                              parking, lift, garaza, terasa] + [0] * (X.shape[1] - 7)])
        input_scaled = scaler.transform(input_data)

        # Predikcija
        predvidjena_cena = model.predict(input_scaled)[0]

        # Prikaz rezultata
        return render_template('index.html', prediction=f'Predviđena cena: {predvidjena_cena:.2f} €')

    except Exception as e:
        return render_template('index.html', prediction=f'Greška: {e}')


# Pokretanje aplikacije
if __name__ == '__main__':
    app.run(debug=True)
