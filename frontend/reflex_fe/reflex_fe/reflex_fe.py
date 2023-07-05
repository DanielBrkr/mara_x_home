"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
import asyncio
from loguru import logger
from datetime import datetime
import pytz

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

    zone: str = "Europe/Berlin"
    stream_data_start: bool = True
    dataframe: pd.DataFrame = pd.DataFrame()
    temperature_figure: go.Figure = None

    current_temperature: float = 0

    def plot_database_static(self) -> None:
        """Retrieves the new dataframe with from the database, including the new received values"""
        # Todo: Annotate last update and now instead of legend

        self.dataframe = pd.read_sql_table("coffee", engine)
        self.dataframe["timestamp"] = self.dataframe["timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        x_data = self.dataframe["timestamp"]
        y_data = self.dataframe["temperature"]

        temp_plot = go.Scatter(
            x=x_data,
            y=y_data,
            mode="lines",
            name="Boiler Temperature",
            marker=dict(color="MediumPurple", size=3),
            showlegend=True,
        )

        temp_fig = go.Figure(data=[temp_plot])

        last_timestamp = self.get_last_timestamp()
        temp_fig.add_trace(
            go.Scatter(x=last_timestamp, y=pd.Series(data=0), name="Last Update")
        )

        now_timestamp = self.get_now_timestamp()
        temp_fig.add_trace(
            go.Scatter(x=now_timestamp, y=pd.Series(data=0), name="Now we're here")
        )

        self.temperature_figure = temp_fig

        logger.debug(f"Plot updated. Last data: {x_data.iloc[-1]}")

    def get_last_timestamp(self):
        x_data = self.dataframe["timestamp"]
        timestamp = pd.Series(data=x_data.iloc[-1])

        return timestamp

    def get_now_timestamp(self):
        now = datetime.now(pytz.timezone(self.zone))
        timestamp = pd.Series(data=now)

        return timestamp

    def set_current_temperature(self) -> float:
        y_data = self.dataframe["temperature"]
        self.current_temperature = y_data.iloc[-1]

        return self.current_temperature

    async def stream_plot(self):
        """Note: self.stream_plot has to be returned in this function, the plot is otherwise not being returned to
        reflex"""

        while True:
            if self.stream_data_start:
                self.plot_database_static()
                self.set_current_temperature()
                await asyncio.sleep(1)

                return self.stream_plot


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("What's the temperature of my coffee machine?", font_size="2em"),
            rx.box(
                "It's " + State.current_temperature + "°C",
                background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
                background_clip="text",
                font_weight="bold",
                font_size="2em",
            ),
            rx.plotly(
                data=State.temperature_figure, layout={"width": "1080", "height": "600"}
            ),
            rx.hstack(rx.button("Stream Temperature Data", on_click=State.stream_plot)),
            width="100%",
        ),
        padding_top="10%",
        width="100%",
    )


engine = create_engine(
    "sqlite:///E:/python_projects/mara_x_home/backend/mqtt_server/sensor_data.db"
)

# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
