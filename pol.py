import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Police Incident Reports from 2018 to 2020 in San Francisco")
df = pd.read_csv("Police.csv")
st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police districts, neighborhood in which it happened, type of incident in category and subcategory, exact location, and resolution.")

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist()
)
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist()
)
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist()
)

if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data0 = subset_data
Resolution_input = st.sidebar.multiselect(
    'Resolution',
    mapa.groupby('Resolution').count().reset_index()['Resolution'].tolist()
)
if len(Resolution_input) > 0:
    subset_data0 = subset_data[subset_data['Incident Year'].isin(Resolution_input)]



st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district')
st.markdown('Crime locations in San Francisco')
st.map(subset_data)

st.markdown('Crimes occurred per day of the week')
day_counts = subset_data['Day'].value_counts().reset_index()
day_counts.columns = ['Day', 'Number of Incidents']
fig = px.bar(day_counts, x='Day', y='Number of Incidents', labels={'Day': 'Day of the week', 'Number of Incidents': 'Number of Incidents'}, color='Day')
st.plotly_chart(fig, use_container_width=True)

st.markdown('Crime occurred per date')
date_counts = subset_data['Date'].value_counts().reset_index()
date_counts.columns = ['Date', 'Number of Incidents']
fig = px.line(date_counts.sort_values('Date'), x='Date', y='Number of Incidents', color='Date')
fig.update_traces(mode='lines+markers')
fig.update_xaxes(title='Date')
fig.update_yaxes(title='Number of Incidents')
st.plotly_chart(fig, use_container_width=True)

st.markdown('Type of crimes committed')
incident_category_counts = subset_data['Incident Category'].value_counts().reset_index()
incident_category_counts.columns = ['Incident Category', 'Number of Incidents']
fig = px.bar(incident_category_counts, x='Incident Category', y='Number of Incidents', labels={'Incident Category': 'Incident Category', 'Number of Incidents': 'Number of Incidents'}, color='Incident Category')
st.plotly_chart(fig, use_container_width=True)

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    incident_subcategory_counts = subset_data['Incident Subcategory'].value_counts().reset_index()
    incident_subcategory_counts.columns = ['Incident Subcategory', 'Number of Incidents']
    fig = px.bar(incident_subcategory_counts, x='Incident Subcategory', y='Number of Incidents', labels={'Incident Subcategory': 'Incident Subcategory', 'Number of Incidents': 'Number of Incidents'}, color='Incident Subcategory')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('Resolution status')
resolution_counts = subset_data['Resolution'].value_counts().reset_index()
resolution_counts.columns = ['Resolution', 'Number of Incidents']
fig = px.pie(resolution_counts, values='Number of Incidents', names='Resolution', title='Resolution')
st.plotly_chart(fig, use_container_width=True)

# Nuevas visualizaciones agregadas
st.markdown('Years with the highest number of incidents')
incident_years = pd.to_datetime(subset_data['Date']).dt.year.value_counts().sort_index().reset_index()
incident_years.columns = ['Year', 'Number of Incidents']
fig = px.bar(incident_years, x='Year', y='Number of Incidents', labels={'Year': 'Year', 'Number of Incidents': 'Number of Incidents'}, color='Year')
st.plotly_chart(fig, use_container_width=True)

st.markdown('Number of incidents by "Incident Subcategory"')
subcategory_counts = subset_data['Incident Subcategory'].value_counts().reset_index()
subcategory_counts.columns = ['Incident Subcategory', 'Number of Incidents']
fig = px.bar(subcategory_counts, x='Incident Subcategory', y='Number of Incidents', labels={'Incident Subcategory': 'Incident Subcategory', 'Number of Incidents': 'Number of Incidents'}, color='Incident Subcategory')
st.plotly_chart(fig, use_container_width=True)

st.markdown('Resolution Types')
resolution_types = subset_data['Resolution'].value_counts().reset_index()
resolution_types.columns = ['Resolution', 'Number of Incidents']
fig = px.bar(resolution_types, x='Resolution', y='Number of Incidents', labels={'Resolution': 'Resolution', 'Number of Incidents': 'Number of Incidents'}, color='Resolution')
st.plotly_chart(fig, use_container_width=True)

st.markdown('Number of incidents by "Police District"')
police_district_counts = subset_data['Police District'].value_counts().reset_index()
police_district_counts.columns = ['Police District', 'Number of Incidents']
fig = px.bar(police_district_counts, x='Police District', y='Number of Incidents', labels={'Police District': 'Police District', 'Number of Incidents': 'Number of Incidents'}, color='Police District')
st.plotly_chart(fig, use_container_width=True)

# Sección para el mapa interactivo y detalles de delitos
st.header("Interactive Crime Incident Map and Reporting")

# Mapa interactivo con detalles sobre los delitos
st.subheader("Crime Incident Map")
st.map(mapa)

# Detalles adicionales sobre los delitos
st.subheader("Crime Incident Details")
selected_category = st.selectbox("Select Incident Category", mapa['Incident Category'].unique())
filtered_data = mapa[mapa['Incident Category'] == selected_category]
st.write(filtered_data)

# Sección para el reporte de incidentes
st.subheader("Report an Incident")
incident_category = st.selectbox("Incident Category", mapa['Incident Category'].unique())
incident_subcategory = st.selectbox("Incident Subcategory", mapa['Incident Subcategory'].unique())
location = st.text_input("Location (Intersection or coordinates)")

if st.button("Report"):
    # Aquí puedes agregar la lógica para guardar el reporte del incidente
    st.success("Incident reported successfully!")