import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20c

# Load your dataset
data = pd.read_csv('HDHI Admission data.csv')

# Convert column names to uppercase
data.columns = data.columns.str.upper()

# Create a Streamlit sidebar for user input
st.sidebar.title('Dashboard Options')

# Sidebar filter options
selected_gender = st.sidebar.selectbox('Select Gender', ['M', 'F'])
selected_age_range = st.sidebar.slider('Select Age Range', int(data['AGE'].min()), int(data['AGE'].max()), (int(data['AGE'].min()), int(data['AGE'].max())))

# Filter the data based on user selections
filtered_data = data[(data['GENDER'] == selected_gender) & (data['AGE'] >= selected_age_range[0]) & (data['AGE'] <= selected_age_range[1])]

# Display the filtered data
st.write('### Filtered Data')
st.write(filtered_data)

# Create Bokeh plots
st.write('### Interactive Bokeh Plots')

# Example: Scatter plot using Bokeh
source = ColumnDataSource(filtered_data)
scatter_plot = figure(plot_width=800, plot_height=400, title="Scatter Plot")
scatter_plot.circle(x='AGE', y='BPSYSAVE', source=source, size=10, color=Category20c[3][0])  # Adjusted column name
scatter_plot.xaxis.axis_label = "Age"
scatter_plot.yaxis.axis_label = "Systolic Blood Pressure"
st.bokeh_chart(scatter_plot)

# Example: Bar chart using Bokeh
bar_data = filtered_data['OUTCOME'].value_counts()
bar_chart = figure(x_range=bar_data.index.tolist(), plot_height=350, title="Outcome Counts")
bar_chart.vbar(x=bar_data.index.tolist(), top=bar_data.values, width=0.4, color=Category20c[3])
bar_chart.xaxis.major_label_orientation = 1
bar_chart.yaxis.axis_label = "Count"
st.bokeh_chart(bar_chart)

# You can continue adding more charts and interactivity based on your dataset

# Finally, run the Streamlit app
if __name__ == '__main__':
    st.title('Hospital Admission Dashboard')
