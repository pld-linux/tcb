#
# TODO
# - Integrate crypt_blowfish into glibc (or an external lib?)
# - Depend on the new glibc or external lib
#
Summary:	The alternative to shadow
Summary(pl.UTF-8):	Alternatywa dla shadow
Name:		tcb
Version:	1.1
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.openwall.com/tcb/%{name}-%{version}.tar.gz
# Source0-md5:	b4ac25f22fd3bdc9eb32ff6f97f022cd
Patch0:		%{name}-make.patch
URL:		http://www.openwall.com/tcb/
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tcb package contains core components of tcb suite implementing the
alternative password shadowing scheme on Owl. It is being made
available separately from Owl primarily for use by other
distributions.

%description -l pl.UTF-8
Pakiet tcb zawiera główne komponenty zestawu tcb implementującego
alternatywny schemat ukrywania haseł w systemie Owl. Jest dostępny
oddzielnie głównie do wykorzystania przez inne dystrybucje.

%package devel
Summary:	Headers for libtcb
Summary(pl.UTF-8):	Pliki nagłówkowe libtcb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers for libtcb.

%description devel -l pl.UTF-8
Pliki nagłówkowe libtcb.

%package static
Summary:	Static library for libtcb
Summary(pl.UTF-8):	Biblioteka statyczna libtcb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static library for libtcb.

%description static -l pl.UTF-8
Biblioteka statyczna libtcb.

%package -n pam-pam_tcb
Summary:	TCB module for PAM
Summary(pl.UTF-8):	Moduł TCB dla PAM
Group:		Base

%description -n pam-pam_tcb
The alternative to shadow (TCB) PAM module.

%description -n pam-pam_tcb -l pl.UTF-8
Alternatywny dla shadow (TCB) moduł PAM.

%package -n nss_tcb
Summary:	TCB library for NSS
Summary(pl.UTF-8):	Biblioteka TCB dla NSS
Group:		Base

%description -n nss_tcb
nss_tcb is a C library extension (NSS module) which allows TCB service
to be used as a primary source of aliases, ethers, groups, hosts,
networks, protocols, users, RPCs, services and shadow passwords
(instead of or in addition to using flat files or NIS).

%description -n nss_tcb -l pl.UTF-8
nss_tcb to biblioteka rozszerzenia (moduł NSS) pozwalający na używanie
usługi TCB jako głównego źródła aliasów (aliases), adresów kart
sieciowych (ethers), grup (group), hostów (hosts), sieci (networks),
protokołów (protocols), użytkowników (passwd), RPC, usług (services) i
ukrytych haseł (shadow) zamiast płaskich plików lub NIS.

%prep
%setup -q
%patch -P0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	DBGFLAG="%{rpmcflags} %{rpmldflags}" \
	SBINDIR=/sbin \
	SLIBDIR=/%{_lib} \
	LIBDIR=%{_libdir} \
	LIBEXECDIR=%{_libexecdir} \
	MANDIR=%{_mandir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SLIBDIR=/%{_lib} \
	LIBDIR=%{_libdir} \
	LIBEXECDIR=%{_libexecdir} \
	MANDIR=%{_mandir}

%{__mv} $RPM_BUILD_ROOT%{_libexecdir}/chkpwd/tcb_chkpwd $RPM_BUILD_ROOT/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 286 -r -f shadow

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%groupremove shadow
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libtcb.so.0.9.8
%attr(755,root,root) %ghost /%{_lib}/libtcb.so.0
%attr(755,root,root) /sbin/tcb_convert
%attr(755,root,root) /sbin/tcb_unconvert
%attr(755,root,root) /sbin/tcb_chkpwd
%{_mandir}/man5/tcb.5*
%{_mandir}/man8/tcb_convert.8*
%{_mandir}/man8/tcb_unconvert.8

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtcb.so
%{_includedir}/tcb.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtcb.a

%files -n nss_tcb
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_tcb.so.2

%files -n pam-pam_tcb
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_tcb.so
%{_mandir}/man8/pam_tcb.8*
