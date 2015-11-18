FROM centos:7
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN yum install -y yum-utils rpmdevtools make git epel-release
COPY / /yrmcds-rpm
WORKDIR /yrmcds-rpm

RUN yum-builddep -y ./yrmcds.spec
RUN make rpm
RUN yum install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/yrmcds-[^d.+].*
RUN /usr/bin/install -o root -g root -m 0700 -d /var/tmp/yrmcds && /bin/rm -f /var/tmp/yrmcds/*
CMD ["yrmcdsd", "-v"]