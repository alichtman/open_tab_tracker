import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime
from typing import List, Tuple


def draw_graph(data: List[Tuple[datetime, int]]):
    # TODO: Make this plot prettier
    times = [datetime.strptime(entry[0], '%Y-%m-%d %H:%M:%S.%f%z') for entry in data]
    times = [time.strftime("%d-%b-%Y %I.%M %p") for time in times]
    values = [int(entry[1]) for entry in data]

    sns.set_theme()
    sns.set(font_scale=0.5)
    sns.color_palette("coolwarm", as_cmap=True)
    sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})
    #  sns.set_theme(style="darkgrid")
    sns.lineplot(x=times, y=values)

    plt.ylim(0)
    plt.ylabel("Firefox tab count")
    plt.xlabel("Time")
    plt.title("Open tab count over time")
    plt.xticks(rotation=90)
    #  plt.margins(0.2)
    plt.show()
