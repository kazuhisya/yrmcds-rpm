#  yrmcds RPM spec

[![Circle CI](https://circleci.com/gh/kazuhisya/yrmcds-rpm/tree/master.svg?style=shield)](https://circleci.com/gh/kazuhisya/yrmcds-rpm/tree/master)

This repository provides unofficial rpmbuild scripts for Red Hat Enterprise Linux and Fedora.

- yrmcds - memcached compatible KVS with master/slave replication. http://cybozu.github.io/yrmcds/


## Distro support

Tested working on:

- RHEL/CentOS 7 x86_64
    - When you try to build on el7, must enable the EPEL repository.
- Fedora 22, 23, 24 x86_64

Prerequisites:

- `gcc` and `g++` 4.8.1 or newer

## Compiled Package


- You can find prebuilt rpm binary from here(el7 and fc22, 23, 24)
    - [FedoraCopr khara/yrmcds Copr](https://copr.fedoraproject.org/coprs/khara/yrmcds/)



el7:

```bash
$ sudo curl -sL -o /etc/yum.repos.d/khara-yrmcds.repo https://copr.fedoraproject.org/coprs/khara/yrmcds/repo/epel-7/khara-yrmcds-epel-7.repo
$ sudo yum install -y yrmcds
```

fc23:

```bash
$ sudo dnf copr enable khara/yrmcds
$ sudo dnf install -y yrmcds
```

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

## Disclaimer

- This repository and all files that are included in this, there is no relationship at all with the upstream and vendor.
