Summary:	Daemon to serve Adobe Flash socket policy XML
Name:		flashpolicyd
Version:	2.1
Release:	0.1
License:	GPL v2
Group:		Applications/System
URL:		http://code.google.com/p/flashpolicyd/
Source0:	http://flashpolicyd.googlecode.com/files/%{name}-%{version}.tgz
# Source0-md5:	0ad1ed0b130cf5850d77600fab90a7c2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	ruby
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Daemon to serve Adobe Flash socket policy XML.

%prep
%setup -q
mv doc rdoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir}}
install -d $RPM_BUILD_ROOT
install -p flashpolicyd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/flashpolicyd
install -p flashpolicyd.rb $RPM_BUILD_ROOT%{_sbindir}/flashpolicyd
cp -a flashpolicy.xml $RPM_BUILD_ROOT%{_sysconfdir}/flashpolicy.xml

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
%doc README check_flashpolicyd.rb
%doc rdoc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/flashpolicy.xml
%attr(754,root,root) /etc/rc.d/init.d/flashpolicyd
%attr(755,root,root) %{_sbindir}/flashpolicyd
