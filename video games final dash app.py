import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Load the dataset
df = pd.read_csv('video_games_new.csv')
background_image_url = '/assets/images.jpg'


# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
years = df['Year'].unique()

## main layout 
app.layout = html.Div([
    html.H1("Analysis of Video Game sales from 2000 to 2015", style={'color': 'white','textAlign': 'center'}),
    dcc.Tabs(children=[             ### Re1 - Abzal
        dcc.Tab(label='Line Chart for video games by year',
                children=[
                    html.H2('Line Chart', style={'color': 'white'}),
                    dcc.Dropdown(df.columns[5:8], id='tab1_dropdown', value='NA_Sales'),
                    dcc.Slider(
                        id='year-slider',
                        min=min(years),
                        max=max(years),
                        step=1,
                        value=min(years),
                        marks={str(year): str(year) for year in years}
                    ),
                    dcc.Graph(id='line-chart'),
        html.Footer(
        'Created by: Abzal-COHNDDS232F-007', style={'color': 'white'}
    )            
                ]),
        dcc.Tab(label='Scatter Plot for video games', children=[   ### req 2 - Sithumi 
            html.H2('Scatter Plot', style={'color': 'white'}),
            dcc.RadioItems(
                id='scatter-plot-radio',
                options=[{'label': col, 'value': col} for col in [
                    'Critic_Count', 'User_Score',
                    'Global_Sales']],
                value='Critic_Count'
            ),
            dcc.Graph(id='scatter-plot'),
        html.Footer(
        'Created by: Sithumi-COHNDDS232F-010', style={'color': 'white'}
    )    
        ]),
        dcc.Tab(label='Interactive Charts for video games', children=[     ### req 3 - Abzal
            html.H2('Interactive Charts', style={'color': 'white'}),
            html.Div([
                dcc.Graph(
                    id='chart1',
                    figure=px.bar(df, x='Genre', y='Critic_Score'),
                     style={'display': 'inline-block', 'width': '50%'}
                ),
                dcc.Graph(
                    id='chart2',
                    figure=px.scatter(df, x='User_Score', y='Critic_Score'),
                     style={'display': 'inline-block', 'width': '50%'}
                ),
        html.Footer(
        'Created by: Abzal-COHNDDS232F-007', style={'color': 'white'}
    )        
            ])
        ]),
        dcc.Tab(label='Custom Graph for video games', children=[          ### req 4 - Sithumi
            html.H2('Pie Chart', style={'color': 'white'}),  
            dcc.Graph(
                id='pie-chart',
                figure=px.pie(df, names='Genre',
                              title='Genre Distribution for 2000-2015')
            ),
            dcc.Graph(
                id='bar-graph',
                figure=px.bar(df, x='Genre', y='Critic_Score',
                              title='Critic Score by Genre')
            ),
    html.Footer(
        'Created by: Sithumi-COHNDDS232F-010', style={'color': 'white'}
    )        

        ])
    ]),
    
], style={'background-image': f'url({background_image_url})',
                             'background-size': 'cover',
                             'background-position': 'center',
                             'height': '100vh','maxWidth': '1200px', 'margin': 'auto', 'height': '100vh', 'overflowY': 'scroll'})



# Callback for line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input(component_id='tab1_dropdown', component_property='value'),
     Input('year-slider', 'value')]
)
def update_graph(dropdown_value, selected_year):
    # Filter the DataFrame based on the selected year
    filtered_df = df[df['Year'] <= selected_year]
    
    # Group the filtered DataFrame by platform and sum up global sales
    platform_sales = filtered_df.groupby('Year')[['NA_Sales','EU_Sales','JP_Sales']].sum().reset_index()

    # Define the figure for the line chart
    fig = {
        'data': [
            {
                'x': platform_sales['Year'],
                'y': platform_sales[dropdown_value],
                'type': 'line',
                'name': 'Global Sales'
            }
        ],
        'layout': {
            'title': f'Video Game Sales by Platform for {selected_year}',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Global Sales'}
        }
    }
    
    return fig



# Callback scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatter-plot-radio', 'value'))
def update_scatter_plot(selected_var):
    # correlation
    correlation = df[['Critic_Score', selected_var]].corr().iloc[0, 1]

    # Update the scatter plot
    fig = px.scatter(df, x='Critic_Score', y=selected_var,
                     title=f'Correlation is {correlation:.2f} in relation to Critic Score')
    return fig


# Callback to update the scatter plot based on the selected bar in the bar
@app.callback(
    Output('chart2', 'figure'),
    Input('chart1', 'clickData'))

def update_scatter_plot_with_click(click_data):

    if click_data is None:
        # If no data is clicked, show the original scatter plot
        fig = px.scatter(df, x='Genre', y='Critic_Score',
                         title='Critic Score and Game Genre',
                         labels={'Genre': 'Genre',
                                 'Critic_Score': 'Critic Score'})
    else:
        # Retrieve the selected category from the clicked data
        selected_category = click_data['points'][0]['x']

        # Filter the dataset based on the selected category
        filtered_df = df[df['Genre'] == selected_category]

        filtered_df = filtered_df.groupby('Year').agg({'Critic_Score':'mean'}).reset_index()

        # Create the updated scatter plot
        fig = go.Figure()
        # Create and style traces
        fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Critic_Score'],
                                 name='Critic_Score',
                                line=dict(color='firebrick', width=4,dash='dashdot'))) 

        fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Global_Sales'],
                                 name='Global_Sales',
                                line=dict(color='blue', width=4,dash='dashdot')))

    return fig


## updating the Custom Pie Chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('bar-graph', 'clickData')]
)
def update_pie_chart(click_data):
    if click_data is None:
        fig = px.pie(df, names='Genre', title='Genre Distribution')
    else:
        selected_genre = click_data['points'][0]['x']
        filtered_df = df[df['Genre'] == selected_genre]
        fig = px.pie(filtered_df, names='Rating', title=f'Rating Distribution for {selected_genre}')
    return fig

# updating the stacked bar graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('pie-chart', 'clickData')]
)
def update_bar_graph(click_data):
    if click_data is None:
        grouped_df = df.groupby(['Genre', 'Rating']).size().reset_index(name='Count')
        fig = px.bar(grouped_df, x='Genre', y='Count', color='Rating',
                     title='Stacked Bar Chart by Genre and Rating', barmode='stack')
    else:
        selected_genre = click_data['points'][0]['label']
        filtered_df = df[df['Genre'] == selected_genre]
        grouped_df = filtered_df.groupby(['Genre', 'Rating']).size().reset_index(name='Count')
        fig = px.bar(grouped_df, x='Genre', y='Count', color='Rating',
                     title=f'Stacked Bar Chart by Genre and Ratings for {selected_genre}', barmode='stack')
    return fig


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True,port=8273)
