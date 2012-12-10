%define _disable_ld_no_undefined 1

%define	major 0
%define libname	%mklibname jingle %{major}
%define develname %mklibname -d jingle

Summary:	Google Talk's implementation of Jingle and Jingle-Audio
Name:		libjingle
Version:	0.4.0
Release:	1
License:	BSD
Group:		System/Servers
URL:		http://sourceforge.net/projects/libjingle
Source0:	http://ignum.dl.sourceforge.net/project/libjingle/libjingle/%version/libjingle-%version.tar.gz
Patch0:		libjingle-0.4.0-compile.patch
BuildRequires:	glib2-devel 
BuildRequires:	dbus-devel 
BuildRequires:	openssl-devel 
BuildRequires:	expat-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

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
%apply_patches

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
find . -name Makefile.am |xargs sed -i -e 's,noinst_LTLIB,lib_LTLIB,g;s,noinst_HEAD,include_HEAD,g'

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
    --enable-static

%make

%install
%makeinstall_std
# Let's not conflict with standard tools
mv %buildroot%_bindir/login %buildroot%_bindir/%name-login

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/relayserver
%{_bindir}/stunserver
%_bindir/%name-login
%_bindir/pcp

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Fri Oct 17 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3.12-1mdv2009.1
+ Revision: 294791
- 0.3.12 (0.4.0 will be another package)
- fix linkage, still _disable_ld_no_undefined has to be used
- 0.4.0
- added other gcc43 patches (more fixes needed)
- added a gcc43 patch from fedora

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Jul 10 2007 Funda Wang <fundawang@mandriva.org> 0.3.11-1mdv2008.0
+ Revision: 50828
- New version


* Tue Oct 10 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 0.3.10-1mdv2007.0
+ Revision: 63091
- New release 0.3.10
- Clean specfile
- Rediff Patch0
- import libjingle-0.3.0-3mdv2007.0

* Wed Jun 21 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-3mdv2007.0
- libified
- added some libtool fixes (P0)
- added fixes from tapioca svn trunk (P1)
- added P2,P3,P4 from the sf tracker
- added lib64 fixes

* Fri Apr 07 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.3.0-2mdk
- Add post/postun

* Fri Apr 07 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.3.0-1mdk
- First Mandriva release

