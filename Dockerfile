FROM python:3.7-alpine

RUN pip install tweepy pyowm pytz

WORKDIR /bots
COPY . .
CMD ["python", "main.py"]