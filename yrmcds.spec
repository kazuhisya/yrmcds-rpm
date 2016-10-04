Name:          yrmcds
Version:       1.1.8
Release:       1%{?dist}
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
Patch0:        yrmcds-change-group.patch
Patch1:        yrmcds-systemd-service.patch


%description
yrmcds is a memory object caching system with master/slave replication.
Currently, yrmcds supports two protocols: the first is an enhanced memcached, and another is a protocol to implement distributed resource counters.
Since the memcached protocol is perfectly compatible with the original implementation, yrmcds can be used as a drop-in replacement for memcached. Thanks to its virtual-IP based replication system, existing applications can obtain high-available memcached-compatible service without any modifications.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1


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
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/etc/%{name}.service $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/etc/%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
cp -Rpf $RPM_BUILD_DIR/%{name}-%{version}/etc/keepalived.conf $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/examples/
cp -pf $RPM_BUILD_DIR/%{name}-%{version}/%{name}d $RPM_BUILD_ROOT%{_sbindir}

for file in ChangeLog COPYING COPYING.hpp README.md ; do
    cp -pf $RPM_BUILD_DIR/%{name}-%{version}/$file $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
done
cp -Rpf $RPM_BUILD_DIR/%{name}-%{version}/docs $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/
touch $RPM_BUILD_ROOT%{_var}/log/%{name}.log
install -o nobody -g nobody -m 644 /dev/null /var/log/yrmcds.log


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
%defattr(644,nobody,nobody)
/var/log/%{name}.log


# only upgrade job.
# In previous releases, yrmcds using root user, now it makes use of nobody user.
%pre
if [ $1 -eq 2 ]; then
  /usr/bin/chown -R nobody:nobody /var/tmp/%{name} >/dev/null 2>&1 ||:
  /usr/bin/chown -R nobody:nobody /var/log/%{name}.log >/dev/null 2>&1 ||:
fi

# Register the yrmcds service
%post
if [ $1 -eq 1 ]; then
  /usr/bin/systemctl preset %{name}.service >/dev/null 2>&1 ||:
fi
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
/usr/bin/install -o nobody -g nobody -m 0700 -d /var/tmp/%{name} >/dev/null 2>&1 ||:

%postun
if [ $1 -eq 0 ]; then
  /usr/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 ||:
  /usr/bin/systemctl stop %{name}.service >/dev/null 2>&1 ||:
  /usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
fi


%changelog
* Tue Oct  4 2016 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.8-1
- In previous releases, yrmcds using root user, now it makes use of nobody user.
- Updated version to 1.1.8
* Mon Oct  3 2016 Kazuhisa Hara <kazuhisya@gmail.com>  - 1.1.7-1
- Updated version to 1.1.7
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
