FROM python:3.8
RUN mkdir -p app/bot
WORKDIR /app/bot
COPY requirements.txt .
COPY main.py .
COPY config.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]

