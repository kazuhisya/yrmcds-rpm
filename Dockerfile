FROM centos:7
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN yum install -y yum-utils rpmdevtools make git epel-release
RUN git clone --depth=1 https://github.com/kazuhisya/yrmcds-rpm.git

WORKDIR /yrmcds-rpm
RUN yum-builddep -y ./yrmcds.spec
RUN make rpm
RUN yum install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/yrmcds-*.rpm
RUN /usr/bin/install -o root -g root -m 0700 -d /var/tmp/yrmcds && /bin/rm -f /var/tmp/yrmcds/*
CMD ["yrmcdsd", "-v"]
