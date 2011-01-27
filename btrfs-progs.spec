Summary:	Utilities belonging to the btrfs filesystem
Name:		btrfs-progs
Version:	0.19
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
# Source0-md5:	5854728d080cc76f21a83bdc99b6ddaa
Patch0:		%{name}-fix-labels.patch
Patch1:		%{name}-build-everything.patch
Patch2:		%{name}-valgrind.patch
Patch3:		%{name}-fix-return-value.patch
Patch4:		%{name}-build-fixes.patch
Patch5:		%{name}-upstream.patch
URL:		http://btrfs.wiki.kernel.org/
BuildRequires:	libuuid-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Btrfs is a new copy on write filesystem for Linux aimed at
implementing advanced features while focusing on fault tolerance,
repair and easy administration.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch1 -p1

sed -i -e 's#gcc#$(CC)#g' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

%{__make} install \
	prefix=%{_prefix} \
	bindir=%{_sbindir} \
	mandir=%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf btrfsck $RPM_BUILD_ROOT%{_sbindir}/fsck.btrfs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*
