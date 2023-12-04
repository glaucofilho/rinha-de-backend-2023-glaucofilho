FROM python:3.11.1
COPY src/ /app/
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN find /app -type d -name __pycache__ -exec rm -r {} +
# CMD ["python", "run_api.py"]
