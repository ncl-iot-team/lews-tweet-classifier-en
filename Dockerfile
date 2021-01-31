FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "tweet-classifier-en.py"]