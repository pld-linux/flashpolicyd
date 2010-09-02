%define		plugin	check_flashpolicyd
Summary:	Daemon to serve Adobe Flash socket policy XML
Name:		flashpolicyd
Version:	2.1
Release:	5
License:	GPL v2
Group:		Networking/Daemons
URL:		http://code.google.com/p/flashpolicyd/
Source0:	http://flashpolicyd.googlecode.com/files/%{name}-%{version}.tgz
# Source0-md5:	0ad1ed0b130cf5850d77600fab90a7c2
Source1:	%{name}.init
Patch0:		%{name}-runas-user.patch
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	ruby-modules
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	ruby-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pluginconf	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Daemon to serve Adobe Flash socket policy XML.

%package rdoc
Summary:	Documentation files for flashpolicyd
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
Documentation files for flashpolicyd.

%package ri
Summary:	ri documentation for flashpolicyd
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla flashpolicyd
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for flashpolicyd.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla flashpolicyd.

%package -n nagios-plugin-%{plugin}
Summary:	Nagios plugin to check flashpolicyd
Group:		Networking
Requires:	nagios-common

%description -n nagios-plugin-%{plugin}
Nagios plugin to check flashpolicyd.

%prep
%setup -q
%patch0 -p1
# we regenerate rdoc our own
rm -rf doc

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} --host $HOSTADDRESS$ $ARG1$
}

define service {
	use                     generic-service
	name                    flashpolicyd
	service_description     flashpolicyd
	register                0

	normal_check_interval   5
	retry_check_interval    1

	check_command           check_flashpolicyd
}
EOF

%build
rdoc --ri --op ri --title 'Flash Policy Daemon version %{version}' flashpolicyd.rb check_flashpolicyd.rb
rdoc --op rdoc --title 'Flash Policy Daemon version %{version}' flashpolicyd.rb check_flashpolicyd.rb
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_sbindir}}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/flashpolicyd
install -p flashpolicyd.rb $RPM_BUILD_ROOT%{_sbindir}/flashpolicyd
cp -a flashpolicy.xml $RPM_BUILD_ROOT%{_sysconfdir}/flashpolicy.xml

# rdoc/ri
install -d $RPM_BUILD_ROOT{%{ruby_ridir},%{ruby_rdocdir}}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}

install -d $RPM_BUILD_ROOT{%{pluginconf},%{plugindir}}
cp -a nagios.cfg $RPM_BUILD_ROOT%{pluginconf}/%{plugin}.cfg
install -p %{plugin}.rb $RPM_BUILD_ROOT%{plugindir}/%{plugin}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add flashpolicyd
%service flashpolicyd restart

%preun
if [ "$1" = 0 ] ; then
	%service flashpolicyd stop
	/sbin/chkconfig --del flashpolicyd
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/flashpolicy.xml
%attr(754,root,root) /etc/rc.d/init.d/flashpolicyd
%attr(755,root,root) %{_sbindir}/flashpolicyd

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/PolicyServer

%files -n nagios-plugin-%{plugin}
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{pluginconf}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
