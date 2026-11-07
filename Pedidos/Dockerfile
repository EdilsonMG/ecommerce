FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=300 -r requirements.txt

EXPOSE 5000

COPY . .

CMD [ "python", "app.py" ]