# 🧠 Kidney Disease Prediction Dashboard

An end-to-end interactive dashboard to predict Chronic Kidney Disease (CKD) using machine learning, built with Python and Streamlit. This project combines data preprocessing, statistical analysis, predictive modeling, and dynamic visualizations to support healthcare insights.

---

## 📌 Project Overview

This project focuses on predicting kidney disease from a clinical dataset consisting of demographic, laboratory, and medical data. It includes:

- Data Cleaning and Imputation
- Exploratory Data Analysis and Hypothesis Testing (ANOVA, t-tests)
- Model Building (Logistic Regression, Random Forest, XGBoost)
- Balanced Classification using Undersampling
- An Interactive Streamlit App for Predictions & Visual Analytics

---

## 🎯 Features

- 🩺 **CKD Prediction Interface**  
  Input 25+ clinical parameters to predict whether a patient is likely to have CKD.

- 📊 **Hypothesis Testing Tab**  
  View significant statistical relationships (e.g., hemoglobin vs. CKD) using ANOVA results.

- 📈 **Interactive Visual Charts**  
  Visualize CKD distributions by age group, pus cell type, and hemoglobin levels using Plotly.

- 📂 **Model Comparison**  
  Logistic Regression, Random Forest, and XGBoost models with GridSearchCV tuning and evaluation.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `Python` | Core programming language |
| `Pandas`, `NumPy` | Data manipulation and numerical analysis |
| `Scikit-learn` | Machine learning models & evaluation |
| `XGBoost` | Gradient boosting classifier |
| `Matplotlib`, `Seaborn`, `Plotly` | Visualizations |
| `Streamlit` | Dashboard & frontend UI |
| `Imbalanced-learn` | Undersampling for class imbalance |

---

## 🧪 Models Used

- **Logistic Regression**
- **Random Forest Classifier**
- **XGBoost Classifier**

Evaluation metrics include:
- Accuracy
- Classification Report
- Precision, Recall, F1-score

---

## 🧬 Dataset Description

The dataset contains 400 records with 25 clinical features including:
- Demographics: `age`, `bp`, `sg`, etc.
- Lab Tests: `hemo`, `bu`, `sc`, `bgr`, etc.
- Categorical Attributes: `rbc`, `pc`, `pcc`, `htn`, `dm`, etc.

The target variable is `classification` (ckd / notckd).

---

## 🚀 How to Run the App Locally

1. Clone the repository:

```bash
git clone https://github.com/yourusername/kidney-disease-prediction.git
cd kidney-disease-prediction
