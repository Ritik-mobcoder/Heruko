FROM python:3.8.10-slim

WORKDIR /HERUKO

COPY . /HERUKO
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
