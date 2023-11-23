# python-test-fastapi
# FastAPI Dashboard

## Overview

This FastAPI application creates an interactive and informative dashboard from a Netflix dataset (`dataset_netflix.csv`). The dashboard presents insightful visualizations and analytics derived from the dataset, providing a clear and comprehensive understanding of its contents.

## Features

- **Random Data Streaming**: The application streams random data to simulate real-time updates. This feature is accessible through the `/chart-data` endpoint.

- **Movie Ratings Distribution Chart**: The application reads the Netflix dataset, extracts movie titles and ratings, and generates a bar chart using Plotly. The chart is saved as an HTML file (`movie_ratings_bar_chart.html`) and displayed through the `/load-chart` endpoint.

## Getting Started

## Clone the repository.

   ```bash
   git clone <repository-url>
Install the required dependencies.

bash
Copy code
pip install -r requirements.txt
Run the FastAPI application.

bash
Copy code
python <filename>.py
Access the main dashboard at http://localhost:8000.

##Endpoints
Main Dashboard: http://localhost:8000

Streaming Random Data: http://localhost:8000/chart-data

Movie Ratings Distribution Chart: http://localhost:8000/load-chart

###Dependencies
fastapi
uvicorn
plotly
