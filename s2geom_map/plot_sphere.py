import plotly.graph_objects as go

if __name__ == '__main__':

    fig = go.Figure(data=go.Scattergeo(
        lat = [60.7127, 71.5072],
        lon = [-30.0059, -10.1275],
        mode = 'lines',
        line = dict(width = 2, color = 'blue'),
    ))

    fig.update_layout(
        title_text = 'London to NYC Great Circle',
        showlegend = False,
        geo = dict(
            resolution = 50,
            showland = True,
            showlakes = True,
            landcolor = 'rgb(204, 204, 204)',
            countrycolor = 'rgb(204, 204, 204)',
            lakecolor = 'rgb(255, 255, 255)',
            projection_type = "equirectangular",
            coastlinewidth = 2,
            lataxis = dict(
                range = [20, 60],
                showgrid = True,
                dtick = 10
            ),
            lonaxis = dict(
                range = [-100, 20],
                showgrid = True,
                dtick = 20
            ),
        )
    )

    fig.show()