"""Streamlit Dashboard for LNMH Plant Monitoring System."""

from os import environ
import logging
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import altair as alt
from pymssql import connect, Connection, exceptions, Cursor

COLOUR_PALETTE = ["#84b067", "#a7de83", "#4b633b", "#2c3b23"]


def get_connection() -> Connection:
    """Connects to Microsoft SQL Server Database"""
    logging.info("Attempting to connect to the database.")
    try:
        conn = connect(
            server=environ["DB_HOST"],
            port=environ["DB_PORT"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
            as_dict=True
        )
        logging.info("Database connection successful.")
        return conn
    except KeyError as e:
        logging.error("%s missing from environment variables.", e)
        raise
    except exceptions.OperationalError as e:
        logging.error("Error connecting to database: %s", e)
        raise
    except Exception as e:
        logging.error("Unexpected error while connecting to database: %s", e)
        raise


def get_cursor(connection: Connection) -> Cursor:
    """Cursor to execute commands in db"""
    return connection.cursor()


def homepage():
    """Homepage showing visualizations for LNMH."""
    st.title("LNMH Plant Monitoring System")
    connection = get_connection()
    cursor = get_cursor(connection)
    live_metrics = get_latest_metrics(cursor)

    plant_names = list(live_metrics['plant_name'])
    filter_plant = get_plant_filter(plant_names)
    filtered_data = filter_by_plant(
        filter_plant, live_metrics)

    st.altair_chart(plot_live_temp(filtered_data['plant_temp']))
    st.altair_chart(plot_live_moisture(filtered_data['moisture']))
    display_table(live_metrics[['plant_id', 'plant_name']])
    st.write(live_metrics)


def get_plant_filter(plant_names: list) -> str:
    """Create a filter based on plant name."""
    return st.sidebar.selectbox(
        'Filter by Plant',
        ['All Plants'] + plant_names)


def filter_by_plant(filter: str, plant_metrics: pd.DataFrame):
    """Filter visualisations based off plant name."""
    if filter != 'All Plants':
        return {
            'plant_temp': plant_metrics[plant_metrics['plant_name'] == filter],
            'moisture': plant_metrics[plant_metrics['plant_name'] == filter]
        }
    return {
        'plant_temp': plant_metrics,
        'moisture': plant_metrics
    }


def get_latest_metrics(cursor: Cursor) -> pd.DataFrame:
    query = f"""
        SELECT pm.temperature, pm.soil_moisture, latest_recording_info.latest_time, p.plant_name, pm.plant_id
        FROM {environ['SCHEMA_NAME']}.plant_metric pm
        JOIN (SELECT plant_id,
            MAX(recording_taken) as latest_time
            FROM {environ['SCHEMA_NAME']}.plant_metric
            GROUP BY plant_id) as latest_recording_info
        ON pm.plant_id = latest_recording_info.plant_id
            AND pm.recording_taken = latest_recording_info.latest_time
        JOIN {environ['SCHEMA_NAME']}.plant as p ON pm.plant_id = p.plant_id;
        """
    cursor.execute(query)
    result = cursor.fetchall()

    return pd.DataFrame(result)


def plot_live_temp(data: pd.DataFrame):
    """Chart to show current temp and soil moisture levels."""
    data['plant_id_name'] = data['plant_name'] + \
        ' (ID: ' + data['plant_id'].astype(str) + ')'

    chart = alt.Chart(data, title="Live Plant Temperature").mark_bar().encode(
        x=alt.X(
            "plant_id:N",
            title="Plant ID"),
        y=alt.Y(
            "temperature:Q",
            title="Temperature (°C)"),
        color=alt.Color(
            "temperature:Q",
            scale=alt.Scale(
                range=COLOUR_PALETTE,
                domain=[data["temperature"].min(), data["temperature"].max()]
            )
        ),
        tooltip=[alt.Tooltip("temperature:Q", title="Temperature (°C)"),
                 alt.Tooltip("plant_id_name:N", title="Plant ID & Name")]
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).interactive()

    return chart


def plot_live_moisture(data: pd.DataFrame):
    data['plant_id_name'] = data['plant_name'] + \
        ' (ID: ' + data['plant_id'].astype(str) + ')'

    chart = alt.Chart(data, title="Live Plant Soil Moisture Levels").mark_bar().encode(
        x=alt.X(
            "plant_id:N",
            title="Plant ID"),
        y=alt.Y(
            "soil_moisture:Q",
            title="Soil Moisture"),
        color=alt.Color(
            "soil_moisture:Q",
            scale=alt.Scale(
                range=COLOUR_PALETTE,
                domain=[data["soil_moisture"].min(), data["soil_moisture"].max()]
            )
        ),
        tooltip=[alt.Tooltip("soil_moisture:Q", title="Soil Moisture (°C)"),
                 alt.Tooltip("plant_id_name:N", title="Plant ID & Name")]
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).interactive()

    return chart


def create_table_plant_id_name(data: pd.DataFrame):

    return data[['plant_name', 'plant_id']].rename(columns={
        'plant_id': 'Plant ID',
        'plant_name': 'Plant Name'
    }).set_index('Plant ID').sort_index().style.set_table_styles([{'selector': 'col0', 'props': [('width', '100px')]},
                                                                 {'selector': 'col1', 'props': [('width', '200px')]}])


def display_table(data):
    st.write(create_table_plant_id_name(data))
    return


if __name__ == "__main__":
    load_dotenv()

    homepage()
