# mminderbinder/passcheck
FROM mminderbinder/python
MAINTAINER Milo Minderbinder <minderbinder.enterprises@gmail.com>


RUN mkdir /etc/service/passcheck
COPY passcheck-run.sh /etc/service/passcheck/run
RUN chmod +x /etc/service/passcheck/run

WORKDIR /opt/passcheck
COPY requirements.txt /opt/passcheck/requirements.txt
RUN pip install -r requirements.txt

COPY passcheck /opt/passcheck/

EXPOSE 5000

# Clean up APT when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
CMD ["/sbin/my_init"]
