FROM python:3.9

# RUN apt-get install wget
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install pandas sqlalchemy psycopg2 pyarrow fastparquet

WORKDIR /app
COPY ingest_data.py ingest_data.py
ENTRYPOINT [ "python", "ingest_data.py" ]

# C:\Users\USER\Desktop\DataEngineeringZoomCamp\week1\vsfiles\ingest-data.py