import dash
#from scout_apm.flask import ScoutApm
from dash import html, dcc, dash_table, Input, Output

port = 9051
app = dash.Dash(__name__, suppress_callback_exceptions = True, 
    title = 'Plotly Holiday Challenge Churn', 
    #update_title=None, 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    
)

@app.callback(
        Output('saved', 'children'),
        Input('save', 'n_clicks'),
    )
def save_result(n_clicks):
    if n_clicks == 0:
        return 'not saved'
    else:
        make_static(f'http://127.0.0.1:{port}/')
        return 'saved'


app.run_server(debug=False, port=port)
# flask_app = app.server

# # Setup a flask 'app' as normal

# # Attach ScoutApm to the Flask App

# ScoutApm(flask_app)
# flask_app.config["SCOUT_NAME"] = "first app"

#new comment
