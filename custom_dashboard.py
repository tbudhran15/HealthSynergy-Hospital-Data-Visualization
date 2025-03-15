import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def is_float_column(series):
    # Check if the series contains float values
    return series.dtype == 'float64' or any('.' in str(value) for value in series)

def custom_dashboard():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Custom Dashboard")
# Additional information about the dataset
    dataset_info = """
    The dataset contains information related to hospital admissions, including patient details, date of admission, date of discharge, demographics, and various health parameters. Here are some key features:

    - **Demographics:** Age, sex, locality (rural or urban)
    - **Admission Details:** Type of admission (emergency or outpatient)
    - **Patient History:** Smoking, alcohol consumption, diabetes mellitus (DM), hypertension (HTN), prior coronary artery disease (CAD), prior cardiomyopathy (CMP), and chronic kidney disease (CKD)
    - **Lab Parameters:** Hemoglobin (HB), total lymphocyte count (TLC), platelets, glucose, urea, creatinine, brain natriuretic peptide (BNP), raised cardiac enzymes (RCE), and ejection fraction (EF)
    - **Comorbidities and Features:** 28 features including heart failure, STEMI, and pulmonary embolism

    Shock categories:
    - **Cardiogenic Shock:** Systolic blood pressure < 90 mmHg due to cardiac reasons
    - **Multifactorial Shock:** Systolic blood pressure < 90 mmHg due to multifactorial pathophysiology (cardiac and non-cardiac)

    Outcomes:
    - **Discharge:** Indicates whether the patient was discharged from the hospital
    - **Expired:** Indicates whether the patient expired in the hospital
    """

    # Display dataset details
    st.markdown("## Dataset Information")
    st.markdown(dataset_info)
    data = pd.read_csv('HDHI Admission data.csv')

    # Rename columns to match the dataset description
    data.rename(columns={
        'SNO': 'Serial Number',
        'MRD No.': 'MRD Number',
        'D.O.A': 'Date of Admission',
        'D.O.D': 'Date of Discharge',
        'AGE': 'Age',
        'GENDER': 'Gender',
        'RURAL': 'Locality (Rural/Urban)',
        'TYPE OF ADMISSION-EMERGENCY/OPD': 'Type of Admission (Emergency/Outpatient)',
        'month year': 'Month Year',
        'DURATION OF STAY': 'Duration of Stay',
        'duration of intensive unit stay': 'Duration of Intensive Unit Stay',
        'OUTCOME': 'Outcome',
        'SMOKING': 'Smoking',
        'ALCOHOL': 'Alcohol',
        'DM': 'Diabetes Mellitus (DM)',
        'HTN': 'Hypertension (HTN)',
        'CAD': 'Prior Coronary Artery Disease (CAD)',
        'PRIOR CMP': 'Prior Cardiomyopathy (CMP)',
        'CKD': 'Chronic Kidney Disease (CKD)',
        'HB': 'Hemoglobin (HB)',
        'TLC': 'Total Lymphocyte Count (TLC)',
        'PLATELETS': 'Platelets',
        'GLUCOSE': 'Glucose',
        'UREA': 'Urea',
        'CREATININE': 'Creatinine',
        'BNP': 'Brain Natriuretic Peptide (BNP)',
        'RAISED CARDIAC ENZYMES': 'Raised Cardiac Enzymes',
        'EF': 'Ejection Fraction (EF)',
        'SEVERE ANAEMIA': 'Severe Anemia',
        'ANAEMIA': 'Anemia',
        'STABLE ANGINA': 'Stable Angina',
        'ACS': 'Acute Coronary Syndrome (ACS)',
        'STEMI': 'ST-Elevation Myocardial Infarction (STEMI)',
        'ATYPICAL CHEST PAIN': 'Atypical Chest Pain',
        'HEART FAILURE': 'Heart Failure',
        'HFREF': 'Heart Failure with Reduced Ejection Fraction (HFREF)',
        'HFNEF': 'Heart Failure with Normal Ejection Fraction (HFNEF)',
        'VALVULAR': 'Valvular Heart Disease',
        'CHB': 'Complete Heart Block (CHB)',
        'SSS': 'Sick Sinus Syndrome (SSS)',
        'AKI': 'Acute Kidney Injury (AKI)',
        'CVA INFRACT': 'Cerebrovascular Accident (CVA) - Infarct',
        'CVA BLEED': 'Cerebrovascular Accident (CVA) - Bleed',
        'AF': 'Atrial Fibrillation (AF)',
        'VT': 'Ventricular Tachycardia (VT)',
        'PSVT': 'Paroxysmal Supraventricular Tachycardia (PSVT)',
        'CONGENITAL': 'Congenital Heart Disease',
        'UTI': 'Urinary Tract Infection (UTI)',
        'NEURO CARDIOGENIC SYNCOPE': 'Neurocardiogenic Syncope',
        'ORTHOSTATIC': 'Orthostatic Hypotension',
        'INFECTIVE ENDOCARDITIS': 'Infective Endocarditis',
        'DVT': 'Deep Vein Thrombosis (DVT)',
        'CARDIOGENIC SHOCK': 'Cardiogenic Shock',
        'SHOCK': 'Shock',
        'PULMONARY EMBOLISM': 'Pulmonary Embolism',
        'CHEST INFECTION': 'Chest Infection'
    }, inplace=True)

    # Sidebar to select analysis type
    analysis_type = st.sidebar.selectbox("Select Analysis Type", ["Univariate", "Bivariate"])
    
    if analysis_type == "Univariate":
        st.subheader("Univariate Analysis")
        
        # Let the user select a variable for analysis
        selected_variable = st.selectbox("Select a variable for analysis", data.columns)

        # Check if the variable is continuous or discrete based on unique value counts
        unique_values_count = len(data[selected_variable].unique())

        if unique_values_count > 15:
            st.sidebar.markdown("Selected Variable Type: Continuous")
            graph_type = st.sidebar.radio("Select Graph Type", ["Histogram", "Density Plot", "Box Plot", "KDE Plot"])

            if graph_type == "Histogram":
                st.subheader("Histogram")
                sns.histplot(data=data, x=selected_variable, bins=20, kde=True)
                st.pyplot()

            elif graph_type == "Density Plot":
                st.subheader("Density Plot")
                sns.kdeplot(data=data, x=selected_variable)
                st.pyplot()

            elif graph_type == "Box Plot":
                st.subheader("Box Plot")
                sns.boxplot(data=data, x=selected_variable)
                st.pyplot()

            elif graph_type == "KDE Plot":
                st.subheader("Kernel Density Estimation (KDE) Plot")
                sns.kdeplot(data=data, x=selected_variable)
                st.pyplot()

        else:
            st.sidebar.markdown("Selected Variable Type: Discrete")
            graph_type = st.sidebar.radio("Select Graph Type", ["Bar Chart", "Count Plot", "Pie Chart"])

            if graph_type == "Bar Chart":
                st.subheader("Bar Chart")
                sns.barplot(x=data[selected_variable].value_counts().index, y=data[selected_variable].value_counts().values)
                plt.xticks(rotation=45)
                st.pyplot()

            elif graph_type == "Count Plot":
                st.subheader("Count Plot")
                sns.countplot(data=data, x=selected_variable)
                plt.xticks(rotation=45)
                st.pyplot()

            elif graph_type == "Pie Chart":
                st.subheader("Pie Chart")
                pie_data = data[selected_variable].value_counts()
                plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
                st.pyplot()

    elif analysis_type == "Bivariate":
        st.subheader("Bivariate Analysis")

        # Generate a list of columns with float or integer values
        numeric_columns = [col for col in data.columns if is_float_column(data[col]) or pd.api.types.is_integer_dtype(data[col])]
        selected_columns = st.multiselect("Select two variables for bivariate analysis", numeric_columns)

        if len(selected_columns) != 2:
            st.warning("Please select exactly two variables for bivariate analysis.")
        else:
            variable1, variable2 = selected_columns
            st.subheader("Scatter Plot")
            sns.scatterplot(data=data, x=variable1, y=variable2)
            st.pyplot()

# Run the Streamlit app
if __name__ == '__main__':
    custom_dashboard()
