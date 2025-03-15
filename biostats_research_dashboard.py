import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
import plotly.graph_objects as go


def biostats_research_dashboard():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Bio Stats Research Dashboard")
    data = pd.read_csv('HDHI Admission data.csv')
    

    # Filter data based on age
    min_age = data['Age'].min()
    max_age = data['Age'].max()

    # Create a new dataframe with reduced sample size
    new_data = pd.DataFrame()

    # Select 50 data points for every 10-year age difference
    for age in np.arange(min_age, max_age, 10):
        age_subset = data[(data['Age'] >= age) & (data['Age'] < age + 10)].sample(n=100, replace=True)
        new_data = pd.concat([new_data, age_subset])

    sns.set_palette("viridis")

    # Scatterplot with loess lines for Age and Duration of Stay
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Age', y='Duration of Stay', data=new_data, ax=ax1, alpha=0.5)
    sns.regplot(x='Age', y='Duration of Stay', data=new_data, scatter=False, lowess=True, line_kws={'color': 'red'}, ax=ax1)
    ax1.set_title('Relationship between Age and Duration of Stay ')
    st.pyplot(fig1)

    # Scatterplot with loess lines for Age and Duration of Intensive Unit Stay
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Age', y='Duration of Intensive Unit Stay', data=new_data, ax=ax2, alpha=0.5)
    sns.regplot(x='Age', y='Duration of Intensive Unit Stay', data=new_data, scatter=False, lowess=True, line_kws={'color': 'pink'}, ax=ax2)
    ax2.set_title('Relationship between Age and Duration of Intensive Unit Stay')
    st.pyplot(fig2)

    # Remove rows with non-numeric values in 'Platelets'
    new_data = new_data[pd.to_numeric(new_data['Platelets'], errors='coerce').notnull()]

    # Convert 'Platelets' to numeric, replacing any non-numeric values with NaN
    new_data['Platelets'] = pd.to_numeric(new_data['Platelets'], errors='coerce')

    # Create 10 ranges for Platelets
    platelet_bins = np.linspace(new_data['Platelets'].min(), new_data['Platelets'].max(), 11)

    # Create labels for platelet ranges
    platelet_labels = [f"{int(platelet_bins[i])}-{int(platelet_bins[i+1])}" for i in range(len(platelet_bins)-1)]

    # Create a new column 'Platelet Range' with the corresponding range for each value
    new_data['Platelet Range'] = pd.cut(new_data['Platelets'], bins=platelet_bins, labels=platelet_labels, include_lowest=True)

    # Scatterplot with loess lines for Age, Platelet count, and DM
    fig3, ax3 = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='Age', y='Platelets', hue='Diabetes Mellitus (DM)', data=new_data, alpha=0.7)
    sns.regplot(x='Age', y='Platelets', data=new_data, scatter=False, lowess=True, line_kws={'color': 'purple'})
    ax3.set_title('Relationship between Age, Platelet count, and Diabetes Mellitus (Reduced Sample)')
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='Duration of Stay', y='Hypertension (HTN)', hue='Chronic Kidney Disease (CKD)', data=new_data, palette='viridis', alpha=0.7)
    sns.regplot(x='Duration of Stay', y='Hypertension (HTN)', data=new_data, scatter=False, lowess=True, line_kws={'color': 'orange'})
    ax4.set_title('Interaction effect between HTN, CKD, and Duration of Stay')
    st.pyplot(fig4)


    new_data = new_data[pd.to_numeric(new_data['Hemoglobin (HB)'], errors='coerce').notnull()]

    # Convert 'Hemoglobin (HB)' to numeric, replacing any non-numeric values with NaN
    new_data['Hemoglobin (HB)'] = pd.to_numeric(new_data['Hemoglobin (HB)'], errors='coerce')

    # Create 10 ranges for Hemoglobin
    hemoglobin_bins = np.linspace(new_data['Hemoglobin (HB)'].min(), new_data['Hemoglobin (HB)'].max(), 11)

    # Create labels for hemoglobin ranges
    hemoglobin_labels = [f"{int(hemoglobin_bins[i])}-{int(hemoglobin_bins[i+1])}" for i in range(len(hemoglobin_bins)-1)]

    # Create a new column 'Hemoglobin Range' with the corresponding range for each value
    new_data['Hemoglobin Range'] = pd.cut(new_data['Hemoglobin (HB)'], bins=hemoglobin_bins, labels=hemoglobin_labels, include_lowest=True)

    # Scatterplot with loess lines for Hemoglobin, Duration of Intensive Unit Stay, and Heart Failure
    fig5, ax5 = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='Hemoglobin (HB)', y='Duration of Intensive Unit Stay', hue='Heart Failure', data=new_data, palette='Set1', alpha=0.7)
    sns.regplot(x='Hemoglobin (HB)', y='Duration of Intensive Unit Stay', data=new_data, scatter=False, lowess=True, line_kws={'color': 'green'})
    ax5.set_title('Relationship between HB, Duration of Intensive Unit Stay, and Heart Failure ')
    st.pyplot(fig5)


if __name__ == '__main__':
    biostats_research_dashboard()
