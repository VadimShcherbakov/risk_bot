FROM python:3.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8000:8000

COPY . .

CMD [ "python", "./bot.py" ]