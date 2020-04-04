# Define SCL name
%{!?scl_name_prefix: %global scl_name_prefix rh-}
%{!?scl_name_base: %global scl_name_base perl}
%{!?version_major: %global version_major 5}
%{!?version_minor: %global version_minor 30}
%{!?scl_name_version: %global scl_name_version %{version_major}%{version_minor}}
%{!?scl: %global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}}

# Turn on new layout -- prefix for packages and location
# for config and variable files
# This must be before calling %%scl_package
%{!?nfsmountable: %global nfsmountable 1}

# Define SCL macros
%{?scl_package:%scl_package %scl}

%{!?install_scl:%global install_scl 0}

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary: Package that installs %scl
Name:    %scl_name
Version: 3.5
Release: 2%{?dist}
License: GPLv2+
Source0: macro-build
Source1: README
Source2: LICENSE
Source3: roffexpandvar
BuildRequires: perl

%if 0%{?install_scl}
Requires: %{?scl_prefix}perl
%endif

BuildRequires: coreutils
BuildRequires: findutils
BuildRequires:  groff-base
BuildRequires: iso-codes
BuildRequires: scl-utils-build
BuildRequires: sed
BuildRequires: util-linux

%description
This is the main package for %scl Software Collection.

%package runtime
Summary:  Package that handles %scl Software Collection
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary:  Package shipping basic build configuration
Requires: scl-utils-build
Requires: %{name}-scldevel = %{version}-%{release}

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary:  Package shipping development files for %scl

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -c -T

# copy the license file so %%files section sees it
cp %{SOURCE2} .

%build
# This section expands manual page from a template and creates plain text
# from that file.
perl %{SOURCE3} \
	'%%{scl_name}' '%{scl_name}' \
	'%%{version}' '%{version}' \
	'%%{_scl_root}' '%{_scl_root}' \
	<%{SOURCE1} >%{scl_name}.7
<%{scl_name}.7 groff -Tutf8 -mandoc | LC_CTYPE=en_US.UTF-8 col -b >README


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_prefix}/local/bin:%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF
%scl_install

# Add the aditional macros to macros.%%{scl}-config
cat %{SOURCE0} >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config
sed -i 's|@MACRO@|%{scl_name_base}%{scl_name_version}|g' %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config
sed -i 's|@SCL@|%{scl}|g' %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config
sed -i 's|@LIBDIR@|%{_libdir}|g' %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{?scl_prefix}
EOF

# install generated man page
mkdir -p %{buildroot}%{_mandir}/man7/
install -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%files

%files runtime -f filelist
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Tue Jan 07 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.5-2
- Disable perl_bootstrap macro

* Thu Dec 19 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.5-1
- Initial version for SCL 3.5
- Enable perl_bootstrap macro

* Tue Dec 19 2017 Petr Pisar <ppisar@redhat.com> - 3.1-3
- Add a macro for perl_Devel_Size

* Tue Dec 19 2017 Petr Pisar <ppisar@redhat.com> - 3.1-2
- Disable perl_bootstrap macro

* Thu Dec 14 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.1-1
- Initial version for SCL 3.1
- Enable perl_bootstrap macro

* Sun Jul 24 2016 Petr Pisar <ppisar@redhat.com> 2.3-2
- Disable perl_bootstrap macro

* Tue Jul 12 2016 Jitka Plesnikova <jplesnik@redhat.com>, Petr Pisar <ppisar@redhat.com> - 2.3-1
- Initial version for SCL 2.3
- Escape apostrophs in rh-perl-520(7) manual page
- Fix ownership of man directories
- Resolves: rhbz#1219522, rhbz#1225445

* Tue Mar 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-7
- Rebuild due to 'scls' removal
- Resolves: rhbz#1200055

* Wed Jan 28 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-6
- Added local bin into PATH

* Sun Jan 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-5
- Disable macro perl_bootstrap

* Mon Jan 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-4
- Update macro %%__perl

* Thu Jan 15 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-3
- Define macros %%tests_req and %%tests_subpackage_requires in case the
  perl-macros is not in buildroot

* Tue Jan 13 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-2
- Added definition of LD_LIBRARY_PATH into the macro %%__perl
- Added macro %%perl_small for SCL restrictions

* Tue Jan 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0-1
- Initial version for SCL 2.0

* Mon Mar 31 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-2
- Wrong macro in README
- Resolves: rhbz#1061453

* Mon Feb 17 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-1
- Introduce README and LICENSE.
- Change version to 1.1.
- Resolves: rhbz#1061453

* Wed Feb 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-17
- Update dependencies of sub-package build
- Resolves: rhbz#1063206

* Mon Jan 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-16
- Changed name of sub-package devel to scldevel
- Added the file macros.%%{scl_name_base}-scldevel
- Resolves: rhbz#1055580

* Thu Jan 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-15
- Moved perl.(prov|req).stack and file*.attr to sub-package devel
- Resolves: rhbz#1052183

* Tue Jan 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-14
- Define macros for tests sub-package
- Resolves: rhbz#1049366

* Tue Dec 17 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-13
- Create macro-build
- Related: rhbz#1040880

* Mon Nov 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-12
- Add %%prep and %%build section

* Mon Jun 17 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-11
- Disable macro perl_bootstrap

* Thu May 23 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-10
- Update definition of MANPATH (rhbz#966388)

* Tue May 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-9
- Do not remove /opt/rh/perl516 to prevent removing of any user data

* Mon May 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-8
- Remove the directory /opt/rh/perl516 after uninstalling rpm (rhbz#956215)

* Sun Apr 28 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-7
- Remove extra colon from path definition

* Thu Apr 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-6
- Update setting of environment variable in the script enable

* Wed Feb  6 2013 Jitka Plesnikova <jplesnik@redhat.com> 1-5
- enable macro perl_bootstrap

* Fri Oct  5 2012 Marcela Mašláňová <mmaslano@redhat.com> 1-4
- update to new version of Perl 5.16
- package perl.{prov,req}.stack as executables

* Mon Jul 23 2012 Marcela Mašláňová <mmaslano@redhat.com> 1-3
- change permission from 700 to 644 on perl.{prov,req}

* Tue Mar  6 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.2
- fix dependency on collection *-runtime

* Tue Dec 06 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.1
- initial packaging of meta perl514 package
