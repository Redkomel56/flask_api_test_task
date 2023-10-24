FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENV PORT=5000
ENV EMAIL=''
ENV DB_URI=''
ENV SMTP_HOST=''
ENV SMTP_PORT=465
ENV SMTP_LOGIN=''
ENV SMTP_PASSWORD=''
ENV SMTP_EMAIL=''
ENV SMTP_NAME=''

CMD ["python3", "app.py"]
