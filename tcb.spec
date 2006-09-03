#
# TODO
# - Integrate crypt_blowfish into glibc (or an external lib?)
# - Depend on the new glibc or external lib
#
Summary:	the alternative to shadow
Name:		tcb
Version:	1.0
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.openwall.com/tcb/%{name}-%{version}.tar.gz
# Source0-md5:	9cf36b80cafdae41e644000a6e3b88fc
Patch0:		%{name}-make.patch
URL:		http://www.openwall.com/tcb/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The tcb package contains core components of our tcb suite implementing
the alternative password shadowing scheme on Owl. It is being made
available separately from Owl primarily for use by other
distributions.

%package devel
Summary:	Headers for libtcb
Group:		Development/Libraries

%description devel
Headers for libtcb.

%package static
Summary:	Static library for libtcb
Group:		Development/Libraries

%description static
Static library for libtcb.

%package -n pam-pam_tcb
Summary:	TCB module for PAM
Group:		Base

%description -n pam-pam_tcb
The alternative to shadow (TCB) PAM module.

%package -n nss_tcb
Summary:	Biblioteka TCB dla NSS
Group:		Base

%description -n nss_tcb
nss_tcb is a C library extension (NSS module) which allows TCB service
to be used as a primary source of aliases, ethers, groups, hosts,
networks, protocols, users, RPCs, services and shadow passwords
(instead of or in addition to using flat files or NIS).

%prep
%setup -q
%patch0 -p1

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
	LIBEXECDIR=%{_libexecdir} \
	MANDIR=%{_mandir}

mv $RPM_BUILD_ROOT%{_libexecdir}/chkpwd/tcb_chkpwd $RPM_BUILD_ROOT/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libtcb.so.0.9.8
%attr(755,root,root) /sbin/tcb_convert
%attr(755,root,root) /sbin/tcb_unconvert
%attr(755,root,root) /sbin/tcb_chkpwd
%{_mandir}/man5/tcb.5*
%{_mandir}/man8/tcb_convert.8*
%{_mandir}/man8/tcb_unconvert.8

%files devel
%defattr(644,root,root,755)
%{_includedir}/tcb.h

%files static
%defattr(644,root,root,755)
%{_prefix}/lib/libtcb.a

#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/chsh
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/passwd
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/useradd
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/shadow
#%exclude %{_mandir}/man8/pam_rpasswd.8*

%files -n nss_tcb
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss*.so.*

%files -n pam-pam_tcb
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/*.so
%{_mandir}/man8/pam_*.8*
