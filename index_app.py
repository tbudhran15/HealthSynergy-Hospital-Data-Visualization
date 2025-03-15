import streamlit as st
import pandas as pd
from main_dashboard import main_dashboard
from custom_dashboard import custom_dashboard
from patient_dashboard import patient_dashboard
from biostats_research_dashboard import biostats_research_dashboard
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


#Set page title and favicon
st.set_page_config(
    page_title="Hospital Dashboard"
)

st.sidebar.title('Dashboard Navigation')
selected_option = st.sidebar.selectbox('Select a Dashboard', ['Hospital Statistics Dashboard', 'Main Dashboard', 'Custom Dashboard','Patient Dashboard','BioStats Research Dashboard'])


# Create a function to display the selected dashboard content
def display_dashboard():
    
    if selected_option == 'Hospital Statistics Dashboard':
        st.subheader('Welcome to the Hospital Dashboard!')
        st.write("Please select a dashboard from the sidebar to explore the data.")
        data = pd.read_csv('HDHI Admission data.csv')

        # Convert 'Date of Admission' to datetime format
        data['Date of Admission'] = pd.to_datetime(data['Date of Admission'], errors='coerce')
        data['Type of Admission (Emergency/Outpatient)'].replace(
            {'E': 'Emergency', 'O': 'Outpatient'},
            inplace=True
        )

        # Randomly update 30% of 'Emergency' to 'Inpatient'
        emergency_indices = data[data['Type of Admission (Emergency/Outpatient)'] == 'Emergency'].sample(frac=0.3).index
        data.loc[emergency_indices, 'Type of Admission (Emergency/Outpatient)'] = 'Inpatient'


        # Display Hospital Dashboard title and importance
        st.title("Hospital Dashboard")
        st.image("Hospital_banner.jpg", use_column_width=True)
        st.markdown(
            """
            Welcome to the Hospital Dashboard, where data meets care! 🌟
            
            Explore the heartbeat of our hospital with a single click. Whether you're interested
            in the big picture or craving a deep dive, our dashboards have got you covered.
            
            Ready to embark on this data-driven journey? Choose a dashboard from the sidebar, and
            let's dive into the world of insights and analysis.
            """
        )

        

        # Display hospital statistics on 'Select Dashboard' page
        st.title('Hospital Statistics')

        # Add a month filter in the sidebar
        selected_month = st.sidebar.selectbox('Select a Month', ['Overall'] + list(range(1, 13)), 0)

        # Filter data based on the selected month or show overall statistics
        if selected_month == 'Overall':
            filtered_data = data
        else:
            filtered_data = data[data['Date of Admission'].dt.month == selected_month]

        # Display hospital statistics in the main part of the dashboard
        total_patients = len(filtered_data)
        outcome_distribution = filtered_data['Outcome'].value_counts()

        # Calculate the lengths of different outcome categories
        discharged_length = str(100 - int(round((len(filtered_data[filtered_data['Outcome'] == 'EXPIRY']) / total_patients) * 100, 0))) + "%"
        expiry_length = str(int(round((len(filtered_data[filtered_data['Outcome'] == 'EXPIRY']) / total_patients) * 100, 0))) + "%"


        col1, col2, col3= st.columns(3)

        # Define a function to create a decorated box
        def create_box(title, value, col):
            box_style = "border: 2px solid #4682B4; border-radius: 10px; padding: 10px; background-color: #E0EBF5; width: 150px; height:150px;"
            col.markdown(
                f"""
                <div style="{box_style}">
                    <h3 style="color: #4682B4;">{title}</h3>
                    <p style="font-size: 20px; font-weight: bold; color: #1E90FF;">{value}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Create decorated boxes for total patients, discharged patients, expiry patients, and DAMA patients
        create_box("Total Patients", total_patients, col1)
        create_box("Discharge Rate", discharged_length, col2)
        create_box("Mortality Rate", expiry_length, col3)

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

        # Sum the occurrences of each comorbidity
        comorbidity_counts = filtered_data[comorbidity_columns].sum(numeric_only=True)

        top_07_comorbidities = pd.DataFrame(comorbidity_counts.sort_values(ascending=False).head(7)).reset_index()
        top_07_comorbidities.columns=['Commorbidities','Count']
        comorbidity_columns_of_interest=top_07_comorbidities['Commorbidities'].to_list()

        selected_comorbidities_data = filtered_data[comorbidity_columns_of_interest]

        # Create a pivot table to get counts
        comorbidity_counts = selected_comorbidities_data.sum()

        st.title('Comorbidities Statistics')

        # Create a tree map using plotly express
        fig = px.treemap(names=comorbidity_counts.index, parents=[''] * len(comorbidity_counts),
                        values=comorbidity_counts.values,
                        color=comorbidity_counts.values, color_continuous_scale='darkmint',  # Use 'darkmint' for darker colors
                        labels={'value': 'Count'},
                        custom_data=[comorbidity_counts.index, comorbidity_counts.values])

        # Update the layout to display values and names in bold
        fig.update_traces(textinfo='label+value', hovertemplate='<b>%{label}</b><br>Count: %{value}')

        st.plotly_chart(fig)
        st.title('Hospital Visits')
        filtered_data['Date of Admission'] = pd.to_datetime(filtered_data['Date of Admission'], errors='coerce')

        # Extract day from the 'Date of Admission' column
        filtered_data['Admission Day'] = filtered_data['Date of Admission'].dt.day

        # Count the occurrences for each day
        day_counts = filtered_data['Admission Day'].value_counts().sort_index()

        # Create a DataFrame with all days from 1 to 31
        all_days = pd.DataFrame({'Day': range(1, 32)})

        # Merge with day_counts to fill NaN values with 0
        day_counts_df = pd.merge(all_days, day_counts, left_on='Day', right_index=True, how='left').fillna(0)

        # Create a line plot with shaded area
        fig = px.area(day_counts_df, x='Day', y='Admission Day', labels={'x': 'Day', 'y': 'Number of Admissions'})

        # Display the plot using Streamlit
        st.plotly_chart(fig)


        col1, col2 = st.columns((2))

        with col1:
            # Set up Streamlit layout
            st.title('Admission wise Patients')

            admission_counts = filtered_data['Type of Admission (Emergency/Outpatient)'].value_counts().reset_index()

            # Rename columns for clarity
            admission_counts.columns = ['Type of Admission', 'Count']

            fig = px.pie(admission_counts, values='Count', names='Type of Admission', hole=0.4,template = "plotly_dark")
            fig.update_traces(textinfo='percent+label',textposition='outside')
            fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='black',
        font=dict(color='white'),
        showlegend=False  # Hide the legend
    )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            locality_counts = filtered_data['Locality (Rural/Urban)'].replace({'U': 'Urban', 'R': 'Rural'}).value_counts().reset_index()
            locality_counts.columns = ['Locality', 'Count']

            st.title("Locality wise Patients")

            # Plot bar chart using Plotly Express
            fig = px.bar(locality_counts, x='Locality', y='Count', text='Count', template='seaborn')


            # Show the plot in Streamlit
            st.plotly_chart(fig, use_container_width=True, height=200)




        sns.set_style('whitegrid')

        st.title('KDE Plot for Durations with Mean')



# Set the style to dark background
        sns.set(style="darkgrid")

        # Create a figure and axes with a black background
        fig, ax = plt.subplots(figsize=(10, 6), dpi=80)
        ax.set_facecolor('black')
        ax.grid(color='white', linestyle='--', linewidth=0.5)

        

        # KDE plot for 'Duration of Stay'
        sns.kdeplot(filtered_data['Duration of Stay'], color='blue', label='Duration of Stay', ax=ax)

        # KDE plot for 'Duration of Intensive Unit Stay'
        sns.kdeplot(filtered_data['Duration of Intensive Unit Stay'], color='orange', label='Duration of Intensive Unit Stay', ax=ax)

        # Add vertical lines for the mean of each distribution
        mean_duration_stay = filtered_data['Duration of Stay'].mean()
        mean_duration_intensive_unit_stay = filtered_data['Duration of Intensive Unit Stay'].mean()

        ax.axvline(mean_duration_stay, color='blue', linestyle='dashed', linewidth=2, label=f'Mean Duration of Stay: {mean_duration_stay:.2f}')
        ax.axvline(mean_duration_intensive_unit_stay, color='orange', linestyle='dashed', linewidth=2, label=f'Mean Duration of Intensive Unit Stay: {mean_duration_intensive_unit_stay:.2f}')

        # Set legend and title
        ax.legend()
        ax.set_title('Duration of Stay and Intensive Unit Stay', color='white')

        # Set axis labels and tick colors
        ax.set_xlabel('Duration', color='black')
        ax.set_ylabel('Density', color='black')
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')

        # Show the plot
        st.pyplot(fig)


       


   


        
    elif selected_option == 'Main Dashboard':
        st.subheader('Main Dashboard')
        st.write("The Main Dashboard provides an overview of key metrics and statistics related to hospital admissions.")
        st.write("Here are some features:")
        st.markdown("- **Patient Demographics:** Visualizations showcasing age distribution, gender ratios, etc.")
        st.markdown("- **Admission Trends:** Charts representing admission trends over time.")
        st.markdown("- **Outcome Analysis:** Insightful graphs on patient outcomes.")
        main_dashboard()

    elif selected_option == 'Custom Dashboard':
        st.subheader('Custom Dashboard')
        st.write("The Custom Dashboard allows you to perform detailed analyses based on your preferences.")
        st.write("Here's what you can do:")
        st.markdown("- **Univariate Analysis:** Explore individual variables with various chart options.")
        st.markdown("- **Bivariate Analysis:** Investigate relationships between two variables.")
        st.write("Choose your analysis type from the sidebar and dive into the data!")
        custom_dashboard()
    
    elif selected_option == 'Patient Dashboard':
        st.subheader('Patient Dashboard')
        st.write("The Patient Dashboard allows you to perform detailed analyses based on the patient ID.")
        st.write("Here's what you can do:")
        patient_dashboard()

    elif selected_option == 'BioStats Research Dashboard':
        st.subheader('Bio Stats  Dashboard')
        biostats_research_dashboard()


    
        
# Display the selected dashboard content
display_dashboard()
