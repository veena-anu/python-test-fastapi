import csv
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response
import asyncio
import json
import logging
import random
from datetime import datetime
from typing import Iterator
from plotly import graph_objects as go

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
random.seed()  


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


async def generate_random_data(request: Request) -> Iterator[str]:
    """
    Generates random value between 0 and 100
    :return: String containing the current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    client_ip = request.client.host

    logger.info("Client %s connected", client_ip)

    while True:
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "value": random.random() * 100,
            }
        )
        yield f"data:{json_data}\n\n"
        await asyncio.sleep(1)


@app.get("/chart-data")
async def chart_data(request: Request) -> StreamingResponse:
    response = StreamingResponse(generate_random_data(request), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


def load_data_from_file(filename: str) -> Iterator[str]:
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
      
        next(reader, None)
        for row in reader:
           
            if row[1].replace('.', '', 1).isdigit():
                yield row

@app.get("/load-chart")
async def load_chart() -> HTMLResponse:
    dataset = load_data_from_file("dataset_netflix.csv")

    
    movie_titles = []
    ratings = []

    for row in dataset:
        movie_title = row[0]
        rating = float(row[1])

        movie_titles.append(movie_title)
        ratings.append(rating)

    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ratings,
        y=movie_titles,
        orientation='h',
        marker_color='skyblue',
    ))

    fig.update_layout(
        title='Movie Ratings Distribution',
        xaxis_title='Rating',
        yaxis_title='Movie Title',
        yaxis_autorange='reversed',  
        xaxis=dict(tickvals=list(range(11))),  
        margin=dict(l=0, r=0, b=0, t=40),
    )

    
    fig.write_html('movie_ratings_bar_chart.html')

    
    with open('movie_ratings_bar_chart.html', 'r', encoding='utf-8') as f:
        html_data = f.read()
        response = HTMLResponse(content=html_data, status_code=200)
        return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
