#FROM python:3.7.7-slim-buster
FROM api_gateway_base:latest

ADD . /APIGateway
WORKDIR /APIGateway

#RUN pip install --no-cache-dir --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
