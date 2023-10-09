FROM python:3.11.1
COPY src/ /app/
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
