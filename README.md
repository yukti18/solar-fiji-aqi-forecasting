# Solar Fiji Environmental Forecast Prototype

An AI-based environmental forecasting and decision-support prototype
developed for Solar Fiji as part of Think Pacific Action Project 57-15.

## Project Overview

This project explores how environmental data and machine-learning
forecasting can be used to predict short-term PM2.5 air-quality
conditions and provide practical environmental information for
solar-energy operations.

The prototype combines:

- PM2.5 air-quality forecasting
- GFS weather data
- ARIMAX time-series modelling
- XGBoost machine learning
- AQI interpretation
- External CAMS forecast comparison
- Forecast uncertainty
- Local solar-site observations
- An interactive Streamlit dashboard

## Key Result

The selected ARIMAX(1,0,1) model achieved a test RMSE of
1.745 µg/m³, improving upon the persistence baseline by 17.25%.

## Important Limitation

The prototype does not directly predict solar-energy loss because
site-level Solar Fiji generation data were not available. It should
be considered an environmental decision-support prototype rather
than an automated operational system.
