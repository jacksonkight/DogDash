import pandas as pd
import dash
import plotly.express as px
from dash import Dash, html, Input, Output, State, dcc, ctx
import dash_bootstrap_components as dbc
from PIL import Image
import pathlib

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], use_pages=True, pages_folder="")
app.title = 'Dog Breed Dash'
server = app.server

main_dir = pathlib.Path(__file__).parent
data = main_dir / 'dog_breeds.csv'
dogs_data = pd.read_csv(data)
 
dogs_data

#drop if missing value for location
dogs_data.dropna(subset='Name', inplace=True)

#set location as the index
dogs_data.set_index('Name', inplace=True)

assert dogs_data.index.is_unique
assert not dogs_data.index.hasnans

attribute_list = [ c for c in dogs_data.columns]
attribute_list.sort()
attribute_list

dogs_data = dogs_data.T 
dogs_data

dogs_data.index.name = 'Name'

dogs_data2 = dogs_data.filter(items=['drooling', 'barking'], axis=0)
dogs_data2
breed_list = [ c for c in dogs_data.columns]
breed_list.sort()
breed_list


#layout for page 1
layout_1 = html.Div(
children=[
        #Title
        html.H1('Interactive Dog Breed Visualization', className='text-center mt-3'),
        #Chart
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H2('Characteristics by Breed', className='text-center mt-5'),
                        dcc.Graph(
                            id='dog_chart',
                            className='m-5',
                            config=dict(displayModeBar=False),
                            style={'width': '80vh', 'height': '30vh'},
                            figure={
                                'layout': {
                                    'xaxis': {'title': 'Characteristics'},
                                    'yaxis': {'title': 'Value'}
                                }
                            }                            
                        ),
                    ],
                ),
                dbc.Col(
                    children=[
                        html.H2('Weight and Height by Breed', className='text-center mt-5'),
                        dcc.Graph(
                            id='dog_chart2',
                            className='m-5',
                            config=dict(displayModeBar=False),
                            style={'width': '80vh', 'height': '30vh'},
                            figure={
                                'layout': {
                                    'xaxis': {'title': 'Weight'},
                                    'yaxis': {'title': 'Height'}
                                }
                            }                               
                        ),
                    ],
                ),
            ],
        ),
        #dropdown and paragraph
        dbc.Row(
            dbc.Col(
                width=dict(size=8, offset=2),
                children=[
                    html.H6('This dashboard can be used to help the user find a dog breed that fits their ideal metrics. The left graph shows selected dog breeds and selected characteristics. The right graph shows selected breeds and their weight and height.'),
                    html.H4('Breed Selection:', className='mt-5'),
                    dcc.Dropdown(
                        options=[
                            dict(label=c, value=c) for c in breed_list
                        ],
                        placeholder='select dog breed(s)',
                        multi=True, #allows multiple selections
                        id='breed_dropdown',
                        value=[],
                        optionHeight=20,
                        className='mb-5',
                    ),
                    html.H4('Characteristic Selection:', className='mt-5'),
                     dcc.Dropdown(
                        options=[
                            dict(label=c, value=c) for c in attribute_list
                        ],
                        placeholder='select dog attribute(s)',
                        multi=True, #allows multiple selections
                        id='attribute_dropdown',
                        value=[],
                        optionHeight=20,
                        className='mb-5',
                    ),
                    html.H4('Weight Selection:', className='mt-5'),
                    dcc.Slider(
                                min=6,
                                max=200,
                                step=10,
                                value=200,
                                id='SliderWeight'
                    ), 
                    dcc.Store(
                        id='last_slider_weight'
                    ),
                    html.H4('Gender Selection:', className='mt-5'),
                    dbc.RadioItems(
                    options=[
                        dict(label="Male", value=1),
                        dict(label="Female", value=2),
                    ],
                    value=1,
                    id='RadioGender',
                    ),
                    html.Br(),
                    html.Br(),
                    html.Div(
                        children=[
                            'Data source: ',
                            html.A(
                                'https://www.kaggle.com/datasets/warcoder/dog-breeds-details?resource=download',
                                href='https://www.kaggle.com/datasets/warcoder/dog-breeds-details?resource=download'
                            )
                        ]
                    )

                ],
            ),
        )
    ],
)


#layout for page 2
layout_2 = html.Div(
    children=[
        html.H1("AI's Take on Dog Breeds", className='mx-5'),
        html.P("Dog breeds are fascinating creatures. With their adorable puppy eyes, wagging tails, and boundless energy, they've been a beloved companion for centuries. But let's be real here, the world of dog breeds is a weird one. From the wrinkly, slobbery faces of the bulldog to the hairless Chihuahua, there's a dog breed out there for everyone.", className='mt-3 mx-5'),
        html.P("Take the Pekingese for instance. This breed is known for its long, flowing coat, which is so luscious that it would put a Victoria's Secret model to shame. It's no surprise that the Pekingese is often featured in dog shows and on the red carpet. After all, who doesn't love a good fur coat? But let's not forget the maintenance involved in keeping that luscious fur in tip-top shape. The Pekingese requires regular grooming, including daily brushing and frequent baths. So if you're considering adopting a Pekingese, be prepared to invest in some good grooming supplies and a lot of elbow grease.", className='mt-3 mx-5'),
        html.P("On the opposite end of the spectrum, we have the Xoloitzcuintli, or the Mexican Hairless. This breed is unique in that it's, well, hairless. That's right, no luscious fur coats for these pups. Instead, they have smooth, sleek skin that gives them a somewhat alien appearance. But hey, at least they're low-maintenance, right? No grooming required for these guys. Although, you might want to invest in some sunscreen for them during the summer months. We wouldn't want them to get sunburnt now, would we?", className='mt-3 mx-5'),
        html.P("Then there's the Bulldog, with its slobbery jowls and wrinkly face. These pups are the epitome of adorably goofy. But let's face it, they're not exactly the most agile of breeds. You're not going to see a Bulldog winning any agility contests any time soon. But what they lack in agility, they make up for in personality. Bulldogs are known for their affectionate and loyal nature, making them the perfect companion for couch potato pet parents.", className='mt-3 mx-5'),
        html.P("And let's not forget about the Chihuahua, the pocket-sized pup with a big attitude. These tiny dogs may be small in size, but they've got big personalities. They're known for their feisty nature and tendency to bark at anything and everything. But hey, at least they're easy to carry around, right? Just pop them in your purse and you're good to go.", className='mt-3 mx-5'),     
        html.P("All joking aside, dog breeds are a fascinating and diverse group of animals. From the regal Great Dane to the tiny Pomeranian, each breed has its own unique quirks and personality traits that make them special. So whether you're a fan of the furrier breeds or the hairless ones, there's a dog out there for everyone. Just remember, owning a dog is a big responsibility, so make sure you're prepared for the commitment before bringing one into your life.", className='mt-3 mx-5'),
        html.P("- ChatGPT", className='mt-3 mx-5'),  
    ]
)



#register pages
dash.register_page(
    'overview', 
    path='/',
    layout=layout_1
    )

dash.register_page(
    'insight', 
    path='/second-page',
    layout=layout_2
    )

app.layout = dbc.Container(
    children=[
        #page navigation    
        dbc.NavbarSimple(
            brand='Dog Breed Dash',
            children=[
                dbc.NavItem( dbc.NavLink('Dash', href='/')),
                dbc.NavItem( dbc.NavLink('Insights', href='/second-page')),
            ],
            color = 'primary',
            dark = True,
        ),
        # page content
        dash.page_container,
    ],
    fluid=True,
    class_name='px-0',
)

@app.callback(
    Output('dog_chart', 'figure'),
    Output('dog_chart2', 'figure'),
    Output('breed_dropdown', 'options'),
    Output('last_slider_weight', 'data'),
    Output('breed_dropdown', 'value'),
    Input('breed_dropdown', 'value'),
    Input('attribute_dropdown', 'value'),
    Input('SliderWeight', 'value'),
    Input('RadioGender', 'value'),
    Input('last_slider_weight', 'data')
)

def update_chart(breeds_selected, attribute_selected, weight_selected, gender_selected,last_selected_weight):
    try:
        
        dogs_data = pd.read_csv('C:/Users/jacks/downloads/dog_breeds.csv')

        dogs_data

        #drop if missing value for location
        dogs_data.dropna(subset='Name', inplace=True)

        #set location as the index
        dogs_data.set_index('Name', inplace=True)

        assert dogs_data.index.is_unique
        assert not dogs_data.index.hasnans

        '''
        attribute_selected = []
        breeds_selected = []
        last_selected_weight = 200
        gender_selected = 1
        weight_selected = 200
        '''
        if gender_selected == 1:
            col_i_want = 'max_weight_male'
        elif gender_selected == 2:
            col_i_want = 'max_weight_female'

        weight_filter = (dogs_data[col_i_want] <= weight_selected)

        weight_filtered_data = dogs_data[weight_filter]
        #weight_filtered_data
        attribute_list = [ c for c in weight_filtered_data.columns]
        attribute_list.sort()
        attribute_list

        dogs_data = weight_filtered_data.T 
        #dogs_data
        dogs_data.index.name = 'Name'

        if weight_selected != last_selected_weight:
            breeds_selected = []

        breed_list = [ c for c in dogs_data.columns]
        breed_list.sort()
        breed_list
        breed_options= [dict(label=c, value=c) for c in breed_list]

        if len(breeds_selected) == 0:
            breeds_selected = ['Maltese']

        if len(attribute_selected) == 0:
            attribute_selected = ['barking']

        dogs_data_subset = dogs_data[breeds_selected].copy()
        dogs_data_subset.dropna(inplace=True, how='all')
        dogs_data2 = dogs_data.filter(items=attribute_selected, axis=0)

        #tkinter.messagebox.showerror(last_selected_weight,weight_selected)
        dog_fig = px.bar(
            dogs_data2,
            x=dogs_data2.index,
            y=breeds_selected,
            barmode= 'group'
        )

        dog_fig.update_xaxes(
            title_text=' ',
            tickfont=dict(size=16)
        )
        dog_fig.update_yaxes(
            title_text=' ',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            tickfont=dict(size=16),
            tickprefix=''
        )

        dog_fig.update_layout(
            legend_title_text = '',
            legend_font_size=16,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=0,b=0)
        )

        dogs_data3 = dogs_data_subset.T

        if gender_selected == 1:
            dog_fig2 = px.scatter(
                dogs_data3,
                x='max_weight_male',
                y='max_height_male',
                color = dogs_data3.index
            )
        else:
             dog_fig2 = px.scatter(
                dogs_data3,
                x='max_weight_female',
                y='max_height_female',
                color = dogs_data3.index
            )
             
        dog_fig2.update_xaxes(
            title_text=' ',
            tickfont=dict(size=16)
        )
        dog_fig2.update_yaxes(
            title_text=' ',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            tickfont=dict(size=16),
            tickprefix=''
        )

        dog_fig2.update_layout(
            legend_title_text = '',
            legend_font_size=16,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=0,b=0)
        )
        
        return dog_fig, dog_fig2, breed_options, weight_selected, breeds_selected
    except:
        dummy = 1

    return 



if __name__ == '__main__':
    app.run_server(debug=True)



