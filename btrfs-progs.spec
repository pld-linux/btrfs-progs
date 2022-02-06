#
# Conditional build:
%bcond_without	python	# Python bindings for libbtrfsutil
%bcond_without	tests	# libbtrfsutil tests (requires python)

%if %{without python}
%undefine	with_tests
%endif
Summary:	Utilities belonging to the btrfs filesystem
Summary(pl.UTF-8):	Narzędzia należące do systemu plików btrfs
Name:		btrfs-progs
Version:	5.16.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz
# Source0-md5:	1eb504968c13e2220e7533ebfe78e233
Patch0:		%{name}-sh.patch
URL:		https://btrfs.wiki.kernel.org/
BuildRequires:	acl-devel
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	e2fsprogs-devel >= 1.42.0
BuildRequires:	libblkid-devel
BuildRequires:	libcom_err-devel
BuildRequires:	libuuid-devel
BuildRequires:	lzo-devel >= 2
BuildRequires:	pkgconfig >= 0.9.0
%{?with_python:BuildRequires:	python3-devel >= 1:3.4}
%{?with_python:BuildRequires:	python3-setuptools}
BuildRequires:	reiserfsprogs-devel >= 3.6.27
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:190
BuildRequires:	xmlto
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.0.0
Requires:	e2fsprogs-libs >= 1.42.0
Requires:	reiserfsprogs-libs >= 1:3.6.27
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Btrfs is a new copy on write filesystem for Linux aimed at
implementing advanced features while focusing on fault tolerance,
repair and easy administration.

%description -l pl.UTF-8
Btrfs to nowy system plików dla Linuksa oparty na zasadzie kopiowania
przy zapisie (copy-on-write), którego celem jest zaimplementowanie
zaawansowanych możliwości ze szczególnym naciskiem na odporność na
awarie, naprawę i łatwe administrowanie.

%package libs
Summary:	Shared btrfs library
Summary(pl.UTF-8):	Biblioteka współdzielona btrfs
Group:		Libraries

%description libs
Shared btrfs library.

%description libs -l pl.UTF-8
Biblioteka współdzielona btrfs.

%package devel
Summary:	Header files for btrfs filesystem-specific library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dla systemu plików btrfs
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files needed to develop btrfs
filesystem-specific programs.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne przy tworzeniu programów
przeznaczonych dla systemu plików btrfs.

%package static
Summary:	Static btrfs filesystem library
Summary(pl.UTF-8):	Statyczna biblioteka dla systemu plików btrfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static btrfs filesystem library.

%description static -l pl.UTF-8
Statyczna biblioteka dla systemu plików btrfs.

%package -n libbtrfsutil
Summary:	Library for managing Btrfs filesystems
Summary(pl.UTF-8):	Biblioteka do zarządzania systemami plików Btrfs
License:	LGPL v2.1+
Group:		Libraries

%description -n libbtrfsutil
libbtrfsutil is a library for managing Btrfs filesystems. It is
licensed under the LGPL. libbtrfsutil provides interfaces for a subset
of the operations offered by the btrfs command line utility. It also
has official Python bindings (Python 3 only).

%description -n libbtrfsutil -l pl.UTF-8
libbtrfsutil to biblioteka do zarządzania systemami plików Btrfs. Jest
dostępna na licencji LGPL. Udostępnia interfejsy do podzbioru operacji
oferowanych przez narzędzie linii poleceń btrfs. Ma także oficjalne
wiązania do Pythona (tylko Pythona 3).

%package -n libbtrfsutil-devel
Summary:	Header file for libbtrfsutil library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libbtrfsutil
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	libbtrfsutil = %{version}-%{release}

%description -n libbtrfsutil-devel
Header file for libbtrfsutil library.

%description -n libbtrfsutil-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libbtrfsutil.

%package -n libbtrfsutil-static
Summary:	Static libbtrfsutil library
Summary(pl.UTF-8):	Statyczna biblioteka libbtrfsutil
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	libbtrfsutil-devel = %{version}-%{release}

%description -n libbtrfsutil-static
Static libbtrfsutil library.

%description -n libbtrfsutil-static -l pl.UTF-8
Statyczna biblioteka libbtrfsutil.

%package -n python3-btrfsutil
Summary:	Python library for managing Btrfs filesystems
Summary(pl.UTF-8):	Biblioteka Pythona do zarządzania systemami plików Btrfs
Group:		Libraries/Python
License:	LGPL v2.1+
Requires:	libbtrfsutil = %{version}-%{release}

%description -n python3-btrfsutil
Python library for managing Btrfs filesystems.

%description -n python3-btrfsutil -l pl.UTF-8
Biblioteka Pythona do zarządzania systemami plików Btrfs.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%configure \
	%{!?with_python:--disable-python}
%{__make} \
	V=1

%if %{with tests}
%{__make} test-libbtrfsutil
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
%{__make} install \
	prefix=%{_prefix} \
	bindir=%{_sbindir} \
	mandir=%{_mandir} \
	libdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__make} install_python \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n libbtrfsutil -p /sbin/ldconfig
%postun	-n libbtrfsutil -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README.md
%attr(755,root,root) %{_sbindir}/btrfs
%attr(755,root,root) %{_sbindir}/btrfs-convert
%attr(755,root,root) %{_sbindir}/btrfs-find-root
%attr(755,root,root) %{_sbindir}/btrfs-image
%attr(755,root,root) %{_sbindir}/btrfs-map-logical
%attr(755,root,root) %{_sbindir}/btrfs-select-super
%attr(755,root,root) %{_sbindir}/btrfsck
%attr(755,root,root) %{_sbindir}/btrfstune
%attr(755,root,root) %{_sbindir}/fsck.btrfs
%attr(755,root,root) %{_sbindir}/mkfs.btrfs
/lib/udev/rules.d/64-btrfs-dm.rules
/lib/udev/rules.d/64-btrfs-zoned.rules
%{_mandir}/man5/btrfs.5*
%{_mandir}/man8/btrfs.8*
%{_mandir}/man8/btrfs-*.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/btrfstune.8*
%{_mandir}/man8/fsck.btrfs.8*
%{_mandir}/man8/mkfs.btrfs.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtrfs.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libbtrfs.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtrfs.so
%{_includedir}/btrfs

%files static
%defattr(644,root,root,755)
%{_libdir}/libbtrfs.a

%files -n libbtrfsutil
%defattr(644,root,root,755)
%doc libbtrfsutil/README.md
%attr(755,root,root) %{_libdir}/libbtrfsutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbtrfsutil.so.1

%files -n libbtrfsutil-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtrfsutil.so
%{_includedir}/btrfsutil.h
%{_pkgconfigdir}/libbtrfsutil.pc

%files -n libbtrfsutil-static
%defattr(644,root,root,755)
%{_libdir}/libbtrfsutil.a

%if %{with python}
%files -n python3-btrfsutil
%attr(755,root,root) %{py3_sitedir}/btrfsutil.cpython-*.so
%{py3_sitedir}/btrfsutil-%{version}-py*.egg-info
%endif
