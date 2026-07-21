
# ============================================================
# SOLAR FIJI ENVIRONMENTAL FORECAST DASHBOARD
# SOLAR_FIJI_FINAL_BRANDING_PATCH_V1
# ============================================================

from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Solar Fiji Environmental Forecast",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(
    "/content/drive/MyDrive/Solar_Fiji_AQI"
)

PREDICTIONS_DIR = (
    PROJECT_ROOT
    / "results"
    / "predictions"
)

METRICS_DIR = (
    PROJECT_ROOT
    / "results"
    / "metrics"
)

DASHBOARD_DIR = (
    PROJECT_ROOT
    / "dashboard"
)

CURRENT_FORECAST_FILE = (
    PREDICTIONS_DIR
    / "current_live_forecast.csv"
)

DASHBOARD_FORECAST_FILE = (
    PREDICTIONS_DIR
    / "current_dashboard_forecast.csv"
)

FORECAST_ARCHIVE_FILE = (
    PREDICTIONS_DIR
    / "live_forecast_archive.csv"
)

HISTORICAL_PREDICTIONS_FILE = (
    PREDICTIONS_DIR
    / "live_compatible_final_test_predictions.csv"
)

MODEL_COMPARISON_FILE = (
    METRICS_DIR
    / "live_final_model_comparison.csv"
)

FEATURE_IMPORTANCE_FILE = (
    METRICS_DIR
    / "live_xgboost_feature_importance.csv"
)

AQI_COMPARISON_FILE = (
    METRICS_DIR
    / "live_aqi_model_comparison.csv"
)

SITE_REPORT_FILE = (
    DASHBOARD_DIR
    / "solar_fiji_site_reports.csv"
)


# ============================================================
# 3. CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .main-title {
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    .forecast-banner {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.3rem;
    }

    .section-note {
        border-left: 4px solid rgba(128,128,128,0.45);
        padding: 0.8rem 1rem;
        margin: 1rem 0;
        background: rgba(128,128,128,0.06);
        border-radius: 5px;
    }

    .action-box {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 14px;
        padding: 1.1rem;
        min-height: 135px;
    }

    .small-label {
        font-size: 0.80rem;
        opacity: 0.65;
        text-transform: uppercase;
        letter-spacing: 0.04rem;
    }

    .large-value {
        font-size: 1.55rem;
        font-weight: 720;
        margin-top: 0.3rem;
    }

    .footer {
        text-align: center;
        opacity: 0.55;
        margin-top: 3rem;
        font-size: 0.85rem;
    }

    

    /* ======================================================
       SOLAR FIJI BRAND REFINEMENTS
       ====================================================== */

    :root {
        --solar-yellow: #FDB813;
        --solar-orange: #F59E0B;
        --solar-green: #1B4332;
        --solar-light-yellow: #FFF9E6;
        --solar-light-green: #EAF7EC;
        --solar-light-orange: #FFF4D6;
        --solar-border: #E5E7EB;
    }


    /* Main headings */

    h1,
    h2,
    h3 {
        color: var(--solar-green);
    }


    /* Sidebar branding */

    [data-testid="stSidebar"] {
        border-right: 3px solid var(--solar-yellow);
    }


    [data-testid="stSidebar"] h1 {
        color: var(--solar-green);
    }


    /* Standard Streamlit metric cards */

    [data-testid="stMetric"] {

        background: white;

        border:
            1px solid
            var(--solar-border);

        border-top:
            4px solid
            var(--solar-yellow);

        border-radius:
            14px;

        padding:
            1rem 1.1rem;

        min-height:
            135px;

        box-shadow:
            0 2px 8px
            rgba(
                0,
                0,
                0,
                0.035
            );
    }


    [data-testid="stMetricLabel"] {

        font-weight: 600;

        color: #4B5563;
    }


    /* Primary forecast banner */

    .forecast-banner {

        border-top:
            5px solid
            var(--solar-yellow)
            !important;

        background:

            linear-gradient(

                100deg,

                rgba(
                    253,
                    184,
                    19,
                    0.10
                ),

                rgba(
                    255,
                    255,
                    255,
                    1
                )

            );
    }


    /* Recommended action box */

    .action-box {

        border-left:
            5px solid
            var(--solar-orange)
            !important;

        background:
            linear-gradient(

                90deg,

                rgba(
                    245,
                    158,
                    11,
                    0.07
                ),

                white

            );
    }


    /* Custom AQI status cards */

    .aqi-status-card {

        border-radius:
            14px;

        padding:
            1rem 1.1rem;

        min-height:
            135px;

        box-shadow:
            0 2px 8px
            rgba(
                0,
                0,
                0,
                0.035
            );
    }


    .aqi-good {

        background:
            #EAF7EC;

        border:
            1px solid
            #B7DFC0;

        border-top:
            4px solid
            #52B788;
    }


    .aqi-moderate {

        background:
            #FFF4D6;

        border:
            1px solid
            #F6D58A;

        border-top:
            4px solid
            #F4A261;
    }


    .aqi-warning {

        background:
            #FDECEC;

        border:
            1px solid
            #F1B6B6;

        border-top:
            4px solid
            #D62828;
    }


    .aqi-card-label {

        font-size:
            0.88rem;

        color:
            #4B5563;

        font-weight:
            600;
    }


    .aqi-card-value {

        font-size:
            2.2rem;

        line-height:
            1.15;

        font-weight:
            700;

        color:
            var(--solar-green);

        margin-top:
            0.65rem;
    }


    .aqi-card-badge {

        display:
            inline-block;

        margin-top:
            0.7rem;

        padding:
            0.22rem
            0.55rem;

        border-radius:
            999px;

        background:
            rgba(
                255,
                255,
                255,
                0.72
            );

        font-size:
            0.88rem;

        font-weight:
            600;

        color:
            var(--solar-green);
    }


    /* Buttons */

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {

        border:
            1px solid
            var(--solar-orange);

        border-radius:
            9px;

        font-weight:
            600;
    }


    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {

        border-color:
            var(--solar-yellow);

        color:
            var(--solar-green);
    }


    /* Dataframe subtle branding */

    [data-testid="stDataFrame"] {

        border-radius:
            12px;

        overflow:
            hidden;

        border:
            1px solid
            var(--solar-border);
    }

    


    /* ======================================================
       SOLAR FIJI FINAL BRANDING
       ====================================================== */

    :root {

        --solar-yellow:
            #FDB813;

        --solar-orange:
            #F59E0B;

        --solar-green:
            #1B4332;

        --solar-light-green:
            #EAF7EC;

        --solar-light-amber:
            #FFF4D6;

        --solar-light-red:
            #FDECEC;

        --solar-border:
            #E5E7EB;

    }


    /* ------------------------------------------------------
       HEADINGS
       ------------------------------------------------------ */

    h1,
    h2,
    h3 {

        color:
            var(
                --solar-green
            );

    }


    /* ------------------------------------------------------
       SIDEBAR
       ------------------------------------------------------ */

    [data-testid="stSidebar"] {

        border-right:

            3px solid
            var(
                --solar-yellow
            );

    }


    [data-testid="stSidebar"] h1 {

        color:

            var(
                --solar-green
            );

    }


    /* ------------------------------------------------------
       STANDARD STREAMLIT METRICS
       ------------------------------------------------------ */

    [data-testid="stMetric"] {

        background:

            #FFFFFF;

        border:

            1px solid
            var(
                --solar-border
            );

        border-top:

            4px solid
            var(
                --solar-yellow
            );

        border-radius:

            14px;

        padding:

            1rem
            1.1rem;

        min-height:

            135px;

        box-shadow:

            0
            2px
            8px

            rgba(
                0,
                0,
                0,
                0.04
            );

    }


    [data-testid="stMetricLabel"] {

        font-weight:

            600;

        color:

            #4B5563;

    }


    /* ------------------------------------------------------
       PRIMARY FORECAST BANNER
       ------------------------------------------------------ */

    .forecast-banner {

        border-top:

            5px solid
            var(
                --solar-yellow
            )

            !important;

        background:

            linear-gradient(

                100deg,

                rgba(
                    253,
                    184,
                    19,
                    0.10
                ),

                rgba(
                    255,
                    255,
                    255,
                    1
                )

            );

    }


    /* ------------------------------------------------------
       RECOMMENDED ACTION
       ------------------------------------------------------ */

    .action-box {

        border-left:

            5px solid
            var(
                --solar-orange
            )

            !important;

        background:

            linear-gradient(

                90deg,

                rgba(
                    245,
                    158,
                    11,
                    0.07
                ),

                #FFFFFF

            );

    }


    /* ------------------------------------------------------
       AQI STATUS CARD
       ------------------------------------------------------ */

    .aqi-status-card {

        border-radius:

            14px;

        padding:

            1rem
            1.1rem;

        min-height:

            135px;

        box-sizing:

            border-box;

        box-shadow:

            0
            2px
            8px

            rgba(
                0,
                0,
                0,
                0.04
            );

    }


    .aqi-good {

        background:

            #EAF7EC;

        border:

            1px solid
            #B7DFC0;

        border-top:

            4px solid
            #52B788;

    }


    .aqi-moderate {

        background:

            #FFF4D6;

        border:

            1px solid
            #F6D58A;

        border-top:

            4px solid
            #F4A261;

    }


    .aqi-warning {

        background:

            #FDECEC;

        border:

            1px solid
            #F1B6B6;

        border-top:

            4px solid
            #D62828;

    }


    .aqi-card-label {

        font-size:

            0.9rem;

        font-weight:

            600;

        color:

            #4B5563;

    }


    .aqi-card-value {

        font-size:

            2.15rem;

        line-height:

            1.15;

        font-weight:

            700;

        color:

            #1B4332;

        margin-top:

            0.55rem;

    }


    .aqi-card-badge {

        display:

            inline-block;

        margin-top:

            0.65rem;

        padding:

            0.25rem
            0.60rem;

        border-radius:

            999px;

        background:

            rgba(
                255,
                255,
                255,
                0.75
            );

        color:

            #1B4332;

        font-size:

            0.88rem;

        font-weight:

            600;

    }


    /* ------------------------------------------------------
       BUTTONS
       ------------------------------------------------------ */

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {

        border:

            1px solid
            var(
                --solar-orange
            );

        border-radius:

            9px;

        font-weight:

            600;

    }


    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {

        border-color:

            var(
                --solar-yellow
            );

        color:

            var(
                --solar-green
            );

    }


    /* ------------------------------------------------------
       DATA TABLES
       ------------------------------------------------------ */

    [data-testid="stDataFrame"] {

        border:

            1px solid
            var(
                --solar-border
            );

        border-radius:

            12px;

        overflow:

            hidden;

    }


</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. DATA LOADING
# ============================================================

@st.cache_data
def load_csv(
    file_path,
    parse_dates=None,
):
    if not Path(file_path).exists():
        return pd.DataFrame()

    return pd.read_csv(
        file_path,
        parse_dates=parse_dates,
    )


forecast_df = load_csv(
    CURRENT_FORECAST_FILE,
    parse_dates=["date"],
)

historical_predictions = load_csv(
    HISTORICAL_PREDICTIONS_FILE,
    parse_dates=["date"],
)

model_comparison = load_csv(
    MODEL_COMPARISON_FILE,
)

feature_importance = load_csv(
    FEATURE_IMPORTANCE_FILE,
)

aqi_comparison = load_csv(
    AQI_COMPARISON_FILE,
)

forecast_archive = load_csv(
    FORECAST_ARCHIVE_FILE,
)


# ============================================================
# 5. REQUIRED LIVE FORECAST CHECK
# ============================================================

if forecast_df.empty:

    st.error(
        """
        No current forecast was found.

        Run Phase 5 first to generate:

        current_live_forecast.csv
        """
    )

    st.stop()


forecast_df = (
    forecast_df
    .sort_values("date")
    .reset_index(drop=True)
)


# ============================================================
# 6. HELPER FUNCTIONS
# ============================================================

def safe_number(
    value,
    digits=1,
):

    if pd.isna(value):
        return "Not available"

    return f"{float(value):.{digits}f}"












def format_fiji_timestamp(
    value,
):

    """
    Convert ISO timestamp to:
    18 Jul 2026, 8:16 AM Fiji time
    """

    try:

        timestamp = pd.to_datetime(
            value
        )


        date_text = (
            timestamp.strftime(
                "%d %b %Y"
            )
        )


        time_text = (

            timestamp.strftime(
                "%I:%M %p"
            )

            .lstrip(
                "0"
            )
        )


        return (

            f"{date_text}, "
            f"{time_text} Fiji time"

        )


    except Exception:

        return str(
            value
        )



def get_aqi_card_class(
    category,
):

    category_text = (

        str(
            category
        )

        .strip()

        .lower()
    )


    if category_text == "good":

        return "aqi-good"


    if category_text == "moderate":

        return "aqi-moderate"


    return "aqi-warning"



def render_aqi_status_card(
    category,
    aqi,
):

    """
    Render the AQI card as HTML.

    IMPORTANT:
    The HTML is deliberately constructed as one continuous
    string so Streamlit Markdown cannot interpret indentation
    as a code block.
    """

    card_class = (
        get_aqi_card_class(
            category
        )
    )


    try:

        aqi_text = str(
            int(
                round(
                    float(
                        aqi
                    )
                )
            )
        )


    except Exception:

        aqi_text = (
            "Not available"
        )


    html = (

        f'<div class="aqi-status-card {card_class}">'

        f'<div class="aqi-card-label">'
        f'Air quality'
        f'</div>'

        f'<div class="aqi-card-value">'
        f'{category}'
        f'</div>'

        f'<div class="aqi-card-badge">'
        f'AQI {aqi_text}'
        f'</div>'

        f'</div>'

    )


    st.markdown(

        html,

        unsafe_allow_html=True,

    )



def friendly_feature_name(
    feature,
):

    mapping = {

        "pm25_lag_1":
            "Yesterday's PM2.5",

        "pm25_rolling_mean_3":
            "Recent 3-day PM2.5",

        "wind_speed_10m_m_s":
            "Wind speed",

        "pm25_previous_day_change":
            "Recent PM2.5 change",

        "pm25_lag_2":
            "PM2.5 two days ago",

        "temperature_max_c":
            "Maximum temperature",

        "temperature_mean_c":
            "Average temperature",

        "pm25_rolling_mean_14":
            "14-day PM2.5 trend",

        "precipitation_mm":
            "Rainfall",

        "shortwave_radiation_kwh_m2_day":
            "Expected sunlight",

        "surface_pressure_kpa":
            "Surface pressure",

        "relative_humidity_pct":
            "Humidity",

        "pm25_lag_14":
            "PM2.5 two weeks ago",

        "wind_direction_sin":
            "Wind direction pattern",

        "wind_direction_cos":
            "Wind direction pattern",

        "pm25_lag_7":
            "PM2.5 one week ago",

        "day_of_year_sin":
            "Seasonal timing",
    }

    return mapping.get(
        feature,
        feature.replace(
            "_",
            " ",
        ).title(),
    )


def sunlight_label(
    radiation,
):

    if pd.isna(radiation):
        return "Unavailable"

    if radiation < 2:
        return "Very limited"

    if radiation < 4:
        return "Moderate"

    if radiation < 6:
        return "Good"

    return "Strong"


def rainfall_label(
    rainfall,
):

    if pd.isna(rainfall):
        return "Unavailable"

    if rainfall < 1:
        return "Little or no rain"

    if rainfall < 10:
        return "Some rainfall"

    if rainfall < 30:
        return "Heavy rainfall"

    return "Very heavy rainfall"


def confidence_message(
    row,
):

    lower = row[
        "model_lower_95"
    ]

    upper = row[
        "model_upper_95"
    ]


    if pd.isna(lower) or pd.isna(upper):
        return "Forecast uncertainty unavailable."


    # PM2.5 threshold used by the project AQI method.
    if (
        lower <= 9.0
        and
        upper >= 9.1
    ):

        return (
            "The forecast interval crosses the Good–Moderate "
            "air-quality boundary, so conditions should be monitored."
        )


    return (
        "The forecast interval remains within the same broad "
        "air-quality range."
    )


# ============================================================
# 7. PRIMARY FORECAST
# ============================================================

primary = (
    forecast_df.iloc[0]
)


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "☀️ Solar Fiji"
    )

    st.caption(
        "Environmental Forecast Prototype"
    )

    st.markdown("---")

    page = st.radio(

        "Navigate",

        [

            "Latest Forecast",

            "Historical Performance",

            "What Affected the Forecast?",

            "Report a Site Condition",

            "Technical Details",

            "About the Prototype",

        ],

        index=0,
    )


    st.markdown("---")


    st.write(
        "**Pilot location**"
    )

    st.write(
        "Suva / Nasinu"
    )


    st.write(
        "**Primary forecast horizon**"
    )

    st.write(
        "1 day ahead"
    )


    if (
        "forecast_generated_at_fiji"
        in forecast_df.columns
    ):

        generated_time = (

            forecast_df

            .iloc[0][
                "forecast_generated_at_fiji"
            ]
        )


        formatted_generated_time = (
            format_fiji_timestamp(
                generated_time
            )
        )


        st.caption(
            "Latest forecast generated"
        )


        st.write(
            f"**{formatted_generated_time}**"
        )


    if st.button(
        "Reload latest files"
    ):

        st.cache_data.clear()

        st.rerun()


# ============================================================
# PAGE 1 — LATEST FORECAST
# ============================================================

if page == "Latest Forecast":

    st.markdown(

        '<div class="main-title">'
        'Bula Vinaka — Solar Fiji Environmental Forecast'
        '</div>',

        unsafe_allow_html=True,
    )


    st.markdown(

        '<div class="subtitle">'
        'Decision support for air quality, weather and '
        'solar operating conditions in Suva and Nasinu.'
        '</div>',

        unsafe_allow_html=True,
    )


    forecast_date = pd.to_datetime(

        primary[
            "date"
        ]

    ).strftime(
        "%A, %d %B %Y"
    )


    st.markdown(

        f"""
        <div class="forecast-banner">

        <div class="small-label">
        Primary forecast
        </div>

        <div class="large-value">
        {forecast_date}
        </div>

        This is the project's validated one-day-ahead forecast horizon.

        </div>
        """,

        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # Primary cards
    # --------------------------------------------------------

    column1, column2, column3, column4 = st.columns(
        4
    )


    with column1:

        render_aqi_status_card(

            category=primary[
                "model_aqi_category"
            ],

            aqi=primary[
                "model_aqi"
            ],
        )


    with column2:

        st.metric(

            "Predicted PM2.5",

            (
                f"{primary['model_pm25_prediction']:.1f} "
                "µg/m³"
            ),
        )


    with column3:

        st.metric(

            "Expected sunlight",

            sunlight_label(

                primary[
                    "shortwave_radiation_kwh_m2_day"
                ]
            ),

            (
                f"{primary['shortwave_radiation_kwh_m2_day']:.1f} "
                "kWh/m²/day"
            ),
        )


    with column4:

        st.metric(

            "Solar operating conditions",

            primary[
                "solar_impact"
            ],
        )


    # --------------------------------------------------------
    # Recommended action
    # --------------------------------------------------------

    st.subheader(
        "What should Solar Fiji do?"
    )


    st.markdown(

        f"""
        <div class="action-box">

        <div class="small-label">
        Recommended action
        </div>

        <div class="large-value">
        {primary['recommended_action']}
        </div>

        </div>
        """,

        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # Conditions
    # --------------------------------------------------------

    st.subheader(
        "Expected environmental conditions"
    )


    condition1, condition2, condition3, condition4 = st.columns(
        4
    )


    with condition1:

        st.metric(

            "Temperature",

            (
                f"{primary['temperature_mean_c']:.1f} °C"
            ),
        )


    with condition2:

        st.metric(

            "Rainfall",

            rainfall_label(

                primary[
                    "precipitation_mm"
                ]
            ),

            (
                f"{primary['precipitation_mm']:.1f} mm"
            ),
        )


    with condition3:

        st.metric(

            "Wind speed",

            (
                f"{primary['wind_speed_10m_m_s']:.1f} m/s"
            ),
        )


    with condition4:

        external_pm25 = (

            primary[
                "external_cams_pm25_forecast"
            ]
        )


        st.metric(

            "External CAMS comparison",

            (
                f"{external_pm25:.1f} µg/m³"

                if pd.notna(
                    external_pm25
                )

                else

                "Not available"
            ),
        )


    # --------------------------------------------------------
    # Forecast uncertainty
    # --------------------------------------------------------

    st.subheader(
        "Forecast confidence"
    )


    st.info(

        (
            f"The model predicts "
            f"{primary['model_pm25_prediction']:.1f} µg/m³, "
            f"with a 95% forecast interval of "
            f"{primary['model_lower_95']:.1f}–"
            f"{primary['model_upper_95']:.1f} µg/m³. "
            f"{confidence_message(primary)}"
        )
    )


    st.warning(

        """
        The regression model performed best overall but did not detect
        Moderate AQI days reliably in the historical test period.
        Forecasts close to an AQI boundary should therefore be interpreted
        alongside the external CAMS outlook and local site observations.
        """
    )


    # --------------------------------------------------------
    # Seven-day outlook
    # --------------------------------------------------------

    st.subheader(
        "7-day environmental outlook"
    )


    outlook_display = (

        forecast_df[

            [

                "date",

                "forecast_day",

                "model_pm25_prediction",

                "model_aqi",

                "model_aqi_category",

                "external_cams_pm25_forecast",

                "temperature_mean_c",

                "precipitation_mm",

                "wind_speed_10m_m_s",

                "shortwave_radiation_kwh_m2_day",

                "solar_impact",

            ]

        ]

        .copy()
    )


    outlook_display = outlook_display.rename(

        columns={

            "date":
                "Date",

            "forecast_day":
                "Day",

            "model_pm25_prediction":
                "Model PM2.5",

            "model_aqi":
                "AQI",

            "model_aqi_category":
                "Air quality",

            "external_cams_pm25_forecast":
                "External CAMS PM2.5",

            "temperature_mean_c":
                "Temperature °C",

            "precipitation_mm":
                "Rain mm",

            "wind_speed_10m_m_s":
                "Wind m/s",

            "shortwave_radiation_kwh_m2_day":
                "Sunlight kWh/m²/day",

            "solar_impact":
                "Operating conditions",

        }
    )


    # Format dates for presentation.

    if (
        "Date"
        in outlook_display.columns
    ):

        outlook_display[
            "Date"
        ] = (

            pd.to_datetime(

                outlook_display[
                    "Date"
                ]

            )

            .dt

            .strftime(
                "%d %b %Y"
            )
        )


    numeric_columns = [

        "Model PM2.5",

        "External CAMS PM2.5",

        "Temperature °C",

        "Rain mm",

        "Wind m/s",

        "Sunlight kWh/m²/day",

    ]


    for column in numeric_columns:

        if column in outlook_display.columns:

            outlook_display[
                column
            ] = (

                outlook_display[
                    column
                ]

                .round(1)
            )


    st.dataframe(

        outlook_display,

        use_container_width=True,

        hide_index=True,
    )


    st.caption(

        """
        Day 1 is the project's primary validated forecast horizon.
        Days 2–7 are extended multi-day planning outlooks and carry
        greater uncertainty.
        """
    )


    # --------------------------------------------------------
    # PM2.5 chart
    # --------------------------------------------------------

    chart_df = (

        forecast_df[

            [

                "date",

                "model_pm25_prediction",

                "model_lower_95",

                "model_upper_95",

                "external_cams_pm25_forecast",

            ]

        ]

        .copy()
    )


    figure = go.Figure()


    figure.add_trace(

        go.Scatter(

            x=chart_df["date"],

            y=chart_df[
                "model_upper_95"
            ],

            mode="lines",

            line=dict(
                width=0
            ),

            showlegend=False,
        )
    )


    figure.add_trace(

        go.Scatter(

            x=chart_df["date"],

            y=chart_df[
                "model_lower_95"
            ],

            mode="lines",

            fill="tonexty",

            name="95% forecast interval",

            line=dict(
                width=0
            ),
        )
    )


    figure.add_trace(

        go.Scatter(

            x=chart_df["date"],

            y=chart_df[
                "model_pm25_prediction"
            ],

            mode="lines+markers",

            name="Solar Fiji model",
        )
    )


    figure.add_trace(

        go.Scatter(

            x=chart_df["date"],

            y=chart_df[
                "external_cams_pm25_forecast"
            ],

            mode="lines+markers",

            name="External CAMS forecast",
        )
    )


    figure.update_layout(

        title=(
            "Current PM2.5 Outlook"
        ),

        xaxis_title="Date",

        yaxis_title="PM2.5 (µg/m³)",

        hovermode="x unified",

        legend_title="Forecast source",
    )


    st.plotly_chart(

        figure,

        use_container_width=True,
    )


    # --------------------------------------------------------
    # Technical details expander
    # --------------------------------------------------------

    with st.expander(
        "View technical forecast details"
    ):

        technical_columns = [

            "date",

            "forecast_day",

            "forecast_type",

            "model_pm25_prediction",

            "model_lower_95",

            "model_upper_95",

            "model_aqi",

            "model_aqi_category",

            "external_cams_pm25_forecast",

            "external_provider_aqi",

            "available_pm25_hours",

        ]


        technical_columns = [

            column

            for column in technical_columns

            if column
            in forecast_df.columns
        ]


        technical_display = (

            forecast_df[
                technical_columns
            ]

            .copy()
        )


        if (
            "date"
            in technical_display.columns
        ):

            technical_display[
                "date"
            ] = (

                pd.to_datetime(

                    technical_display[
                        "date"
                    ]

                )

                .dt

                .strftime(
                    "%d %b %Y"
                )
            )


        st.dataframe(

            technical_display,

            use_container_width=True,

            hide_index=True,
        )


# ============================================================
# PAGE 2 — HISTORICAL PERFORMANCE
# ============================================================

elif page == "Historical Performance":

    st.title(
        "Historical Forecast Performance"
    )


    st.write(

        """
        The final evaluation used a chronological test period from
        25 February 2024 to 10 July 2024.
        """
    )


    if not model_comparison.empty:

        st.subheader(
            "Model comparison"
        )


        comparison_display = (
            model_comparison.copy()
        )


        for column in [

            "MAE",

            "RMSE",

            "R2",

            "sMAPE_percent",

        ]:

            if column in comparison_display.columns:

                comparison_display[
                    column
                ] = (

                    comparison_display[
                        column
                    ]

                    .round(3)
                )


        st.dataframe(

            comparison_display,

            use_container_width=True,

            hide_index=True,
        )


        rmse_chart = px.bar(

            model_comparison,

            x="Model",

            y="RMSE",

            title=(
                "Test RMSE by Forecasting Model"
            ),
        )


        st.plotly_chart(

            rmse_chart,

            use_container_width=True,
        )


        st.success(

            """
            ARIMAX(1,0,1) achieved the strongest overall regression
            performance, with RMSE 1.745 µg/m³ and a 17.25% improvement
            over the persistence baseline.
            """
        )


    if not historical_predictions.empty:

        st.subheader(
            "Actual versus predicted PM2.5"
        )


        performance_figure = go.Figure()


        performance_figure.add_trace(

            go.Scatter(

                x=historical_predictions[
                    "date"
                ],

                y=historical_predictions[
                    "actual_pm25_ug_m3"
                ],

                mode="lines",

                name="Actual PM2.5",
            )
        )


        performance_figure.add_trace(

            go.Scatter(

                x=historical_predictions[
                    "date"
                ],

                y=historical_predictions[
                    "arimax_prediction"
                ],

                mode="lines",

                name="ARIMAX",
            )
        )


        performance_figure.add_trace(

            go.Scatter(

                x=historical_predictions[
                    "date"
                ],

                y=historical_predictions[
                    "xgboost_prediction"
                ],

                mode="lines",

                name="XGBoost",
            )
        )


        performance_figure.update_layout(

            title=(
                "Historical Test-Period Forecasts"
            ),

            xaxis_title="Date",

            yaxis_title="PM2.5 (µg/m³)",

            hovermode="x unified",
        )


        st.plotly_chart(

            performance_figure,

            use_container_width=True,
        )


    if not aqi_comparison.empty:

        st.subheader(
            "AQI-category performance"
        )


        st.dataframe(

            aqi_comparison.round(3),

            use_container_width=True,

            hide_index=True,
        )


        st.warning(

            """
            Although ARIMAX achieved the lowest PM2.5 forecasting error,
            it failed to identify Moderate AQI days in the small historical
            test sample. XGBoost detected some Moderate days but had slightly
            higher regression error.
            """
        )


# ============================================================
# PAGE 3 — FORECAST DRIVERS
# ============================================================

elif page == "What Affected the Forecast?":

    st.title(
        "What Affected the Forecast?"
    )


    st.write(

        """
        XGBoost is retained as an explanatory companion model.
        Its feature importance helps show which historical and
        environmental variables contributed most strongly to prediction.
        """
    )


    if feature_importance.empty:

        st.warning(
            "Feature-importance data is unavailable."
        )


    else:

        explanatory_df = (
            feature_importance.copy()
        )


        explanatory_df[
            "friendly_name"
        ] = (

            explanatory_df[
                "feature"
            ]

            .apply(
                friendly_feature_name
            )
        )


        top_features = (
            explanatory_df
            .head(10)
            .copy()
        )


        st.subheader(
            "Most influential forecast variables"
        )


        top_columns = st.columns(
            5
        )


        for index in range(
            min(
                5,
                len(
                    top_features
                )
            )
        ):

            with top_columns[
                index
            ]:

                st.metric(

                    top_features.iloc[
                        index
                    ][
                        "friendly_name"
                    ],

                    (
                        f"{top_features.iloc[index]['importance']:.3f}"
                    ),
                )


        chart_data = (

            explanatory_df

            .head(15)

            .sort_values(
                "importance"
            )
        )


        importance_chart = px.bar(

            chart_data,

            x="importance",

            y="friendly_name",

            orientation="h",

            title=(
                "Top 15 XGBoost Forecast Drivers"
            ),

            labels={

                "importance":
                    "Relative importance",

                "friendly_name":
                    "Variable",

            },
        )


        st.plotly_chart(

            importance_chart,

            use_container_width=True,
        )


        st.info(

            """
            The strongest drivers were recent PM2.5 levels and short-term
            pollution trends. Wind speed, temperature, rainfall and expected
            solar radiation also contributed to the model.
            Feature importance indicates predictive contribution, not
            necessarily direct causation.
            """
        )


# ============================================================
# PAGE 4 — SITE REPORTING
# ============================================================

elif page == "Report a Site Condition":

    st.title(
        "Report a Solar Site Condition"
    )


    st.write(

        """
        Local observations can provide context that satellite,
        reanalysis and forecast-model data may not capture.
        """
    )


    site_options = [

        "Suva / Nasinu",

        "Taveuni",

        "Kadavu",

        "Vanua Levu",

        "Rotuma",

        "Lau Group",

        "Yasawa",

        "Rabi Island",

        "Vanuatu",

        "Other",

    ]


    condition_options = [

        "Haze",

        "Smoke",

        "Dust",

        "Salt deposits",

        "Dirty panels",

        "Heavy rain",

        "Strong wind",

        "Cloud cover",

        "Reduced solar generation",

        "No unusual condition",

        "Other",

    ]


    with st.form(
        "site_report_form"
    ):

        site = st.selectbox(

            "Site or region",

            site_options,
        )


        custom_site = st.text_input(

            "Site name, if different"
        )


        observed_date = st.date_input(

            "Observation date"
        )


        conditions = st.multiselect(

            "Observed conditions",

            condition_options,
        )


        generation_issue = st.selectbox(

            "Was reduced solar output observed?",

            [

                "Unknown",

                "No",

                "Yes",

            ],
        )


        notes = st.text_area(

            "Additional notes",

            placeholder=(
                "Example: visible haze in the morning, "
                "dust on panels, output lower than expected..."
            ),
        )


        submitted = st.form_submit_button(

            "Save site report"
        )


    if submitted:

        final_site = (

            custom_site.strip()

            if custom_site.strip()

            else

            site
        )


        new_report = pd.DataFrame(

            [

                {

                    "submitted_at":
                        datetime.now().isoformat(
                            timespec="seconds"
                        ),

                    "observation_date":
                        str(
                            observed_date
                        ),

                    "site":
                        final_site,

                    "conditions":
                        ", ".join(
                            conditions
                        ),

                    "reduced_generation":
                        generation_issue,

                    "notes":
                        notes,

                }

            ]
        )


        if SITE_REPORT_FILE.exists():

            existing_reports = (
                pd.read_csv(
                    SITE_REPORT_FILE
                )
            )


            all_reports = pd.concat(

                [

                    existing_reports,

                    new_report,

                ],

                ignore_index=True,
            )


        else:

            all_reports = (
                new_report
            )


        all_reports.to_csv(

            SITE_REPORT_FILE,

            index=False,
        )


        st.success(
            "Site observation saved."
        )


    if SITE_REPORT_FILE.exists():

        reports = pd.read_csv(
            SITE_REPORT_FILE
        )


        if not reports.empty:

            st.subheader(
                "Recent site observations"
            )


            st.dataframe(

                reports.tail(
                    20
                ),

                use_container_width=True,

                hide_index=True,
            )


# ============================================================
# PAGE 5 — TECHNICAL DETAILS
# ============================================================

elif page == "Technical Details":

    st.title(
        "Technical Details"
    )


    st.subheader(
        "Production forecasting model"
    )


    st.write(
        "**Selected model:** ARIMAX(1,0,1)"
    )


    st.write(
        "**Primary forecast horizon:** One day ahead"
    )


    st.write(
        "**Test RMSE:** 1.745 µg/m³"
    )


    st.write(
        "**Test MAE:** 1.368 µg/m³"
    )


    st.write(
        "**Test R²:** 0.390"
    )


    st.write(
        "**Improvement over persistence:** 17.25%"
    )


    st.subheader(
        "Model inputs"
    )


    st.write(

        """
        The ARIMAX model uses forecast-day environmental variables including:

        - temperature
        - humidity
        - rainfall
        - wind speed and direction
        - surface pressure
        - expected shortwave solar radiation
        - seasonal timing variables

        The ARIMA component represents temporal dependence in PM2.5.
        """
    )


    st.subheader(
        "Current operational workflow"
    )


    st.code(

        """
Recent CAMS-based PM2.5 history
            +
Recent GFS weather
            ↓
Update current ARIMAX model state
            +
Forecast-day GFS weather
            ↓
Current PM2.5 forecast
            ↓
AQI interpretation
            ↓
Solar Fiji operational guidance
        """
    )


    st.subheader(
        "Important limitations"
    )


    st.warning(

        """
        1. The original historical PM2.5 target series was derived from
        CAMS EAC4, while current PM2.5 state information comes from an
        operational CAMS-based forecast feed.

        2. The model has been validated primarily for one-day-ahead prediction.
        Multi-day forecasts should be treated as planning guidance.

        3. Historical air quality was dominated by Good days, so performance
        on less common Moderate or poorer air-quality conditions is uncertain.

        4. The dashboard estimates environmental operating conditions.
        It does not directly predict solar-panel power loss because measured
        site-level generation data were not available for model training.

        5. Feature importance represents predictive association and should
        not automatically be interpreted as causation.
        """
    )


    if not model_comparison.empty:

        st.subheader(
            "Full model comparison"
        )


        st.dataframe(

            model_comparison.round(3),

            use_container_width=True,

            hide_index=True,
        )


# ============================================================
# PAGE 6 — ABOUT
# ============================================================

elif page == "About the Prototype":

    st.title(
        "About the Solar Fiji Environmental Forecast Prototype"
    )


    st.write(

        """
        This prototype was developed as a decision-support concept for
        Solar Fiji.

        It combines air-quality information, environmental forecasting
        and machine-learning analysis to help teams anticipate conditions
        that may affect solar operations, maintenance planning and
        field observations.
        """
    )


    st.subheader(
        "What makes the approach useful?"
    )


    st.write(

        """
        Rather than presenting a technical pollution forecast alone,
        the prototype translates environmental information into
        practical operational guidance.

        It also combines three forms of information:

        **1. Predictive modelling**  
        A locally developed ARIMAX forecasting model.

        **2. External operational comparison**  
        A CAMS-based PM2.5 forecast used as an additional reference.

        **3. Local observations**  
        Technician and site reports capturing smoke, haze, dust,
        panel deposits and unusual operating conditions.
        """
    )


    st.subheader(
        "Fiji-focused design"
    )


    st.write(

        """
        The interface prioritises plain-language recommendations,
        mobile-friendly summaries and local site reporting.

        The current pilot focuses on Suva and Nasinu, while the concept
        could later be expanded to remote Solar Fiji installations across
        Fiji and the wider Pacific.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(

    """
    <div class="footer">

    Solar Fiji Environmental Forecast Prototype ·
    Research and decision-support demonstration

    </div>
    """,

    unsafe_allow_html=True,
)
