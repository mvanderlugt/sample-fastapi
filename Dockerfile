FROM python:3.7-stretch

EXPOSE 80

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
