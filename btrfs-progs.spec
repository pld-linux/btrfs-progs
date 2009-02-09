Summary:	Utilities belonging to the btrfs filesystem
Name:		btrfs-progs
Version:	0.18
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
# Source0-md5:	f1d49b54e3059f127fc82eab4fafcb8e
URL:		http://btrfs.wiki.kernel.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libuuid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Btrfs is a new copy on write filesystem for Linux aimed at
implementing advanced features while focusing on fault tolerance,
repair and easy administration.

%prep
%setup -q

sed -i -e 's#gcc#%{__cc}#g' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

%{__make} install \
	bindir=%{_sbindir} \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf btrfsck $RPM_BUILD_ROOT%{_sbindir}/fsck.btrfs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL
%attr(755,root,root) %{_sbindir}/*
