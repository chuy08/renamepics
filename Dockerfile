FROM python:3.8-slim

COPY dist/sortpics-0.0.1.tar.gz /sortpics-0.0.1.tar.gz
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN pip install /sortpics-0.0.1.tar.gz

ENTRYPOINT [ "sortpics" ]
