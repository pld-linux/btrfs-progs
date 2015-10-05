Summary:	Utilities belonging to the btrfs filesystem
Summary(pl.UTF-8):	Narzędzia należące do systemu plików btrfs
Name:		btrfs-progs
Version:	4.2.2
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz
# Source0-md5:	7b1cfba5198622e5cd915f4ac12500c6
Patch0:		%{name}-man.patch
URL:		http://btrfs.wiki.kernel.org/
BuildRequires:	acl-devel
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.60
BuildRequires:	e2fsprogs-devel
BuildRequires:	libblkid-devel
BuildRequires:	libcom_err-devel
BuildRequires:	libuuid-devel
BuildRequires:	lzo-devel >= 2
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xz
BuildRequires:	zlib-devel
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

%package devel
Summary:	Header files for btrfs filesystem-specific library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dla systemu plików btrfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
%{__make} install \
	prefix=%{_prefix} \
	bindir=%{_sbindir} \
	mandir=%{_mandir} \
	libdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf btrfsck $RPM_BUILD_ROOT%{_sbindir}/fsck.btrfs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL
%attr(755,root,root) %{_sbindir}/btrfsck
%attr(755,root,root) %{_sbindir}/mkfs.btrfs
%attr(755,root,root) %{_sbindir}/fsck.btrfs
%attr(755,root,root) %{_sbindir}/btrfs-debug-tree
%attr(755,root,root) %{_sbindir}/btrfs-image
%attr(755,root,root) %{_sbindir}/btrfs-convert
%attr(755,root,root) %{_sbindir}/btrfstune
%attr(755,root,root) %{_sbindir}/btrfs
%attr(755,root,root) %{_sbindir}/btrfs-map-logical
%attr(755,root,root) %{_sbindir}/btrfs-zero-log
%attr(755,root,root) %{_sbindir}/btrfs-find-root
%attr(755,root,root) %{_sbindir}/btrfs-select-super
%attr(755,root,root) %{_sbindir}/btrfs-show-super
%attr(755,root,root) %{_libdir}/libbtrfs.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libbtrfs.so.0
%{_mandir}/man5/btrfs.5*
%{_mandir}/man8/btrfs.8*
%{_mandir}/man8/btrfs-*.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/btrfstune.8*
%{_mandir}/man8/fsck.btrfs.8*
%{_mandir}/man8/mkfs.btrfs.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtrfs.so
%{_includedir}/btrfs

%files static
%defattr(644,root,root,755)
%{_libdir}/libbtrfs.a
