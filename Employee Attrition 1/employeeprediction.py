import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from scipy.stats import chi2_contingency
from sklearn.preprocessing import MinMaxScaler
from streamlit_option_menu import option_menu

# Load models and scaler
with open('/Users/narayansanthanam/Downloads/Employee Attrition project/EmployeePromotionLikelihood1.pkl', 'rb') as file:
    promotion_model = pickle.load(file)

with open('/Users/narayansanthanam/Downloads/Employee Attrition project/performance_rating_model.pkl','rb') as file:
    performance_model = pickle.load(file)

with open('/Users/narayansanthanam/Downloads/Employee Attrition project/Attrition_rate1.pkl', 'rb') as file:
    attrition_model = pickle.load(file)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load data for EDA
data = pd.read_csv('/Users/narayansanthanam/Downloads/Employee Attrition project/Employee-Attrition - Employee-Attrition.csv')

# Set page configuration
st.set_page_config(page_title="Employee Portal & EDA", layout="wide")

# Horizontal Navigation Bar
selected = option_menu(
    menu_title=None,
    options=[
        "Employee Promotion Likelihood",
        "Performance Rating Prediction",
        "Attrition Prediction",
        "EDA Dashboard"
    ],
    icons=["arrow-up-circle", "bar-chart-line", "person-x", "bar-chart"],
    orientation="horizontal"
)

# Page 1: Employee Promotion Likelihood
if selected == "Employee Promotion Likelihood":
    st.title("🚀 Employee Promotion Likelihood")
    JobLevel = st.number_input("Job Level", 1, 5)
    TotalWorkingYears = st.number_input("Total Working Years", 0, 40)
    YearsInCurrentRole = st.number_input("Years in Current Role", 0, 20)
    MonthlyIncome = st.number_input("MonthlyIncome", 0, 20000)
    YearsAtCompany = st.selectbox("Years At Company", [1, 2, 3, 4, 5, 6, 7, 8])
    YearsWithCurrManager = st.number_input("Years with Current Manager", 0, 10)

    if st.button("Predict Promotion Time"):
        input_data = [[JobLevel, TotalWorkingYears, YearsInCurrentRole, MonthlyIncome, YearsAtCompany, YearsWithCurrManager]]
        scaled_input = scaler.transform(input_data)
        prediction = promotion_model.predict(scaled_input)[0]
        st.success(f"Estimated Years Since Last Promotion: {prediction} years")

# Page 2: Performance Rating Prediction
elif selected == "Performance Rating Prediction":
    st.title("📈 Performance Rating Prediction")
    YearsAtCompany = st.number_input("Years at Company", 0, 40)
    Education = st.selectbox("Education Level", [1, 2, 3, 4, 5])
    YearsInCurrentRole = st.number_input("Years in Current Role", 0, 20)
    YearsWithCurrManager = st.number_input("Years with Current Manager", 0, 20)
    YearsSinceLastPromotion = st.number_input("Years Since Last Promotion", 0, 20)
    JobInvolvement = st.selectbox("Job Involvement", [1, 2, 3, 4])

    if st.button("Predict Performance Rating"):
        input_data = [[YearsAtCompany, Education, YearsInCurrentRole, YearsWithCurrManager, YearsSinceLastPromotion, JobInvolvement]]
        prediction = performance_model.predict(input_data)[0]
        st.success(f"Predicted Performance Rating: {prediction}")

# Page 3: Attrition Prediction
elif selected == "Attrition Prediction":
    st.title("❗ Attrition Risk Prediction")
    JobSatisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4])
    OverTime = st.selectbox("OverTime", ['No', 'Yes'])
    Education = st.selectbox("Education Level", [1, 2, 3, 4, 5])
    JobLevel = st.number_input("Job Level", 1, 5)
    YearsAtCompany = st.number_input("Years at Company", 0, 40)
    YearsInCurrentRole = st.number_input("Years in Current Role", 0, 20)
    TotalWorkingYears = st.number_input("Total Working Years", 0, 40)

    if st.button("Predict Attrition Risk"):
        OverTime_encoded = 1 if OverTime == 'Yes' else 0
        input_data = [[JobSatisfaction, OverTime_encoded, Education, JobLevel, YearsAtCompany, YearsInCurrentRole, TotalWorkingYears]]
        prediction = attrition_model.predict(input_data)[0]
        result = "YES" if prediction == 1 else "NO"
        st.success(f"Attrition Risk: {result}")

# Page 4: EDA Dashboard
if selected == "EDA Dashboard":
    st.title("📊 Interactive EDA Dashboard")
    eda_options = [
        "Job Satisfaction by Department",
        "Distance Travelled >15 Miles vs Attrition",
        "Monthly Income <5000 vs Attrition",
        "OverTime vs Attrition",
        "Job Satisfaction vs Attrition",
        "Performance Rating vs Attrition",
        "Correlation Heatmap"
    ]
    selected_chart = st.selectbox("Select EDA Analysis to View:", eda_options)

    if selected_chart == "Job Satisfaction by Department":
        st.subheader("Job Satisfaction by Department")
        datadepartment = data[['Department', 'JobSatisfaction']]
        low = datadepartment[datadepartment['JobSatisfaction'] == 1].groupby('Department').count().rename(columns={'JobSatisfaction': '1 - Low'})
        medium = datadepartment[datadepartment['JobSatisfaction'] == 2].groupby('Department').count().rename(columns={'JobSatisfaction': '2 - Medium'})
        high = datadepartment[datadepartment['JobSatisfaction'] == 3].groupby('Department').count().rename(columns={'JobSatisfaction': '3 - High'})
        very_high = datadepartment[datadepartment['JobSatisfaction'] == 4].groupby('Department').count().rename(columns={'JobSatisfaction': '4 - Very High'})
        merged_df = low.merge(medium, on='Department').merge(high, on='Department').merge(very_high, on='Department')

        fig = go.Figure()
        for col in merged_df.columns[1:]:
            fig.add_trace(go.Bar(x=merged_df.index, y=merged_df[col], name=col))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)

    elif selected_chart == "Distance Travelled >15 Miles vs Attrition":
        st.subheader("Distance Travelled >15 Miles vs Attrition")
        data['miles'] = data["DistanceFromHome"] > 15
        table = pd.crosstab(data['miles'], data['Attrition'])
        chi2, p, _, _ = chi2_contingency(table)
        norm = table.div(table.sum(axis=1), axis=0)
        fig, ax = plt.subplots()
        norm.plot(kind='bar', stacked=True, ax=ax, colormap='Accent')
        ax.set_title("Distance >15 Miles vs Attrition")
        ax.text(0.5, 1.05, f"Chi-Square p-value: {p:.4f}", transform=ax.transAxes, ha='center')
        st.pyplot(fig)

    elif selected_chart == "Monthly Income <5000 vs Attrition":
        st.subheader("Monthly Income <5000 vs Attrition")
        data['income5k'] = data['MonthlyIncome'] < 5000
        table = pd.crosstab(data['income5k'], data['Attrition'])
        chi2, p, _, _ = chi2_contingency(table)
        norm = table.div(table.sum(axis=1), axis=0)
        fig, ax = plt.subplots()
        norm.plot(kind='bar', stacked=True, ax=ax, colormap='Accent')
        ax.set_title("Income <5000 vs Attrition")
        ax.text(0.5, 1.5, f"Chi-Square p-value: {p:.4f}", transform=ax.transAxes, ha='center')
        st.pyplot(fig)

    elif selected_chart == "OverTime vs Attrition":
        st.subheader("OverTime vs Attrition")
        table = pd.crosstab(data['OverTime'], data['Attrition'])
        chi2, p, _, _ = chi2_contingency(table)
        norm = table.div(table.sum(axis=1), axis=0)
        fig, ax = plt.subplots()
        norm.plot(kind='bar', stacked=True, ax=ax, colormap='Accent')
        ax.set_title("OverTime vs Attrition")
        ax.text(0.5, 1.05, f"Chi-Square p-value: {p:.4f}", transform=ax.transAxes, ha='center')
        st.pyplot(fig)

    elif selected_chart == "Job Satisfaction vs Attrition":
        st.subheader("Job Satisfaction vs Attrition")
        table = pd.crosstab(data['JobSatisfaction'], data['Attrition'])
        chi2, p, _, _ = chi2_contingency(table)
        norm = table.div(table.sum(axis=1), axis=0)
        fig, ax = plt.subplots()
        norm.plot(kind='bar', stacked=True, ax=ax, colormap='Accent')
        ax.set_title("Job Satisfaction vs Attrition")
        ax.text(0.5, 1.05, f"Chi-Square p-value: {p:.4f}", transform=ax.transAxes, ha='center')
        st.pyplot(fig)

    elif selected_chart == "Performance Rating vs Attrition":
        st.subheader("Performance Rating vs Attrition")
        table = pd.crosstab(data['PerformanceRating'], data['Attrition'])
        chi2, p, _, _ = chi2_contingency(table)
        fig, ax = plt.subplots()
        sns.heatmap(table, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title("Performance Rating vs Attrition")
        ax.text(1.5, -0.5, f"Chi-Square p-value: {p:.4f}", ha='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='black'))
        st.pyplot(fig)

    elif selected_chart == "Correlation Heatmap":
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(data.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap of Numerical Features")
        st.pyplot(fig)
