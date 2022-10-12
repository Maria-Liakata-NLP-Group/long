FROM python:3.8-slim-buster
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
#Server will reload itself on file changes if in dev mode
ENV FLASK_DEBUG=True
# ENV FLASK_ENV=development
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["flask", "run"]
