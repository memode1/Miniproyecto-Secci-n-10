# 📘 Proyecto: API de Predicción de Enfermedad Cardíaca  
## Machine Learning + FastAPI + Docker + Kubernetes

Este proyecto implementa un modelo de Machine Learning (**RandomForest**) capaz de predecir la probabilidad de **enfermedad cardíaca** basado en atributos clínicos de un paciente.

Incluye:
- ✔️ Entrenamiento y validación del modelo  
- ✔️ API REST con FastAPI  
- ✔️ Contenedor Docker  
- ✔️ Despliegue en Kubernetes  
- ✔️ Notebooks con EDA y modelado  
- ✔️ Pipeline reproducible  

---

## 📁 Estructura del Proyecto

Miniproyecto 3/
│
├── app/
│ ├── api.py # API FastAPI
│ ├── model.joblib # Modelo RandomForest final
│
├── docker/
│ ├── Dockerfile # Imagen Docker
│ ├── requirements.txt # Dependencias
│
├── k8s/
│ ├── deployment.yaml # Deployment en Kubernetes
│ └── service.yaml # Service NodePort
│
└── notebooks/
├── EDA.ipynb # Exploración de datos
└── 2_model_pipeline_cv.ipynb # Entrenamiento del modelo

---

# 1. Entrenamiento del Modelo

Entrenado en:  
`notebooks/2_model_pipeline_cv.ipynb`

Incluye:
- EDA  
- Limpieza  
- Imputación  
- Manejo de outliers  
- Escalado  
- Entrenamiento de: Logistic, KNN, Naive Bayes, RandomForest, XGBoost  
- GridSearchCV  
- Métricas comparativas  
- Selección final: **RandomForest**

Modelo guardado en:

app/model.joblib


---

# 2. API con FastAPI

Archivo principal:  
`app/api.py`

Carga el modelo y expone el endpoint:

## **POST /predict**

### 📥 Ejemplo de entrada:


{
  "features": [63, 1, 3, 145, 233, 1, 2, 150, 0, 2.3, 3]
}


### Ejemplo de salida:


{
  "heart_disease_probability": 0.585,
  "prediction": 1,
  "risk_level": "moderado",
  "summary": "El modelo estima una probabilidad MODERADA (~58.5%) de enfermedad cardíaca. Existen factores de riesgo que conviene vigilar.",
  "risk_factors": [
    "Edad mayor o igual a 55 años.",
    "Sexo masculino (mayor riesgo coronario).",
    "Dolor de pecho asintomático (tipo ASY).",
    "Presión arterial en reposo elevada (≥140 mmHg).",
    "Colesterol total elevado (≥200 mg/dL).",
    "Glucosa en ayunas alta (>120 mg/dL).",
    "ECG en reposo con probable hipertrofia ventricular (LVH).",
    "Depresión del ST significativa (Oldpeak ≥ 2).",
    "Pendiente del ST descendente (downsloping)."
  ],
  "note": "Este resultado es generado por un modelo estadístico y NO reemplaza una valoración médica profesional."
}

Swagger UI
http://localhost:8000/docs

# 3. Despliegue con Docker
Dockerfile ubicado en:
docker/Dockerfile

## Construir imagen
docker build -t heart-api -f docker/Dockerfile .


## Ejecutar contenedor
docker run -p 8000:8000 heart-api


## Acceder a la API
http://localhost:8000/docs

# 4. Despliegue en Kubernetes

Manifiestos en carpeta:
k8s/

Requisitos:

Docker Desktop con Kubernetes habilitado

kubectl configurado

## Aplicar Deployment y Service

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml


## Ver estado

kubectl get pods
kubectl get svc


## Acceder a la API en Kubernetes
NodePort: 30000
http://localhost:30000/docs

# 5. Dependencias

Archivo:

docker/requirements.txt


## Incluye:

- fastapi
- uvicorn
- scikit-learn
- joblib
- numpy
- pydantic

# 6. Resumen del Dockerfile

FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r docker/requirements.txt
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]


# Autores

Jeronimo Dominguez – Mariana Franco – Juan Andres Ramos
