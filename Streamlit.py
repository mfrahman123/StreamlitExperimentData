# import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Function to load data and transform it into a more plottable format
def load_data():
    # Load the data from csv
    data = pd.read_csv('unemployment_data.csv')
    
    # Convert data from wide to long format so that each year is a row rather than a column
    data = data.melt(id_vars=["Country Name", "Country Code"], var_name="Year", value_name="Unemployment Rate")
    
    # convert 'Year' column data to numeric format
    data['Year'] = pd.to_numeric(data['Year'])
    
    return data

# Function to plot the unemployment rates for select countries over the years
def plot_mult_countries(data, countries):
    # Initialize an empty Plotly Figure
    fig = go.Figure()
    
    # For each selected country, add a line plot of the unemployment rate over the years
    for country in countries:
        country_data = data[data['Country Name'] == country]
        fig.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Unemployment Rate'], mode='lines', name=country))
    
    return fig

def main():
    # Load data
    data = load_data()
    
    # Set the title for the Streamlit App
    st.title("Unemployment & Job Market Trend Dashboard")

    # Multiselect box for choosing countries
    selected = st.multiselect('Select countries', options=data['Country Name'].unique())
    
    # If at least one country is selected, plot the corresponding line plots
    if len(selected) > 0:
        fig = plot_mult_countries(data, selected)
        st.plotly_chart(fig)
    
        # For comparison of single years between countries
        selected_year = st.slider("Select Year for comparison", int(data['Year'].min()), int(data['Year'].max()), step=1)
        year_data = data[data['Year']==selected_year]
        year_data_selected = year_data[year_data['Country Name'].isin(selected)]
        fig2 = go.Figure(data=[go.Bar(x=year_data_selected['Country Name'], y=year_data_selected['Unemployment Rate'])])
        fig2.update_layout(title_text='Unemployment Rate Comparison for Year {}'.format(selected_year))
        st.plotly_chart(fig2)
        
    else:
        # Prompt user to select at least one country if no country is selected
        st.write("No countries selected")

if __name__ == '__main__':
    main()