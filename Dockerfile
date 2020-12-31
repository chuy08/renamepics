FROM python:3.8-slim

COPY requirements.txt /requirements.txt
COPY dist/sortpics-0.0.1.tar.gz /sortpics-0.0.1.tar.gz
COPY exiftool_12.13-1_amd64.deb /exiftool_12.13-1_amd64.deb

RUN dpkg -i /exiftool_12.13-1_amd64.deb
RUN pip install -r requirements.txt
RUN pip install /sortpics-0.0.1.tar.gz
RUN rm -rf /sortpics-0.0.1.tar.gz
RUN rm -rf /exiftool_12.13-1_amd64.deb

ENTRYPOINT [ "sortpics" ]
