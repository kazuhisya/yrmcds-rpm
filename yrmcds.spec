Name:          yrmcds
Version:       1.1.4
Release:       1%{?dist}
Summary:       memcached compatible KVS with master/slave replication.
Group:         Development/Libraries
License:       BSD-2-clause
URL:           http://cybozu.github.io/yrmcds/
Source0:       https://github.com/cybozu/%{name}/archive/v%{version}.tar.gz
Source1:       yrmcds.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
Prefix:        /usr
Requires:      libevent
BuildRequires: systemd-units
BuildRequires: libevent-devel
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: libatomic
BuildRequires: gperftools-libs
BuildRequires: gperftools-devel
Patch0:        yrmcds-change-user-and-group.patch


%description
yrmcds is a memory object caching system with master/slave replication.

Currently, yrmcds supports two protocols: the first is an enhanced memcached, and another is a protocol to implement distributed resource counters.

Since the memcached protocol is perfectly compatible with the original implementation, yrmcds can be used as a drop-in replacement for memcached. Thanks to its virtual-IP based replication system, existing applications can obtain high-available memcached-compatible service without any modifications.


%prep
rm -rf $RPM_SOURCE_DIR/%{name}-%{version}

%setup -q -n %{name}-%{version}
%patch0 -p1
make PREFIX=%{prefix} DEFAULT_CONFIG=/etc/%{name}/%{name}.conf


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system
mkdir -p $RPM_BUILD_ROOT/etc/%{name}
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT/var/log

cp -pf $RPM_BUILD_DIR/%{name}-%{version}/etc/logrotate $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/etc/%{name}.conf $RPM_BUILD_ROOT/etc/%{name}/
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/%{name}d $RPM_BUILD_ROOT/usr/sbin/

for file in ChangeLog COPYING COPYING.hpp README.md ; do
    cp -pf $RPM_BUILD_DIR/%{name}-%{version}/$file $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/
done
cp -Rpf $RPM_BUILD_DIR/%{name}-%{version}/docs $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/
cp -Rpf %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/systemd/system/%{name}.service
touch $RPM_BUILD_ROOT/var/log/%{name}.log


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_defaultdocdir}/%{name}-%{version}
%{_sysconfdir}/%{name}
%{_sysconfdir}/logrotate.d
%defattr(755,root,root)
%{_sbindir}/%{name}d
%defattr(644,root,root)
%{_unitdir}/%{name}.service
/var/log/%{name}.log


%changelog
* Sat Sep 26 2015 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.4-1
- init
