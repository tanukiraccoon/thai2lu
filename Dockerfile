FROM python:3.9.0-slim
WORKDIR /code 
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY / .
CMD ["python", "app.py"]