# Mini Proyecto 3: Predicción de Enfermedad Cardiaca  
### Modelado, Evaluación y Despliegue en API, Docker y Kubernetes

##  Integrantes
- **Mariana Franco**
- **Jerónimo Domínguez**
- **Juan Andrés Ramos**

---

# Contextualización del Proyecto

Las enfermedades cardiovasculares representan una de las principales causas de mortalidad a nivel mundial.  
Este proyecto busca **analizar y modelar datos clínicos** para predecir la presencia de enfermedad cardiaca en pacientes mediante técnicas de Machine Learning.

Además de construir y comparar diferentes modelos, se selecciona el mejor y se despliega como una **API funcional** utilizando **FastAPI**, **Docker** y **Kubernetes**.

---

# Contexto del Dataset

El dataset utilizado proviene del repositorio **UCI Heart Disease** y contiene información médica básica recopilada en evaluaciones clínicas.

Esta información permite estudiar patrones asociados al riesgo cardiaco y entrenar modelos capaces de identificar pacientes con probabilidad de presentar la enfermedad.

---

# Descripción del Dataset

El dataset contiene **918 registros** y **12 columnas**, entre variables numéricas y categóricas.

### Resumen:
- **Número de muestras:** 918  
- **Número de variables:** 12  
- **Tipo de problema:** Clasificación binaria  
- **Variable objetivo:** `HeartDisease` (1 = presencia, 0 = ausencia)  

---

# Variables del Dataset

| Variable        | Tipo        | Descripción |
|-----------------|-------------|-------------|
| **Age**         | Numérica    | Edad del paciente |
| **Sex**         | Categórica  | 1 = Hombre, 0 = Mujer |
| **ChestPainType** | Categórica | Tipo de dolor torácico |
| **RestingBP**   | Numérica    | Presión arterial en reposo |
| **Cholesterol** | Numérica    | Nivel de colesterol |
| **FastingBS**   | Numérica    | Azúcar en sangre en ayunas |
| **RestingECG**  | Categórica  | Resultado del ECG |
| **MaxHR**       | Numérica    | Frecuencia cardíaca máxima |
| **ExerciseAngina** | Categórica | Angina inducida por ejercicio |
| **Oldpeak**     | Numérica    | Depresión del segmento ST |
| **ST_Slope**    | Categórica  | Pendiente del segmento ST |
| **HeartDisease** | Binaria    | Variable objetivo |

---

# Observaciones Importantes

- Existen **valores faltantes** en algunas variables numéricas.  
- Se encontraron **outliers** en variables como `Cholesterol` y `Oldpeak`.  
- Se realizaron pasos de:
  - Imputación de datos  
  - Tratamiento de atípicos  
  - Escalado y codificación  
  - Partición estratificada del dataset  

- Modelos entrenados:
  - Logistic Regression  
  - Naive Bayes  
  - KNN  
  - Random Forest  
  - XGBoost  

- El mejor modelo fue **Random Forest**, según desempeño en **AUC-ROC** y métricas de clasificación.

---

# Despliegue del Modelo

El modelo final se empaquetó y desplegó mediante:

### ✔ FastAPI  
API para recibir datos del paciente y retornar predicción.

### ✔ Docker  
Contenedor para estandarizar ejecución en cualquier entorno.

### ✔ Kubernetes  
Orquestación del contenedor para asegurar disponibilidad y escalabilidad.

---

