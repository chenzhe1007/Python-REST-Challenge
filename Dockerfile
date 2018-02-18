FROM python:3
ADD . /restful_challenge
WORKDIR /restful_challenge
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","server.py", "5000", "people_input.csv"]
