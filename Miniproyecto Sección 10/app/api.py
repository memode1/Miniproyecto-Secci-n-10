from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import __main__  # para registrar la clase con este módulo

class ManejoAtipicos(BaseEstimator, TransformerMixin):
    def __init__(self, metodo="iqr", estrategia="winsorizar"):
        self.metodo = metodo
        self.estrategia = estrategia
        self.limites_ = {}

    def fit(self, X, y=None):
        X = pd.DataFrame(X).copy()
        for col in X.columns:
            if self.metodo == "iqr":
                Q1 = X[col].quantile(0.25)
                Q3 = X[col].quantile(0.75)
                IQR = Q3 - Q1
                lim_inf = Q1 - 1.5 * IQR
                lim_sup = Q3 + 1.5 * IQR
            elif self.metodo == "percentil":
                lim_inf = X[col].quantile(0.01)
                lim_sup = X[col].quantile(0.99)
            else:
                raise ValueError("Método no soportado")

            self.limites_[col] = (lim_inf, lim_sup)
        return self

    def transform(self, X):
        X = pd.DataFrame(X).copy()
        for col in X.columns:
            lim_inf, lim_sup = self.limites_[col]
            if self.estrategia == "eliminar":
                X = X[(X[col] >= lim_inf) & (X[col] <= lim_sup)]
            elif self.estrategia == "winsorizar":
                X[col] = np.where(X[col] < lim_inf, lim_inf, X[col])
                X[col] = np.where(X[col] > lim_sup, lim_sup, X[col])
            else:
                raise ValueError("Estrategia no soportada")
        X.reset_index(drop=True, inplace=True)
        return X

FEATURE_COLUMNS = [
    "Age",
    "Sex",
    "ChestPainType",
    "RestingBP",
    "Cholesterol",
    "FastingBS",
    "RestingECG",
    "MaxHR",
    "ExerciseAngina",
    "Oldpeak",
    "ST_Slope",
]

def interpretar_paciente(features, proba):
    """
    features: lista [Age, Sex, ChestPainType, RestingBP, Cholesterol,
                     FastingBS, RestingECG, MaxHR, ExerciseAngina,
                     Oldpeak, ST_Slope]
    proba: probabilidad de enfermedad (0–1)
    """
    (age, sex, chestpain, bp, chol,
     fbs, ecg, maxhr, exang, oldpeak, st_slope) = features

    riesgo = []

    # Reglas simples basadas en clínica y dataset
    if age >= 55:
        riesgo.append("Edad mayor o igual a 55 años.")
    if sex == 1:
        riesgo.append("Sexo masculino (mayor riesgo coronario).")
    if chestpain == 3:
        riesgo.append("Dolor de pecho asintomático (tipo ASY).")
    if bp >= 140:
        riesgo.append("Presión arterial en reposo elevada (≥140 mmHg).")
    if chol >= 200:
        riesgo.append("Colesterol total elevado (≥200 mg/dL).")
    if fbs == 1:
        riesgo.append("Glucosa en ayunas alta (>120 mg/dL).")
    if ecg == 2:
        riesgo.append("ECG en reposo con probable hipertrofia ventricular (LVH).")
    if exang == 1:
        riesgo.append("Angina inducida por el ejercicio.")
    if oldpeak >= 2:
        riesgo.append("Depresión del ST significativa (Oldpeak ≥ 2).")
    if st_slope == 3:
        riesgo.append("Pendiente del ST descendente (downsloping).")

    # Mensaje global según probabilidad
    if proba < 0.25:
        nivel = "bajo"
        resumen = (
            f"El modelo estima una probabilidad BAJA (~{proba*100:.1f}%) "
            "de enfermedad cardíaca para este paciente."
        )
    elif proba < 0.6:
        nivel = "moderado"
        resumen = (
            f"El modelo estima una probabilidad MODERADA (~{proba*100:.1f}%) "
            "de enfermedad cardíaca. Existen factores de riesgo que conviene vigilar."
        )
    else:
        nivel = "alto"
        resumen = (
            f"El modelo estima una probabilidad ALTA (~{proba*100:.1f}%) "
            "de enfermedad cardíaca. Se recomienda valoración clínica detallada."
        )

    return nivel, resumen, riesgo


# REGISTRAR la clase con el mismo nombre que tenía al guardarse
setattr(__main__, "ManejoAtipicos", ManejoAtipicos)

# ahora sí, cargar el modelo
model = joblib.load("app/model.joblib")

app = FastAPI()

class Input(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: Input):
    # Convertir la lista en un DataFrame con nombres de columnas
    X_df = pd.DataFrame([data.features], columns=FEATURE_COLUMNS)

    # Pasar DataFrame al pipeline
    proba = model.predict_proba(X_df)[0][1]
    pred = int(proba >= 0.5)
    nivel_riesgo, resumen, factores = interpretar_paciente(data.features, proba)

    return {
        "heart_disease_probability": proba,
        "prediction": pred,
        "risk_level": nivel_riesgo,
        "summary": resumen,
        "risk_factors": factores,
        "note": "Este resultado es generado por un modelo estadístico y NO reemplaza una valoración médica profesional."
    }