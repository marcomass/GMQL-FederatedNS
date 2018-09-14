FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD NameServer ./

RUN pip install django djangorestframework markdown django-filter djangorestframework-xml 

RUN apt-get update && apt-get install -y \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

EXPOSE 8800
RUN pwd
RUN ls .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8800"]
