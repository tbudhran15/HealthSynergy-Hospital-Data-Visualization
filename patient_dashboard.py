import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def patient_dashboard():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Patient Dashboard")
    data = pd.read_csv('HDHI Admission data.csv')

    # Add a text input box for MRD Number
    mrd_number = st.text_input("Enter MRD Number:")

    # Filter data based on MRD Number
    if mrd_number:
        filtered_data = data[data['MRD Number'] == mrd_number]

        # Display patient information
        st.subheader(f"Patient Statistics for MRD Number: {mrd_number}")
        st.write(filtered_data)

        # Calculate additional statistics
        num_visits = len(filtered_data)
        first_visit = filtered_data['Date of Admission'].min()
        last_visit = filtered_data['Date of Admission'].max()

        st.subheader("Additional Patient Statistics:")
        st.write(f"Number of Visits: {num_visits}")
        st.write(f"First Visit: {first_visit}")
        st.write(f"Last Visit: {last_visit}")

        # Calculate comorbidities statistics
        comorbidity_columns = [
            'Diabetes Mellitus (DM)', 'Hypertension (HTN)', 'Prior Coronary Artery Disease (CAD)',
            'Prior Cardiomyopathy (CMP)', 'Chronic Kidney Disease (CKD)', 'Ejection Fraction (EF)',
            'Severe Anemia', 'Anemia', 'Stable Angina', 'Acute Coronary Syndrome (ACS)',
            'ST-Elevation Myocardial Infarction (STEMI)', 'Atypical Chest Pain', 'Heart Failure',
            'Heart Failure with Reduced Ejection Fraction (HFREF)', 'Heart Failure with Normal Ejection Fraction (HFNEF)',
            'Valvular Heart Disease', 'Complete Heart Block (CHB)', 'Sick Sinus Syndrome (SSS)',
            'Acute Kidney Injury (AKI)', 'Cerebrovascular Accident (CVA) - Infarct', 'Cerebrovascular Accident (CVA) - Bleed',
            'Atrial Fibrillation (AF)', 'Ventricular Tachycardia (VT)', 'Paroxysmal Supraventricular Tachycardia (PSVT)',
            'Congenital Heart Disease', 'Urinary Tract Infection (UTI)', 'Neurocardiogenic Syncope',
            'Orthostatic Hypotension', 'Infective Endocarditis', 'Deep Vein Thrombosis (DVT)',
            'Cardiogenic Shock', 'Shock', 'Pulmonary Embolism'
        ]

        comorbidity_counts = filtered_data[comorbidity_columns].sum()
        st.subheader("Comorbidities Statistics:")
        st.bar_chart(comorbidity_counts)

        # Show Discharge Date for the First Visit
        
        first_visit_discharge_date = filtered_data.loc[filtered_data['Date of Admission'] == first_visit, 'Date of Discharge'].max()
        if first_visit_discharge_date is not pd.NaT:
            st.write(f"Discharge Date for the First Visit:{first_visit_discharge_date}")
        else:
            st.write("No discharge date available for the first visit.")

        last_visit_discharge_date = filtered_data.loc[filtered_data['Date of Admission'] == last_visit, 'Date of Discharge'].max()
        if last_visit_discharge_date is not pd.NaT:
            st.write(f"Discharge Date for the Last Visit:{last_visit_discharge_date}")
        else:
            st.write("No discharge date available for the last visit.")

# Run the dashboard function
if __name__ == '__main__':
    patient_dashboard()
