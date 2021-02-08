FROM python:3.9-buster
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["run.py" ]
