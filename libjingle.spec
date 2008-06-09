%define	major 0
%define libname	%mklibname jingle %{major}
%define develname %mklibname -d jingle

Summary:	Google Talk's implementation of Jingle and Jingle-Audio
Name:		libjingle
Version:	0.4.0
Release:	%mkrel 1
License:	BSD
Group:		System/Servers
URL:		http://sourceforge.net/projects/libjingle
Source0:	http://dl.sf.net/libjingle/%{name}-%{version}.tar.gz
# http://code.google.com/p/libjingle/issues/detail?id=2
Patch0:		libjingle-0.4.0-gcc43.patch
Patch1:		libjingle-0.4.0-ortp.patch
BuildRequires:	glib2-devel 
BuildRequires:	dbus-devel 
BuildRequires:	openssl-devel 
BuildRequires:	expat-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	speex-devel
BuildRequires:	libilbc-devel
BuildRequires:	ortp-devel
BuildRequires:	alsa-lib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Libjingle is a set of C++ components provided by Google to interoperate with
Google Talk's peer-to-peer and voice calling capabilities. The package includes
source code for Google's implementation of Jingle and Jingle-Audio, two
proposed extensions to the XMPP standard that are currently available in
experimental draft form.

%package -n	%{libname}
Summary:	Shared Google Talk's implementation of Jingle and Jingle-Audio library
Group:          System/Libraries

%description -n	%{libname}
Libjingle is a set of C++ components provided by Google to interoperate with
Google Talk's peer-to-peer and voice calling capabilities. The package includes
source code for Google's implementation of Jingle and Jingle-Audio, two
proposed extensions to the XMPP standard that are currently available in
experimental draft form.

This package contains the shared %{name} library.

%package -n	%{develname}
Summary:	Static library and header files for the %{name} library
Group:		Development/C++
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname -d jingle 0}

%description -n	%{develname}
Libjingle is a set of C++ components provided by Google to interoperate with
Google Talk's peer-to-peer and voice calling capabilities. The package includes
source code for Google's implementation of Jingle and Jingle-Audio, two
proposed extensions to the XMPP standard that are currently available in
experimental draft form.

This package contains the static %{name} library and its header files
needed to compile applications such as stegdetect, etc.

%prep

%setup -q
%patch0 -p0
%patch1 -p1

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# cleanup
for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
rm -rf autom4te.cache
rm -f configure
libtoolize --copy --force; aclocal; automake --add-missing --copy --foreign; autoconf

%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-speex=%{_prefix} \
    --with-ilbc=%{_prefix}
    
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/relayserver
%{_bindir}/stunserver

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
