FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update; apt-get install -y graphviz
RUN pip install -r requirements.txt

COPY . .

CMD [ "streamlit", "run", "main.py"]
