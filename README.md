#  yrmcds RPM spec

This repository provides unofficial rpmbuild scripts for Red Hat Enterprise Linux and Fedora.

- yrmcds - memcached compatible KVS with master/slave replication. http://cybozu.github.io/yrmcds/


## Distro support

Tested working on:

- RHEL/CentOS 7 x86_64
    - When you try to build on el7, must enable the EPEL repository.
- Fedora 22 x86_64
    - This spec is tested under el7 only.
    - However, Fedora22 or later work. maybe.

Prerequisites:

- `gcc` and `g++` 4.8.1 or newer


## Build

setting up:

```bash
$ sudo yum install -y yum-utils rpmdevtools make
```

git clone and make:

```bash
$ git clone https://github.com/kazuhisya/yrmcds-rpm.git
$ cd yrmcds-rpm
$ sudo yum-builddep ./yrmcds.spec
```

```bash
$ make rpm
$ cd ./dist/RPMS/x86_64/
$ sudo yum install ./yrmcds-X.X.X-X.el7.x86_64.rpm --nogpgcheck
```

# Disclaimer

- This repository and all files that are included in this, there is no relationship at all with the upstream and vendor.
