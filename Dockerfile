FROM python:3.10 as builder

COPY ./requirements.txt /tmp/

RUN pip install -i "https://mirrors.aliyun.com/pypi/simple/" -r /tmp/requirements.txt


FROM builder

ENV PYTHONUNBUFFERED=TRUE
EXPOSE 80

RUN cvd config set --dbdir /clamav \
    && mkdir -p /opt/clamav-mirror

WORKDIR /opt/clamav-mirror

COPY mirror.py /opt/clamav-mirror

CMD python mirror.py