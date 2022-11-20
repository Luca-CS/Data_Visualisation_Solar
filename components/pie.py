import plotly.graph_objects as go
import dash_core_components as dcc

def pie(X,Y, title):
    fig = go.Figure(data=[go.Pie(labels=X, values=Y)])
    fig_layout = fig["layout"]
    fig_layout["title"] = "<b>{0}</b>".format(title)
    fig_layout["legend"] = dict(orientation="v")
    fig_layout["autosize"] = True
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#2cfec1"
    return dcc.Graph(id="graph", figure=fig)