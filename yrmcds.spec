Name:          yrmcds
Version:       1.1.6
Release:       2%{?dist}
Summary:       memcached compatible KVS with master/slave replication.
Group:         Development/Libraries
License:       BSD-2-clause
URL:           http://cybozu.github.io/yrmcds/
Source0:       https://github.com/cybozu/%{name}/archive/v%{version}.tar.gz
Source1:       yrmcds.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
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
%setup -q -n %{name}-%{version}
%patch0 -p1


%build
make PREFIX=%{_prefix} DEFAULT_CONFIG=/etc/%{name}/%{name}.conf %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/examples
mkdir -p $RPM_BUILD_ROOT%{_var}/log

cp -pf $RPM_BUILD_DIR/%{name}-%{version}/etc/logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/etc/%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
cp -Rpf $RPM_BUILD_DIR/%{name}-%{version}/etc/keepalived.conf $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/examples/
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/%{name}d $RPM_BUILD_ROOT%{_sbindir}

for file in ChangeLog COPYING COPYING.hpp README.md ; do
    cp -pf $RPM_BUILD_DIR/%{name}-%{version}/$file $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
done
cp -Rpf $RPM_BUILD_DIR/%{name}-%{version}/docs $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/
cp -Rpf %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
touch $RPM_BUILD_ROOT%{_var}/log/%{name}.log


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_defaultdocdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/logrotate.d
%defattr(755,root,root)
%{_sbindir}/%{name}d
%defattr(644,root,root)
%{_unitdir}/%{name}.service
/var/log/%{name}.log


%changelog
* Tue Feb 16 2016 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.6-2
- Add example keepalived.conf
- Explicitly declare "noreplace"
* Thu Jan 28 2016 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.6-1
- Updated version to 1.1.6
* Tue Nov 17 2015 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.5-1
- Updated version to 1.1.5
* Mon Sep 28 2015 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.4-2
- Improved in order to conform to rpmlint syntax check
* Sat Sep 26 2015 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.4-1
- init
