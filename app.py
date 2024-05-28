import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go



def create_dataframe(
    bangladesh_divisions:dict,
    rain_and_temperature_data:pd.DataFrame
):

    years=[year for year in rain_and_temperature_data['Year']]
    months=[month for month in rain_and_temperature_data['Month']]
    id_names=[]
    division_names=[]
    for row in bangladesh_divisions['features']:
        for _ in range(0,len(years)): 
            id_names.append(row['id'])
            division_names.append(row['properties']['ADM1_EN'])
            
    years=years*(len(id_names)//len(years))
    months=months*(len(id_names)//len(months))

    temperature_data=rain_and_temperature_data['tem'].to_list()
    temperature_data=[int(t) for t in temperature_data]
    temperature_data=temperature_data*(len(id_names)//len(temperature_data))

    data = {
        'id_name': id_names,  
        'division_name':division_names,   
        'years':years,
        'month':months,
        'temp':temperature_data[:]
    }
    return data

if __name__=='__main__':
    bangladesh_divisions=None
    with open('dataset/bangladesh-division-geojson.json','r',encoding='UTF-8') as boundaries:
        bangladesh_divisions=json.load(boundaries)
    

    rain_and_temperature_data=pd.read_csv('dataset/sorted_temp_and_rain_dataset.csv')
    data=create_dataframe(bangladesh_divisions,rain_and_temperature_data)
    divisions = pd.DataFrame(data)
    divisions.to_csv('division_with_temp.csv')
    
 
    fig = px.choropleth(
        divisions,
        geojson=bangladesh_divisions,
        color='temp',
        locations='division_name',  
        scope='asia',
        hover_name="division_name",
        featureidkey="properties.ADM1_EN",
        labels='division_name',
        animation_frame="years",
        color_continuous_scale = "Viridis"
    )
    

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    fig.show()
    