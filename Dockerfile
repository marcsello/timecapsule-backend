FROM python:3

ADD timecapsule requirements.txt /timecapsule/
WORKDIR /timecapsule/

RUN pip3 install -r requirements.txt && pip3 install gunicorn

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]

