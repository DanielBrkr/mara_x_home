"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
import asyncio
from loguru import logger

filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

    zone: str = "Europe/Berlin"
    stream_data_start: bool = True
    dataframe: pd.DataFrame = pd.DataFrame()

    figure: go.Figure = None

    def plot_database_static(self) -> None:
        """Retrieves the new dataframe with from the database, including the new received values"""

        self.dataframe = pd.read_sql_table("coffee", engine)
        self.dataframe["timestamp"] = self.dataframe["timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        x_data = self.dataframe["timestamp"]
        y_data = self.dataframe["temperature"]
        fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data)])
        self.figure = fig

        logger.debug("Plot updated.")

    async def stream_plot(self):
        while True:
            await asyncio.sleep(3)
            self.plot_database_static()


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Siebträger Temperatur", font_size="2em"),
            rx.box("Prototype Dummy "),
            rx.plotly(data=State.figure, height="1080px", width="1080px"),
            rx.hstack(rx.button("Update plot", on_click=State.plot_database_static)),
        ),
        padding_top="10%",
    )


engine = create_engine(
    "sqlite:///E:/python_projects/mara_x_home/backend/mqtt_server/sensor_data.db"
)


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
