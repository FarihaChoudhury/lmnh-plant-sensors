"""Streamlit Dashboard for LNMH Plant Monitoring System."""

from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import altair as alt

from db_queries import (get_archival_data, get_latest_metrics,
                        get_connection, get_cursor, get_plant_image_url)

COLOUR_PALETTE = ["#84b067", "#a7de83", "#4b633b", "#2c3b23"]


def homepage() -> None:
    """Homepage showing visualizations for LNMH."""

    st.set_page_config(page_title="LNHM Plant Metrics",
                       page_icon="seedling", layout="wide")
    emoji_left, title, emoji_right = st.columns((1, 2, 1))
    with emoji_left:
        st.title("🌱🌵🍄")
    with title:
        st.markdown(
            "<h1 style='text-align: center;'>LNMH Plant Monitoring System</h1>",
            unsafe_allow_html=True)

    with emoji_right:
        st.markdown("<h1 style='text-align: right;'>🍄🌵🌱</h1>",
                    unsafe_allow_html=True)

    connection = get_connection()
    cursor = get_cursor(connection)
    live_metrics = get_latest_metrics(cursor)
    archival_metrics = get_archival_data(cursor)

    filter_plant = get_plant_filter(list(live_metrics['plant_name']))
    st.write(" ")

    filtered_data = filter_by_plant(
        filter_plant, live_metrics, archival_metrics)

    display_charts(filtered_data[0], filtered_data[1], cursor)


def display_charts(data_live: pd.DataFrame, data_archival: pd.DataFrame, cursor) -> None:
    """Function to display and format charts."""
    left, space, right = st.columns((6, 0.2, 1))
    with left:
        st.altair_chart(overlay_temperature_chart(data_live,
                                                  data_archival))
        st.write(" ")
        st.altair_chart(overlay_soil_moisture_chart(data_live,
                                                    data_archival))
        st.write(" ")
        st.altair_chart(plot_last_watered(data_live))

    with right:
        table_data = get_data_plant_table(data_live)
        st.write(
            table_data.style.set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'left')]},
                {'selector': 'td', 'props': [('width', '100px')]},
                {'selector': 'col1', 'props': [('width', '200px')]}
            ])
        )
        st.write("")
        st.write("")

        single_plant_chosen = filter_single_plant_for_image(
            data_live['plant_name'].unique())
        plant_url = get_plant_image_url(cursor, single_plant_chosen)
        display_plant_image(plant_url)

    st.altair_chart(plot_last_watered(data_live))


def filter_single_plant_for_image(plant_names: list) -> str:
    """Filter for one plant to display image for"""
    return st.selectbox(
        "Choose a plant to view! 🌷",
        options=plant_names,
        key="plant_dropdown"
    )


def display_plant_image(plant_url: str) -> None:
    """Displays a plant image by its url if it exists in database."""
    if plant_url:
        st.image(plant_url['image_url'],
                 use_container_width=True, width=500)


def get_plant_filter(plant_names: list, key: str = "plant_filter") -> list:
    """Create a multiselect filter based on plant names."""
    return st.multiselect(
        'Filter by Plant(s)',
        options=plant_names,
        default=plant_names,
        key=key
    )


def filter_by_plant(selected_plants: list, plant_metrics: pd.DataFrame,
                    archive_plants: pd.DataFrame) -> list:
    """Filter visualizations based on selected plant names."""
    if selected_plants:
        return [plant_metrics[plant_metrics['plant_name'].isin(selected_plants)],
                archive_plants[archive_plants['plant_name'].isin(selected_plants)]]
    return [plant_metrics, archive_plants]


def link_plant_name_id(data: pd.DataFrame) -> pd.DataFrame:
    """Create a link between id and name in the dataframe."""
    data['plant_id_name'] = data['plant_name'] + \
        ' (ID: ' + data['plant_id'].astype(str) + ')'
    return data


def plot_live_temp(data: pd.DataFrame) -> alt.Chart:
    """Function to create a chart to show current temperature for each plant ID."""

    data = link_plant_name_id(data)

    chart = alt.Chart(data, title="Live Plant Temperature").mark_bar(width=10).encode(
        x=alt.X(
            "plant_id:N",
            title="Plant ID"),
        y=alt.Y(
            "temperature:Q",
            title="Temperature (°C)"),
        color=alt.Color(
            "temperature:Q",
            title="Temperature (°C)",
            scale=alt.Scale(
                range=COLOUR_PALETTE,
                domain=[data["temperature"].min(), data["temperature"].max()]
            )
        ),
        tooltip=[alt.Tooltip("temperature:Q", title="Temperature (°C)"),
                 alt.Tooltip("plant_id_name:N", title="Plant Name (ID)")]
    )

    return chart


def plot_live_moisture(data: pd.DataFrame) -> alt.Chart:
    """Function to create a plot for the live soil moisture levels of each plant."""
    data = link_plant_name_id(data)

    chart = alt.Chart(data, title="Live Plant Soil Moisture Levels").mark_bar(width=10).encode(
        x=alt.X(
            "plant_id:N",
            title="Plant ID"),
        y=alt.Y(
            "soil_moisture:Q",
            title="Soil Moisture"),
        color=alt.Color(
            "soil_moisture:Q",
            title="Soil Moisture Levels",
            scale=alt.Scale(
                range=COLOUR_PALETTE,
                domain=[data["soil_moisture"].min(), data["soil_moisture"].max()]
            )
        ),
        tooltip=[alt.Tooltip("soil_moisture:Q", title="Soil Moisture"),
                 alt.Tooltip("plant_id_name:N", title="Plant Name (ID)")]
    )
    return chart


def get_data_plant_table(data: dict) -> pd.DataFrame:
    """Display a table with plant IDs and names in Streamlit."""

    df = pd.DataFrame({
        'plant_id': data['plant_id'],
        'plant_name': data['plant_name']
    })

    return df.rename(columns={
        'plant_id': 'Plant ID',
        'plant_name': 'Plant Name'
    }).set_index('Plant ID').sort_index()


def plot_last_watered(data: pd.DataFrame) -> alt.Chart:
    """Function to create a plot showing when each plant was last watered."""
    data = link_plant_name_id(data)
    chart = alt.Chart(data, title="Last Watered").mark_point().encode(
        x=alt.X(
            "plant_id:N",
            title="Plant ID"),
        y=alt.Y(
            "last_watered:T",
            title="Last Watered At"),
        color=alt.Color(
            "last_watered:T",
            legend=None,
            scale=alt.Scale(
                range=COLOUR_PALETTE,
                domain=[data["last_watered"].min(
                ), data["last_watered"].max()]
            )
        ),
        tooltip=[alt.Tooltip("last_watered:T", title="Last Watered At"),
                 alt.Tooltip("plant_id_name:N", title="Plant Name (ID)")]
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).interactive()

    return chart


def create_avg_temp_line(data: pd.DataFrame) -> alt.Chart:
    """Create a line for the average temperature for each plant."""
    data = link_plant_name_id(data)
    avg_line = alt.Chart(data).mark_line(color='#9367B0', point=True).encode(
        x=alt.X('plant_id:N', title="Plant ID"),
        y=alt.Y('avg_temperature:Q', title="Average Temperature (°C)"),
        tooltip=[alt.Tooltip('avg_temperature:Q', title="Average Temperature (°C)"),
                 alt.Tooltip("plant_id_name:N", title="Plant Name (ID)")]
    )
    return avg_line


def create_avg_soil_line(data: pd.DataFrame) -> alt.Chart:
    """Create a line for the average soil moisture levels for each plant."""

    data = link_plant_name_id(data)
    avg_line = alt.Chart(data).mark_line(color='#9367B0', point=True).encode(
        x=alt.X('plant_id:N', title="Plant ID"),
        y=alt.Y('avg_soil_moisture:Q', title="Average Soil Moisture Levels"),
        tooltip=[alt.Tooltip('avg_soil_moisture:Q', title="Average Soil Moisture Level"),
                 alt.Tooltip("plant_id_name:N", title="Plant Name (ID)")]
    )
    return avg_line


def overlay_temperature_chart(data_live: pd.DataFrame, data_archival: pd.DataFrame) -> alt.Chart:
    """Overlay the live temperature chart with the average line."""
    bar_chart = plot_live_temp(data_live)
    avg_line = create_avg_temp_line(data_archival)

    combined_chart = alt.layer(bar_chart, avg_line).resolve_scale(
        y='shared',
        x='shared'
    ).properties(
        height=400,
        title="Live Plant Temperature with Average"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).interactive()
    return combined_chart


def overlay_soil_moisture_chart(data_live: pd.DataFrame, data_archival: pd.DataFrame) -> alt.Chart:
    """Overlay the live soil moisture levels with the average line for each plant."""
    bar_chart = plot_live_moisture(data_live)
    avg_line = create_avg_soil_line(data_archival)

    combined_chart = alt.layer(bar_chart, avg_line).resolve_scale(
        y='shared',
        x='shared'
    ).properties(
        height=400,
        title="Live Plant Soil Moisture Levels with Average"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).interactive()
    return combined_chart


if __name__ == "__main__":
    load_dotenv()
    homepage()
