import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_dashboard():
    # Your main dashboard content goes here
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

    st.sidebar.title('Dashboard Options')

    # Sidebar filter options
    selected_gender = st.sidebar.selectbox('Select Gender', data['Gender'].unique())
    selected_age = st.sidebar.slider('Select Age', float(data['Age'].min()), float(data['Age'].max()), (float(data['Age'].min()), float(data['Age'].max())))

    # Filter the data based on user selections
    filtered_data = data[(data['Gender'] == selected_gender) & (data['Age'] >= selected_age[0]) & (data['Age'] <= selected_age[1])]

    # Display the filtered data
    st.write('### Filtered Data')
    st.write(filtered_data)

    # Create a 2x2 grid layout for plots using subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

    # Plot 1: Bar chart
    axes[0, 0].set_title('Outcome Counts')
    bar_data = filtered_data['Outcome'].value_counts()
    bar_data.plot(kind='bar', ax=axes[0, 0], rot=0)
    axes[0, 0].set_ylabel('Count')

    # Plot 2: Histogram for Age
    axes[0, 1].set_title('Age Distribution')
    sns.histplot(data=filtered_data, x='Age', bins=20, kde=True, ax=axes[0, 1])
    axes[0, 1].set_xlabel('Age')
    axes[0, 1].set_ylabel('Count')

    # Plot 3: Line chart
    axes[1, 0].set_title('Admission Count Over Time')
    line_data = filtered_data.groupby('Date of Admission').size().reset_index(name='Count')
    line_data['Date of Admission'] = pd.to_datetime(line_data['Date of Admission'])
    axes[1, 0].plot(line_data['Date of Admission'], line_data['Count'])
    axes[1, 0].set_xlabel('Date of Admission')
    axes[1, 0].set_ylabel('Count')

    # Plot 4: Box plot for Age by Outcome
    axes[1, 1].set_title('Age Distribution by Outcome')
    sns.boxplot(x='Outcome', y='Age', data=filtered_data, ax=axes[1, 1])
    axes[1, 1].set_xlabel('Outcome')
    axes[1, 1].set_ylabel('Age')

    # Adjust layout
    plt.tight_layout()

    # Display the Matplotlib plot using Streamlit
    st.pyplot(fig)

# Run the Streamlit app
if __name__ == '__main__':
    main_dashboard()
