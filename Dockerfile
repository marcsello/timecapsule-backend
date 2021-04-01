FROM python:3.9

ADD timecapsule requirements.txt /timecapsule/
WORKDIR /timecapsule/

RUN pip3 install -r requirements.txt && pip3 install gunicorn

ARG RELEASE_ID
ENV RELEASE_ID ${RELEASE_ID:-""}

EXPOSE 8000
USER www-data
CMD ["gunicorn", "-t", "28800", "--threads", "4", "-b", "0.0.0.0:8000", "app:app"]

