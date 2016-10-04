FROM centos:7
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN yum install -y yum-utils rpmdevtools make
COPY / /yrmcds-rpm
WORKDIR /yrmcds-rpm

RUN yum-builddep -y ./yrmcds.spec
RUN make rpm
RUN yum install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/yrmcds-[^d.+].*
RUN /usr/bin/install -o nobody -g nobody -m 0700 -d /var/tmp/yrmcds && /bin/rm -f /var/tmp/yrmcds/*

EXPOSE 11211

CMD ["-f", "/etc/yrmcds/yrmcds.conf"]
ENTRYPOINT ["/usr/sbin/yrmcdsd"]
