%define	pssver	3.01

Summary:	Provides several solitaire card games
Name:		pysol
Version:        4.82
Release:        17
License:	GPL
Group:		Games/Cards
URL:		http://www.oberhumer.com/opensource/pysol/

Source0:	%{name}-%{version}.tar.bz2
Source1: 	http://www.oberhumer.com/opensource/pysol/download/pysol-sound-server-%{pssver}.tar.bz2
Source2:	%name-%version-src.tar.bz2
#gw use the pysol.py from the source release instead of the bytecode
Patch:		pysol-4.81-srcrelease.patch
Patch1:		pysol-4.82-sound.patch
Requires:	tkinter >= 1.5.2
BuildRequires:	pkgconfig(python-2.7)
#%py_requires -d
BuildRequires:  smpeg-devel

%description
PySol has several solitaire card games, written in 100%% pure
Python. It has many features: unlimited undo and redo, load & save
games, player statistics, hint system, game plug-ins, and more!
Contains: klondike, freecel, spider, golf, etc.

%prep
%setup -q -a 1 -a 2
%patch -p1
%patch1

cp pysol-sound-server-%pssver/NEWS NEWS.pysol-sound-server
cp pysol-sound-server-%pssver/README README.pysol-sound-server

%build
cd pysol-sound-server-%pssver/src
./configure --libdir=%_libdir
%make


%install
rm -fr %buildroot
make prefix=%_prefix bindir=%buildroot%_gamesbindir pkgdatadir=%buildroot%_gamesdatadir/%name install-bin install-data install-man mandir=%{buildroot}/%{_mandir}
perl -pi -e "s%%{buildroot}/usr%/usr%" %{buildroot}%_gamesbindir/pysol
cd pysol-sound-server-%pssver/src
python setup.py install --root=%{buildroot}
cd ../..
# they don't support python 2.4 yet
rm -f %buildroot%_gamesdatadir/%name/*pyc
mkdir %buildroot%_gamesdatadir/%name/BINARIES
cp -r %name-%version/src/* %buildroot%_gamesdatadir/%name/BINARIES
cat > %{buildroot}/%_gamesbindir/pysol << EOF
#!/bin/sh
exec python %_gamesdatadir/%name/BINARIES/pysol.py --pkgdatadir=%_gamesdatadir/%name/ --bindir=%_gamesdatadir/%name/BINARIES/ ${1+"$@"}

echo "$0: running $PYTHON failed !"
exit 1
EOF
chmod 755 %{buildroot}/%_gamesbindir/pysol

# Menu support
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=PySOL
Comment=All solitaire cards games
Exec=%{name}
Icon=cards_section
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Games-Cards;Game;CardGame;
EOF

%clean

%files
%defattr(-, root,root)
%doc NEWS* README*
%{_gamesdatadir}/pysol/
%{_gamesbindir}/pysol
%{_mandir}/man6/pysol.6*
%_datadir/applications/mandriva*
%{py_platsitedir}/*

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus} 
%endif




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 4.82-14mdv2011.0
+ Revision: 667909
- mass rebuild

* Mon Nov 01 2010 Funda Wang <fwang@mandriva.org> 4.82-13mdv2011.0
+ Revision: 591273
- rebuild for py2.7

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 4.82-12mdv2010.1
+ Revision: 523758
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 4.82-11mdv2010.0
+ Revision: 426793
- rebuild

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 4.82-10mdv2009.1
+ Revision: 319762
- rebuild for new python

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 4.82-9mdv2009.0
+ Revision: 218437
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 4.82-9mdv2008.1
+ Revision: 134227
- rebuild

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 4.82-8mdv2008.1
+ Revision: 125849
- kill re-definition of %%buildroot on Pixel's request
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Tue Nov 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 4.82-8mdv2007.0
+ Revision: 88188
- Import pysol

* Tue Nov 28 2006 Götz Waschk <waschk@mandriva.org> 4.82-8mdv2007.1
- update file list

* Wed Aug 02 2006 Götz Waschk <waschk@mandriva.org> 4.82-7mdv2007.0
- xdg menu

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 4.82-6mdk
- Rebuild

* Wed Apr 27 2005 Götz Waschk <waschk@mandriva.org> 4.82-5mdk
- update the pysol sound server to 3.01

* Mon Mar 21 2005 Nicolas Lécureuil <neoclust@mandrake.org> 4.82-4mdk
- Fix Spec files (Bug #12763) Thanks to hlomi Fish

* Sun Dec 05 2004 Götz Waschk <waschk@linux-mandrake.com> 4.82-3mdk
- patch bug 12578
- use the source, there's no python 2.4 bytecode available

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 4.82-2mdk
- Rebuild for new python

