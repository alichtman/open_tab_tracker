import plotly.express as px
import pandas as pd


def draw_graph(df: pd.DataFrame, graph_type="line"):
    if graph_type == "line":
        fig = px.line(
            df, x="datetime", y="firefox_tab_count", title="Open tab count over time"
        )
    elif graph_type == "scatter":
        fig = px.scatter(
            df,
            x="datetime",
            y="firefox_tab_count",
            size="firefox_tab_count",
            title="Open tab count over time",
        )

    fig.show()
