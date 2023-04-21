FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /flexwire

RUN mkdir /flexwire/static && mkdir /flexwire/media

COPY . /flexwire

RUN pip install -r /flexwire/requirements/requirements.txt
RUN pip install -r /flexwire/requirements/requirements_dev.txt
RUN pip install -r /flexwire/requirements/requirements_test.txt

EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]