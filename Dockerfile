FROM python:3.9.15-slim

COPY . /bot
WORKDIR /bot

RUN pip install -r requirements.txt

CMD [ "python", "bot.py" ]