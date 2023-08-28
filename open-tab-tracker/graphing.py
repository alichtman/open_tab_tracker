import matplotlib.pyplot as plt
import pandas as pd


def draw_graph(data):
    # Let's make sure 'date' is actually a date in pandas
    data["date"] = pd.to_datetime(data["date"])
    date = data["date"]
    value = data["value"]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(date, value)
