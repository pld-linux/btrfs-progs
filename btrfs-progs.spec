Summary:	Utilities belonging to the btrfs filesystem
Name:		btrfs-progs
Version:	3.12
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/kernel/people/mason/btrfs-progs/%{name}-v%{version}.tar.xz
# Source0-md5:	cd96bb73acd864e577cddba5fe310650
URL:		http://btrfs.wiki.kernel.org/
BuildRequires:	acl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	libblkid-devel
BuildRequires:	libuuid-devel
BuildRequires:	lzo-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Btrfs is a new copy on write filesystem for Linux aimed at
implementing advanced features while focusing on fault tolerance,
repair and easy administration.

%package devel
Summary:	btrfs filesystem-specific libraries and headers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
btrfs-progs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

You should install btrfs-progs-devel if you want to develop btrfs
filesystem-specific programs.

%prep
%setup -q -n %{name}-v%{version}

%build
%{__make} \
	V=1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -fno-strict-aliasing"

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

rm $RPM_BUILD_ROOT%{_libdir}/*.a

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
%attr(755,root,root) %{_sbindir}/btrfs-show-super
%attr(755,root,root) %{_libdir}/libbtrfs.so.*.*
%ghost %{_libdir}/libbtrfs.so.0
%{_mandir}/man8/btrfs-image.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/mkfs.btrfs.8*
%{_mandir}/man8/btrfs.8*
%{_mandir}/man8/btrfs-convert.8*
%{_mandir}/man8/btrfs-debug-tree.8*
%{_mandir}/man8/btrfs-find-root.8*
%{_mandir}/man8/btrfs-map-logical.8*
%{_mandir}/man8/btrfs-show-super.8*
%{_mandir}/man8/btrfs-zero-log.8*
%{_mandir}/man8/btrfstune.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/btrfs
%{_libdir}/libbtrfs.so
