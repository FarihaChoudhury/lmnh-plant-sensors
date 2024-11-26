FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY clean_plant_info.csv .

COPY load.py .

CMD ["python", "load.py"]
