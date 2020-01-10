%define _disable_ld_no_undefined 1

%define	major 1
%define libname	%mklibname jingle %{major}
%define libnamedev %mklibname -d jingle
%define libnamestaticdev %mklibname jingle -d -s


Summary:	Google Talk's implementation of Jingle and Jingle-Audio
Group:		System/Servers
Name:		libjingle
Version:	0.6.14
Release:	1
License:	BSD
URL:            http://code.google.com/apis/talk/libjingle/
Source0:        http://libjingle.googlecode.com/files/%{name}-%{version}.zip
# Use Makefiles, dammit.
Patch0:		libjingle-0.6.14-build-sanity.patch
# talk/base/basictypes.h and talk/base/logging.h must be included 
# before any header with __BEGIN_DECLS, notably, sys/types.h
Patch1:		libjingle-0.5.1-C-linkage-fix.patch
# We need <cstdlib> for NULL.
Patch2:		libjingle-0.5.8-NULL-fix.patch
# In file included from /usr/include/fcntl.h:41:0,
#                 from physicalsocketserver.cc:37:
#/usr/include/bits/stat.h:91:21: error: field 'st_atim' has incomplete type
#/usr/include/bits/stat.h:92:21: error: field 'st_mtim' has incomplete type
#/usr/include/bits/stat.h:93:21: error: field 'st_ctim' has incomplete type
# FIX: Include <time.h> first.
Patch3:		libjingle-0.5.8-statfix.patch
# md5.h had a typedef for uint32 that did not match the one in basictypes.h
Patch4:		libjingle-0.5.1-uint32-fix.patch
# thread.cc: In static member function â€˜static bool talk_base::Thread::SleepMs(int)â€™:
# thread.cc:199:19: error: aggregate â€˜timespec tsâ€™ has incomplete type and cannot be defined
# thread.cc:202:34: error: â€˜nanosleepâ€™ was not declared in this scope
# This happens because a local header is included before time.h
Patch5:		libjingle-0.5.1-timefix.patch
# unixfilesystem.cc wouldn't compile.
Patch6:		libjingle-0.5.1-unixfilesystemfix.patch
# Google seems to love to be stupid with headers.
# Especially when they're in "third_party" code.
# Hardcoding paths in include files is dumb.
Patch7:		libjingle-0.5.8-system-expat.patch
Patch8:		libjingle-0.5.8-system-srtp.patch
# Fix devicemanager.cc to compile
Patch9:		libjingle-0.6.14-devicemanager-fix.patch
# Fix v4llookup.cc to compile
Patch10:	libjingle-0.5.8-v4llookup-fix.patch
# Fix type and definition conflicts with Chromium
Patch11:        libjingle-0.6.6-fixconflict.patch
# Make sure linux.h/linux.cc pulls in config.h for LINUX define
Patch14:	libjingle-0.5.8-config-linux.patch
# Fix 0.5.2 compilation
Patch16:	libjingle-0.6.6-compilefix.patch
# Fix missing cstdlib for size_t
Patch17:	libjingle-0.6.0-size_t.patch
# Fix obsolete macro usage
Patch18:	libjingle-0.5.8-fixmacro.patch
# Gcc 4.7.0 no longer includes unistd.h by default
Patch20:	libjingle-0.6.6-unistd.patch
Patch21:	libjingle-0.6.14-automake-1.13.patch
Patch22:	libjingle-0.6.14-aarch64.patch
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	dbus-devel 
BuildRequires:	openssl-devel 
BuildRequires:	expat-devel
BuildRequires:	srtp-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	kernel-headers
BuildRequires:	pkgconfig(udev)
BuildRequires:	alsa-oss-devel
BuildRequires:	pkgconfig(gtk+-2.0)

%description
Libjingle is a set of C++ components provided by Google to interoperate with
Google Talk's peer-to-peer and voice calling capabilities. The package includes
source code for Google's implementation of Jingle and Jingle-Audio, two
proposed extensions to the XMPP standard that are currently available in
experimental draft form.

%files
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/relayserver
%{_bindir}/stunserver


#------------------------------------------------------------------------------
%package -n %{libname}
Summary:	Shared Google Talk's implementation of Jingle and Jingle-Audio library
Group:          System/Libraries

%description -n	%{libname}
Libjingle is a set of C++ components provided by Google to interoperate with
Google Talk's peer-to-peer and voice calling capabilities. The package includes
source code for Google's implementation of Jingle and Jingle-Audio, two
proposed extensions to the XMPP standard that are currently available in
experimental draft form.

This package contains the shared %{name} library.

%files -n %{libname}
%{_libdir}/%{name}*.so.%{major}*


#------------------------------------------------------------------------------
%package -n %{libnamedev}
Summary:	Static library and header files for the %{name} library
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libnamedev}
Libjingle is a set of C++ components provided by Google to interoperate with
Google Talk's peer-to-peer and voice calling capabilities. The package includes
source code for Google's implementation of Jingle and Jingle-Audio, two
proposed extensions to the XMPP standard that are currently available in
experimental draft form.

%files -n %{libnamedev}
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}-0.6
%{_libdir}/%{name}*.so


#------------------------------------------------------------------------------
%package -n %{libnamestaticdev}
Summary:	Static files for the %{name} library
Group:		Development/C++
Requires:	%{libnamedev} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}

%description -n %{libnamestaticdev}
This package contains the static %{name} library and its header files
needed to compile applications such as stegdetect, etc.

%files -n %{libnamestaticdev}
%{_libdir}/%{name}*.a


#------------------------------------------------------------------------------
%prep
%setup -q
find . -perm 0640 | xargs chmod 0644
%autopatch -p1

sed -i 's!-lpthread!-lpthread -ldl!g' talk/p2p/base/Makefile.*
touch NEWS ChangeLog
autoreconf -i

rm -rf talk/base/time.h

%build
%configure --enable-static

## Remove rpath.
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std
