import pandas as pd
import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import base64




data = pd.read_csv("preprocessed_best_selling_games.csv")
nintendoEAD = data[data["Developer(s)"] == "Nintendo EAD"]

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    "custom.css"  # Path to your custom CSS file
]


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)


# Group the data by Publisher(s) and sum the Sales for each Developer(s)
grouped_data = data.groupby("Publisher(s)")["Sales"].sum().reset_index()

# Sort the data in descending order based on Sales
grouped_data = grouped_data.sort_values("Sales", ascending=False)
filtered_data = data[data["Publisher(s)"] == "Nintendo"]

# Get the sales by platform
platform_sales = data.groupby("Platform(s)")["Sales"].sum().reset_index()


# Define the app layout
app.layout = html.Div(    
    id="main-container",
    style={"backgroundColor": "light grey"}, 
    children=[
        html.Div(
            className="header",
            style={
                  "background-color": "black",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "height": "30px",
            },
            children=[
                html.P(children="aa",style={"color": "black"}),
            ],
        ),

        html.Div(
            className="header",
            style={
                "background-color": "black",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "height": "100px",
            },
            children=[
                html.Img(src="https://mms.businesswire.com/media/20210202005629/en/856294/5/4874400_EA_SPORTS_logo.jpg", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://img.freepik.com/free-icon/playstation-logo_318-10089.jpg", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="data:image/png;base64,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", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://cdn-icons-png.flaticon.com/512/871/871377.png", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Rockstar_Games_Logo.svg/800px-Rockstar_Games_Logo.svg.png", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/800px-Steam_icon_logo.svg.png", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://www.pngmart.com/files/22/Garena-Free-Fire-Logo-PNG.png", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://cdn-icons-png.flaticon.com/512/871/871362.png", className="header-image", style={"width": "60px", "height": "60px"}),
                html.P(children="aa",style={"color": "black"}),
                html.Img(src="https://img.konami.com/kde_cms/na_publish/uploads/konami-logo.png", className="header-image", style={"width": "60px", "height": "60px"}),
                
            ],
        ),
        
        html.Div(
            className="header",
            style={
                "background-color": "black",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "height": "50px",
            },
            children=[
                html.P(
                    children="",
                    className="header-emoji",
                    style={"color": "white", "font-family": "Comic Sans MS, cursive", "font-weight": "bold"}
                ),
                html.H1(
                    children="Best Selling Video Games",
                    className="header-title",
                    style={"color": "white", "font-family": "Comic Sans MS, cursive", "font-weight": "bold"}
                ),
            ],
        ),
        html.Div(
            className="header",
            style={
                "background-color": "black",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "height": "10px",
            },
            children=[
                html.P(
                    children=[
                        
                    ],
                    className="header-description",
                    style={"white-space": "pre-line", "color": "white"},  # Set font color to white
                ),
            ],
        ),

    
    dcc.Tabs(
    id='tabs',
    value='tab-1',
    children=[
        dcc.Tab(
            label='Total Sales by Publisher',
            value='tab-1',
            children=[
                dcc.Graph(
                    id='total_sales_bar_chart',
                    figure={
                        "data": [
                            {
                                "x": grouped_data["Publisher(s)"],
                                "y": grouped_data["Sales"],
                                "type": "bar",
                            }
                        ],
                        "layout": {"title": "Total Sales by Publisher"},
                    },
                ),
            ],
        ),
        dcc.Tab(
            label='Sales by Developer',
            value='tab-2',
            children=[
                dcc.Dropdown(
                    id='developer_publisher_dropdown',
                    options=[{'label': publisher, 'value': publisher} for publisher in data["Publisher(s)"].unique()],
                    value=data["Publisher(s)"].unique()[0],
                ),
                html.Div(
                    children=[
                        dcc.Graph(id='sales_bar_chart'),
                        html.Div(id='developer_table_div')
                    ],
                    style={'display': 'flex', 'flex-direction': 'column'}
                )
            ]
        ),
        dcc.Tab(
            label='Sales by Platform for each Publisher',
            value='tab-3',
            children=[
                dcc.Dropdown(
                    id='platform_publisher_dropdown',
                    options=[{'label': publisher, 'value': publisher} for publisher in data["Publisher(s)"].unique()],
                    value=data["Publisher(s)"].unique()[0],
                ),
                dcc.Graph(id='platform_pie_chart'),
                html.Div(id='platform_table_div', style={'margin': 'auto', 'width': '50%'})
            ]
        ),
    ],
    style={'backgroundColor': 'light grey'}  # Set the background color to light gray
)
])

# Define the callback to update the bar chart for Sales by Developer
@app.callback(
    Output('sales_bar_chart', 'figure'),
    Input('developer_publisher_dropdown', 'value')
)
def update_sales_bar_chart(selected_publisher):
    filtered_data = data[data["Publisher(s)"] == selected_publisher]
    fig = px.bar(
        filtered_data,
        x="Developer(s)",
        y="Sales",
        color="Series",
        barmode="group",
        title=f"Sales by Developer for Publisher: {selected_publisher}",
    )
    return fig

@app.callback(
    Output('platform_pie_chart', 'figure'),
    Input('platform_publisher_dropdown', 'value')
)
def update_platform_pie_chart(selected_publisher):
    filtered_data = data[data["Publisher(s)"] == selected_publisher]
    platform_counts = filtered_data["Platform(s)"].value_counts()

    fig = go.Figure(data=[go.Pie(labels=platform_counts.index, values=platform_counts.values)])

    fig.update_layout(title=f"Platform Distribution for Publisher: {selected_publisher}")

    return fig

@app.callback(
    Output('developer_table_div', 'children'),
    Input('developer_publisher_dropdown', 'value')
)
def update_developer_table(selected_publisher):
    filtered_data = data[data["Publisher(s)"] == selected_publisher]
    developer_sales = filtered_data.groupby("Developer(s)")["Sales"].sum().reset_index()
    sorted_developer_sales = developer_sales.sort_values("Sales", ascending=False)

    table = html.Table(
        # Table Header
        [html.Tr([html.Th("Developer"), html.Th("Total Sales")])] +
        # Table Rows
        [html.Tr([html.Td(row["Developer(s)"]), html.Td(row["Sales"])]) for _, row in sorted_developer_sales.iterrows()],
        # Add CSS styling to center align the table and increase size
        style={'margin': 'auto', 'width': '50%', 'font-size': '16px'}
    )

    return table

@app.callback(
    Output('platform_table_div', 'children'),
    Input('platform_publisher_dropdown', 'value')
)
def update_platform_table(selected_publisher):
    filtered_data = data[data["Publisher(s)"] == selected_publisher]
    platform_sales = filtered_data.groupby("Platform(s)")["Sales"].sum().reset_index()
    sorted_platform_sales = platform_sales.sort_values("Sales", ascending=False)

    table = html.Table(
        # Table Header
        [html.Tr([html.Th("Platform"), html.Th("Total Sales")])] +
        # Table Rows
        [html.Tr([html.Td(row["Platform(s)"]), html.Td(row["Sales"])]) for _, row in sorted_platform_sales.iterrows()],
        # Add CSS styling to center align the table and increase size
        style={'margin': 'auto', 'width': '50%', 'font-size': '16px'}
    )

    return table

app.css.append_css({
    "external_url": "custom.css"  # Path to your custom CSS file
})
app.css.config.serve_locally = False

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
