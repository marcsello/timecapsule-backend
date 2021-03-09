FROM python:3

ADD timecapsule requirements.txt /timecapsule/
WORKDIR /timecapsule/

RUN pip3 install -r requirements.txt && pip3 install gunicorn

ARG RELEASE_ID
ENV RELEASE_ID ${RELEASE_ID:-""}

EXPOSE 8000
CMD ["gunicorn", "-t", "7200", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]

