FROM	alpine:3.9

RUN	apk --no-cache update  \
	&& apk add --no-cache \
	   rsyslog \
	   rsyslog-elasticsearch \
	   rsyslog-imrelp \
	   rsyslog-mmjsonparse \
	   rsyslog-mmutf8fix \
	   rsyslog-omrelp \
	   python3 \
	   py3-requests

RUN \
    echo "" >> /etc/rsyslog.conf && \
    echo "module(load=\"imudp\")" >> /etc/rsyslog.conf && \
    echo "input(type=\"imudp\" port=\"514\" ruleset=\"apple_airport\")" >> /etc/rsyslog.conf && \
    echo "module(load=\"omprog\")" >> /etc/rsyslog.conf && \
    echo "ruleset(name=\"apple_airport\"){" >> /etc/rsyslog.conf && \
    echo "action(type=\"omprog\" binary=\"/opt/apple_airport.py\")" >> /etc/rsyslog.conf && \
    echo "}" >> /etc/rsyslog.conf

COPY apple_airport.py /opt/apple_airport.py

RUN chmod +x /opt/apple_airport.py

CMD ["/usr/sbin/rsyslogd","-n", "-d"]

EXPOSE 514/udp