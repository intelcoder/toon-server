FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /code/log
RUN touch /code/log/cronjob.log

WORKDIR /code
ADD . /code


RUN cd /code
RUN apt-get update 
RUN apt-get install -y apt-utils python3 python3-pip 
RUN pip3 install -r requirements.txt

RUN apt-get install -y wget xvfb cron vim rsyslog
RUN cd /usr/local/share && wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN cd /usr/local/share && tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/share/phantomjs
RUN ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
RUN ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
RUN cd /code/webtoon
RUN ls /etc

