FROM python:3.8.5

RUN pip3 install pipenv

RUN mkdir /opt/project
WORKDIR /opt/project

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install

COPY . /opt/project
