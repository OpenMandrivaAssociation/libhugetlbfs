%define major 0
%define libname %mklibname hugetlbfs %{major}
%define develname %mklibname hugetlbfs -d
%define ldscriptdir %{_datadir}/%{name}/ldscripts

Summary:	A library which provides easy access to huge pages of memory
Name:		libhugetlbfs
Version:	2.6
Release:	%mkrel 2
Group:		System/Libraries
License:	LGPLv2+
URL:		https://libhugetlbfs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/libhugetlbfs/%{name}-%{version}.tar.gz
Patch0:		libhugetlbfs-2.6-s390x-build.patch
Patch1:		libhugetlbfs-2.6-sonames.diff
BuildRequires:	kernel-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libhugetlbfs is a library which provides easy access to huge pages of memory.
It is a wrapper for the hugetlbfs file system. Applications can use huge pages
to fulfill malloc() requests without being recompiled by using LD_PRELOAD.
Alternatively, applications can be linked against libhugetlbfs without source
modifications to load BSS or BSS, data, and text segments into large pages.

%package -n	%{libname}
Summary:	A library which provides easy access to huge pages of memory
Group:		System/Libraries

%description -n	%{libname}
libhugetlbfs is a library which provides easy access to huge pages of memory.
It is a wrapper for the hugetlbfs file system. Applications can use huge pages
to fulfill malloc() requests without being recompiled by using LD_PRELOAD.
Alternatively, applications can be linked against libhugetlbfs without source
modifications to load BSS or BSS, data, and text segments into large pages.

%package -n	%{develname}
Summary:	Header files for libhugetlbfs
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
libhugetlbfs is a library which provides easy access to huge pages of memory.
It is a wrapper for the hugetlbfs file system. Applications can use huge pages
to fulfill malloc() requests without being recompiled by using LD_PRELOAD.
Alternatively, applications can be linked against libhugetlbfs without source
modifications to load BSS or BSS, data, and text segments into large pages.

Contains header files for building with libhugetlbfs.

%package	utils
Summary:	Userspace utilities for configuring the hugepage environment
Group:		System/Kernel and hardware

%description	utils
This packages contains a number of utilities that will help administrate the
use of huge pages on your system.  hugeedit modifies binaries to set default
segment remapping behavior. hugectl sets environment variables for using huge
pages and then execs the target program. hugeadm gives easy access to huge page
pool size control. pagesize lists page sizes available on the machine.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1 -b .s390x-build
%patch1 -p0 -b .sonames

%build
# Parallel builds are not reliable
make CFLAGS="%{optflags} -fPIC" MAJOR="%{major}" BUILDTYPE=NATIVEONLY

%install
rm -rf %{buildroot}

make install PREFIX=%{_prefix} DESTDIR=%{buildroot} LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY

ln -s libhugetlbfs.so.%{major} %{buildroot}%{_libdir}/libhugetlbfs.so
ln -s get_huge_pages.3 %{buildroot}%{_mandir}/man3/free_huge_pages.3
ln -s get_hugepage_region.3 %{buildroot}%{_mandir}/man3/free_hugepage_region.3

# remove statically built libraries:
rm -f %{buildroot}%{_libdir}/*.a

# remove unused sbin directory
rm -rf %{buildroot}%{_sbindir}/

# these are not packaged in fedora
rm -f %{buildroot}%{_libdir}/libhugetlbfs_privutils.so.%{major}
rm -f %{buildroot}%{_bindir}/cpupcstat
rm -f %{buildroot}%{_bindir}/oprofile_map_events.pl
rm -f %{buildroot}%{_bindir}/oprofile_start.sh
rm -f %{buildroot}%{_mandir}/man8/cpupcstat.8*
rm -rf %{buildroot}/usr/lib/perl5/TLBC

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc README HOWTO LGPL-2.1 NEWS
%attr(0755,root,root) %{_libdir}/libhugetlbfs.so.%{major}
%{_datadir}/%{name}/
%attr(0644,root,root) %{_mandir}/man7/libhugetlbfs.7*

%files -n %{develname}
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/hugetlbfs.h
%attr(0644,root,root) %{_libdir}/libhugetlbfs.so
%attr(0644,root,root) %{_mandir}/man3/getpagesizes.3*
%attr(0644,root,root) %{_mandir}/man3/free_huge_pages.3*
%attr(0644,root,root) %{_mandir}/man3/get_huge_pages.3*
%attr(0644,root,root) %{_mandir}/man3/gethugepagesizes.3*
%attr(0644,root,root) %{_mandir}/man3/free_hugepage_region.3*
%attr(0644,root,root) %{_mandir}/man3/get_hugepage_region.3*

%files utils
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/hugeedit
%attr(0755,root,root) %{_bindir}/hugeadm
%attr(0755,root,root) %{_bindir}/hugectl
%attr(0755,root,root) %{_bindir}/pagesize
%attr(0644,root,root) %{_mandir}/man8/hugeedit.8*
%attr(0644,root,root) %{_mandir}/man8/hugectl.8*
%attr(0644,root,root) %{_mandir}/man8/hugeadm.8*
%attr(0644,root,root) %{_mandir}/man1/pagesize.1*

