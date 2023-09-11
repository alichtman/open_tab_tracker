from datetime import datetime, timezone
import plotly.express as px
import pandas as pd
from loguru import logger


def convert_utc_datetime_to_local_formatted_string(utc_time_str: str):
    utc_datetime: datetime = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S.%f%z")
    current_timezone = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
    logger.debug(f"Converted {utc_time_str} to {current_timezone}")
    return current_timezone.strftime("%m/%d/%y %I:%M%p")


def draw_graph(df: pd.DataFrame, graph_type="line"):
    df["datetime"] = df["datetime"].apply(
        lambda x: convert_utc_datetime_to_local_formatted_string(x)
    )
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
