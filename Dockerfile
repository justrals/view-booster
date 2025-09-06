FROM python:3.9-slim

WORKDIR /view-booster

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install-deps

RUN playwright install

CMD ["python", "./main.py"]