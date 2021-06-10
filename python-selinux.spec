%define	sepol_ver	2.9
Summary:	Python 2 binding for SELinux library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki SELinux
Name:		python-selinux
Version:	2.9
Release:	6
License:	Public Domain
Group:		Libraries
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://github.com/SELinuxProject/selinux/releases/download/20190315/libselinux-%{version}.tar.gz
# Source0-md5:	bb449431b6ed55a0a0496dbc366d6e31
Patch0:		libselinux-vcontext-selinux.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
%ifarch ppc ppc64 sparc sparcv9 sparc64
BuildRequires:	gcc >= 5:3.4
%else
BuildRequires:	gcc >= 5:3.2
%endif
BuildRequires:	glibc-devel >= 6:2.3
BuildRequires:	libsepol-static >= %{sepol_ver}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python
Requires:	libselinux >= %{version}
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 binding for SELinux library.

%description -l pl.UTF-8
Wiązania Pythona 2 do biblioteki SELinux.

%prep
%setup -q -n libselinux-%{version}
%patch0 -p1

# "-z defs" doesn't mix with --as-needed when some object needs symbols from
# ld.so (because of __thread variable in this case)
%{__sed} -i -e 's/-z,defs,//' src/Makefile

%build
%{__make} -j1 pywrap \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -D_FILE_OFFSET_BITS=64" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	PYPREFIX=python2 \
	PYSITEDIR=%{py_sitedir} \
	PYTHON=%{__python}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-pywrap \
	LIBDIR=%{_libdir} \
	SHLIBDIR=/%{_lib} \
	PYPREFIX=python2 \
	PYSITEDIR=%{py_sitedir} \
	PYTHON=%{__python} \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}/selinux
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/selinux
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%dir %{py_sitedir}/selinux
%attr(755,root,root) %{py_sitedir}/_selinux.so
%attr(755,root,root) %{py_sitedir}/selinux/audit2why.so
%{py_sitedir}/selinux/__init__.py[co]
