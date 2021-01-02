FROM python:3.8

RUN mkdir -p /usr/src/coach_bot
WORKDIR /usr/src/coach_bot
COPY . /usr/src/coach_bot

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "bot_main.py"]