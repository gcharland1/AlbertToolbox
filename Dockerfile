FROM python:3.9-buster
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py" ]
