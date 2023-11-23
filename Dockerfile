FROM python:3.9
ENV PYTHONUNBUFFERED=1

COPY . . 
RUN pip install -r requirements.txt
RUN shasum dataset_netflix.csv
 
WORKDIR /code
