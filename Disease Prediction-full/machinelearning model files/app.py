import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np
from scipy.stats import f_oneway
from sklearn.preprocessing import LabelEncoder

# Load cleaned datasets
liver = pd.read_csv("/Users/narayansanthanam/Downloads/Disease Prediction/indian_liver_patient - indian_liver_patient.csv")
kidney = pd.read_csv('/Users/narayansanthanam/Downloads/Disease Prediction/kidney_disease - kidney_disease.csv')
parkinsons = pd.read_csv("/Users/narayansanthanam/Downloads/Disease Prediction/parkinsons - parkinsons.csv")

# Load models
kidney_model = pickle.load(open("/Users/narayansanthanam/Downloads/Disease Prediction/kidney.pkl", "rb"))
liver_model = pickle.load(open("/Users/narayansanthanam/Downloads/Disease Prediction/liver.pkl", "rb"))
parkinson_model = pickle.load(open("/Users/narayansanthanam/Downloads/Disease Prediction/parkinson.pkl", "rb"))

# Define features
kidney_features = ['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr',
                   'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc',
                   'htn', 'dm', 'cad', 'appet', 'pe', 'ane']

categorical_kidney_features = {
    'rbc': ['normal', 'abnormal'],
    'pc': ['normal', 'abnormal'],
    'pcc': ['notpresent', 'present'],
    'ba': ['notpresent', 'present'],
    'htn': ['no', 'yes'],
    'dm': ['no', 'yes'],
    'cad': ['no', 'yes'],
    'appet': ['good', 'poor'],
    'pe': ['no', 'yes'],
    'ane': ['no', 'yes']
}

liver_features = ['Age','Gender','Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase',
                  'Alamine_Aminotransferase', 'Aspartate_Aminotransferase',
                  'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio']

liver_categorical_features = {'Gender':['Male',"Female"]}

parkinson_features = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)',
                      'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP',
                      'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)',
                      'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA',
                      'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']

# Preprocessing
kidney['classification'] = kidney['classification'].map({'ckd': 'ckd', 'notckd': 'notckd'})
liver['Disease'] = liver['Dataset'].map({1: 'Liver Disease', 2: 'Healthy'})
parkinsons['status_label'] = parkinsons['status'].map({0: "Healthy", 1: "Parkinson"})

# Hypothesis Testing for Kidney
numeric_features = ['hemo', 'pcv', 'rc', 'bu', 'sc', 'bgr']
result = []
for feature in numeric_features:
    ckd_group = kidney[kidney['classification'] == 'ckd'][feature].dropna()
    notckd_group = kidney[kidney['classification'] == 'notckd'][feature].dropna()
    stat, p = f_oneway(ckd_group, notckd_group)
    if p < 0.05:
        result.append({'Feature': feature, 'p-value': p})
result_df = pd.DataFrame(result)
result_df['p-value'] = pd.to_numeric(result_df['p-value'], errors='coerce')

# Create 'Significant' column
result_df['Significant'] = result_df['p-value'].apply(
    lambda x: 'Yes' if pd.notnull(x) and x < 0.05 else 'No'
)

# Format p-values to scientific notation for display
result_df['p-value'] = result_df['p-value'].map(lambda x: f"{x:.10e}" if pd.notnull(x) else "NA")


from scipy.stats import f_oneway
import pandas as pd

numeric_features = [
    'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase',
    'Alamine_Aminotransferase', 'Aspartate_Aminotransferase',
    'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio'
]

results = []

# Perform ANOVA for each feature
for feature in numeric_features:
    group1 = liver[liver['Dataset'] == 1][feature].dropna()
    group2 = liver[liver['Dataset'] == 2][feature].dropna()

    if len(group1) >= 2 and len(group2) >= 2:
        stat, p = f_oneway(group1, group2)
        results.append({'Feature': feature, 'p-value': p})
    else:
        results.append({'Feature': feature, 'p-value': None})

# Create DataFrame
result_liver = pd.DataFrame(results)

# Ensure 'p-value' is float
result_liver['p-value'] = pd.to_numeric(result_liver['p-value'], errors='coerce')

# Create 'Significant' column
result_liver['Significant'] = result_liver['p-value'].apply(
    lambda x: 'Yes' if pd.notnull(x) and x < 0.05 else 'No'
)

# Format p-values to scientific notation for display
result_liver['p-value'] = result_liver['p-value'].map(lambda x: f"{x:.10e}" if pd.notnull(x) else "NA")

#parkinsons

from scipy.stats import ttest_ind
from scipy.stats import f_oneway
import pandas as pd


numeric_features = [ 'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
       'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
       'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
       'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA',
       'spread1', 'spread2', 'D2', 'PPE']

results = []

# Perform t-test for each feature
for feature in numeric_features:
    group1 = parkinsons[parkinsons['status'] == 1][feature].dropna()
    group2 = parkinsons[parkinsons['status'] == 0][feature].dropna()
    
    if len(group1) >= 2 and len(group2) >= 2:
        stat, p = f_oneway(group1, group2)
        results.append({'Feature': feature, 'p-value': p})
    else:
        results.append({'Feature': feature, 'p-value': None})

# Convert to DataFrame
result_park = pd.DataFrame(results)
result_park['p-value'] = pd.to_numeric(result_park['p-value'],errors='coerce')
result_park['Significant'] = result_park['p-value'].apply(lambda x: 'Yes' if pd.notnull(x) and x < 0.05 else 'No')
result_park['p-value'] = result_park['p-value'].map(lambda x : f'{x:.6e}' if pd.notnull(x) else "NA")


kidney_hypo = result_df
liver_hypo = result_liver
parkinson_hypo = result_park

hypothesis_results = {
    'Kidney': kidney_hypo,
    'Liver': liver_hypo,
    'Parkinson': parkinson_hypo
}

# Chart loading function (unchanged for brevity)

def load_chart(dataset, chart_name):
    if dataset == 'Kidney':
        if chart_name == 'Hemoglobin Classification':
            low_hemo = kidney[kidney['hemo'] < 13].copy()
            low_hemo['hemo_level'] = 'Low (<13)'
            high_hemo = kidney[kidney['hemo'] > 13].copy()
            high_hemo['hemo_level'] = 'High (>13)'
            combined_hemo = pd.concat([low_hemo, high_hemo])
            hemo_class_counts = combined_hemo.groupby(['hemo_level', 'classification']).size().reset_index(name='count')
            return px.bar(hemo_class_counts, x='hemo_level', y='count', color='classification', barmode='group', text='count', title='Number of Patients by Hemoglobin Level and CKD Classification')

        elif chart_name == 'Age vs CKD Outcome':
            bins = [0, 30, 50, 70, 100]
            labels = ['<30', '30–50', '50–70', '70+']
            kidney['age_group'] = pd.cut(kidney['age'], bins=bins, labels=labels)
            age_class_counts = kidney.groupby(['age_group', 'classification']).size().reset_index(name='count')
            return px.bar(age_class_counts, x='age_group', y='count', color='classification', barmode='group', text='count', title='Number of CKD and Non-CKD Patients Across Age Groups')

        elif chart_name == 'Age vs Pus Cells':
            bins = [0, 30, 50, 70, 100]
            labels = ["<30", "30-50", "50-70", "70+"]
            kidney['age_group'] = pd.cut(kidney['age'], bins=bins, labels=labels)
            age_pc_counts = kidney.groupby(["age_group", 'pc', 'classification']).size().reset_index(name='count')
            return px.bar(age_pc_counts, x='age_group', y='count', color='classification', facet_col='pc', barmode='group', text='count', title='Distribution of Pus Cells and Classification Across Age Groups')

    elif dataset == 'Liver':
        if chart_name == 'Age & Gender vs Disease':
            bins = [0, 30, 50, 70, 100]
            labels = ['<30', '30–50', '50–70', '70+']
            liver['age_group'] = pd.cut(liver['Age'], bins=bins, labels=labels)
            liver['Disease'] = liver['Dataset'].map({1: 'Liver Disease', 2: 'Healthy'})
            grouped = liver.groupby(['age_group', 'Gender', 'Disease']).size().reset_index(name='count')
            return px.bar(grouped, x='age_group', y='count', color='Disease', barmode='group', facet_col='Gender', text='count', title='Liver Disease Cases by Age Group and Gender')
                

    elif dataset == 'Parkinson':
        if chart_name == 'Correlation Heatmap':
            import seaborn as sns
            import matplotlib.pyplot as plt
            import streamlit as st
            # Make a copy to avoid modifying original data
            df_corr = parkinsons.copy()
            if 'name' in df_corr.columns:
                df_corr.drop(columns='name', inplace=True)
                
            fig, ax = plt.subplots(figsize=(20, 15))
            correlation_matrix = df_corr.select_dtypes(include=[np.number]).corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)
            return None 
                
        elif chart_name == 'Boxplots of Acoustic Features':
            import streamlit as st
            parkinsons['status_label'] = parkinsons['status'].map({0: "Healthy", 1: "Parkinson"})
            top_features = ['MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)']
            selected_feature = st.selectbox("Select Feature to View", top_features)
            fig = px.box(
                        parkinsons,
                        x='status_label',
                        y=selected_feature,
                        color='status_label',
                        title=f'{selected_feature} Distribution by Parkinson Status',
                        points='all'
                        )
            fig.update_layout(xaxis_title='Status', yaxis_title=selected_feature, showlegend=False)
            return fig

    return None
# ...

# Streamlit Layout
st.title("Disease Prediction & Medical Analysis Dashboard")
section = st.sidebar.selectbox("Select Section", ["Prediction", "Hypothesis Testing", "Visual Charts"])

if section == "Prediction":
    st.subheader("Disease Prediction")
    disease = st.selectbox("Select Disease", ["Kidney", "Liver", "Parkinson"])

    if disease == "Kidney":
        inputs = []
        for feature in kidney_features:
            if feature in categorical_kidney_features:
                val = st.selectbox(f"Select {feature}", categorical_kidney_features[feature])
                le = LabelEncoder()
                le.fit(categorical_kidney_features[feature])
                encoded = le.transform([val])[0]
                inputs.append(encoded)
            else:
                inputs.append(st.number_input(f"Enter {feature}", step=0.1))

        if st.button("Predict Kidney Disease"):
            prediction = kidney_model.predict([inputs])[0]
            st.success(f"Prediction: {'CKD Positive' if prediction == 1 else 'CKD Negative'}")

    elif disease == "Liver":
        inputs = []
        for feature in liver_features:
            if feature in liver_categorical_features:
                val = st.selectbox(f"Select {feature}", liver_categorical_features[feature])
                le = LabelEncoder()
                le.fit(liver_categorical_features[feature])
                encoded = le.transform([val])[0]
                inputs.append(encoded)
            else:
                inputs.append(st.number_input(f"Enter {feature}", step=0.1))

        if st.button("Predict Liver Disease"):
            prediction = liver_model.predict([inputs])[0]
            st.success(f"Prediction: {'Liver Disease' if prediction == 1 else 'Healthy'}")

    elif disease == "Parkinson":
        inputs = [st.number_input(f"Enter {f}", step=0.01) for f in parkinson_features]
        if st.button("Predict Parkinson Disease"):
            prediction = parkinson_model.predict([inputs])[0]
            st.success(f"Prediction: {'Parkinson Positive' if prediction == 1 else 'Healthy'}")

elif section == "Hypothesis Testing":
    dataset = st.selectbox("Select Dataset", list(hypothesis_results.keys()))
    st.subheader(f"Hypothesis Testing - {dataset}")
    st.dataframe(hypothesis_results[dataset])


elif section == "Visual Charts":
    st.subheader("📊 Visual Exploration of Datasets")

    chart_options = {
        'Kidney': [
            'Hemoglobin Classification',
            'Age vs CKD Outcome',
            'Age vs Pus Cells'
        ],
        'Liver': [
            'Age & Gender vs Disease'
        ],
        'Parkinson': [
            'Boxplots of Acoustic Features',
            'Correlation Heatmap'
        ]
    }
    
    dataset = st.selectbox("Select Dataset", list(chart_options.keys()))
    chart_name = st.selectbox("Select Chart", chart_options[dataset])
    st.subheader("📊 Visual Exploration of Datasets")

    fig = load_chart(dataset, chart_name)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
    elif fig is None and dataset == 'Parkinson' and chart_name == 'Correlation Heatmap':
        pass  # already displayed via st.pyplot
    else:
        st.warning("Chart not available.")
        
    
   


