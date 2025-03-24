import os
import dash
from dash import html, dcc
import plotly.graph_objs as go

import numpy as np
from dash.dependencies import Input, Output

def create_dash_app(players, df, df_sorted, match_history, include_plot=False, Monthly_rating=None):
    # Initialize the Dash app
    port = 8059
    service_prefix = os.getenv("JUPYTERHUB_SERVICE_PREFIX", "/")
    domain = os.getenv("JUPYTERHUB_HTTP_REFERER", None)
    app = dash.Dash(
        __name__,
        requests_pathname_prefix=f"{service_prefix}proxy/{port}/"
    )

    # Define the layout of the app
    app.layout = html.Div([
        html.H1("Player Ratings"),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Player"),
                    html.Th("Rating"),
                    html.Th("Games Played")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(player),
                    html.Td(df_sorted.loc[player, 'rating']),
                    html.Td(df_sorted.loc[player, 'games_played'])
                ]) for player in df_sorted.index
            ])
        ]),

        html.H2("Player Win Rates Against Others"),
        dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': player, 'value': player} for player in df.index],
            value=df.index[0]  # Set the initial value to the first player in the list
        ),
        html.Table(id='win-rate-table')
    ])

    if include_plot and Monthly_rating:
        # Create the plot
        player_names = [player["player"] for player in Monthly_rating]
        player_ratings = [player["ratings"] for player in Monthly_rating]

        fig = go.Figure()
        for i in range(len(Monthly_rating)):
            fig.add_trace(go.Scatter(x=np.arange(1, len(player_ratings[i]) + 1), y=player_ratings[i], mode='lines+markers', name=player_names[i]))

        # Add layout
        fig.update_layout(
            title="Player Progression",
            xaxis_title="Periode",
            yaxis_title="Rating"
        )

        app.layout = html.Div([
            html.H1("Player Ratings"),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Player"),
                        html.Th("Rating"),
                        html.Th("Games Played")
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(player),
                        html.Td(df_sorted.loc[player, 'rating']),
                        html.Td(df_sorted.loc[player, 'games_played'])
                    ]) for player in df_sorted.index
                ])
            ]),

            html.H2("Player Win Rates Against Others"),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': player, 'value': player} for player in df.index],
                value=df.index[0]  # Set the initial value to the first player in the list
            ),
            html.Table(id='win-rate-table'),

            html.H2("Player Progression"),
            dcc.Graph(
                id='player-progression-graph',
                figure=fig, 
                 style={'height': '6000px'}  # Adjust the height as needed
            ),
            dcc.Checklist(
                id='show-plot',
                options=[
                    {'label': 'Show Plot', 'value': 'show'}
                ],
                value=[]
            )
        ])

    @app.callback(
        Output('win-rate-table', 'children'),
        [Input('player-dropdown', 'value')]
    )
    def update_win_rate_table(selected_player):
        rows = []
        for player in df.index:
            if player != selected_player:
                wins = 0
                total_games = 0
                for match in match_history:
                    if match['winner'] == player and match['loser'] == selected_player:
                        wins += 1
                        total_games += 1
                    elif match['loser'] == player and match['winner'] == selected_player:
                        total_games += 1
                win_rate = round((wins / total_games) * 100) if total_games > 0 else 0
                rows.append(html.Tr([html.Td(player), html.Td(f"{win_rate}%")]))
        return [
            html.Thead(
                html.Tr([html.Th("Opponent"), html.Th("Win Rate Against Selected Player")])
            ),
            html.Tbody(rows)
        ]

    @app.callback(
        Output('player-progression-graph', 'style'),
        [Input('show-plot', 'value')]
    )
    def toggle_plot_visibility(show):
        if 'show' in show:
            return {'display': 'block'}
        else:
            return {'display': 'none'}

    return app