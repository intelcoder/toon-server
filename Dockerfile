FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /code/log
RUN touch /code/log/cronjob.log

WORKDIR /code
ADD . /code


RUN cd /code
RUN apt-get update 
RUN apt-get install -y apt-utils python3 python3-pip wget  xvfb cron vim rsyslog
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -y google-chrome-stable

RUN cd /usr/local/share && wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN cd /usr/local/share && tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/share/phantomjs
RUN ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
RUN ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
RUN cd /code/webtoon
RUN pip3 install -r requirements.txt
RUN ls /etc

COPY ./cron.txt /etc/cron.d
RUN crontab /etc/cron.d/cron.txt
RUN /etc/init.d/cron start
RUN cron
