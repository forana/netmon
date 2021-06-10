FROM python:3-alpine
RUN mkdir /netmon
WORKDIR /netmon
COPY ./netmon.py /netmon/netmon.py
CMD ["python3", "/netmon/netmon.py"]
