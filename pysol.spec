%define	pssver	3.01

Summary:	PySol provides several solitaire card games
Name:		pysol
Version:        4.82
Release:        %mkrel 12
License:	GPL
Group:		Games/Cards
URL:		http://www.oberhumer.com/opensource/pysol/

Source0:	%{name}-%{version}.tar.bz2
Source1: 	http://www.oberhumer.com/opensource/pysol/download/pysol-sound-server-%{pssver}.tar.bz2
Source2:	%name-%version-src.tar.bz2
#gw use the pysol.py from the source release instead of the bytecode
Patch:		pysol-4.81-srcrelease.patch
Patch1:		pysol-4.82-sound.patch
BuildRoot:	%_tmppath/%name-%version-%release-root
Requires:	tkinter >= 1.5.2
%py_requires -d
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
make prefix=%_prefix bindir=%buildroot%_gamesbindir pkgdatadir=%buildroot%_gamesdatadir/%name install-bin install-data install-man mandir=$RPM_BUILD_ROOT/%{_mandir}
perl -pi -e "s%$RPM_BUILD_ROOT/usr%/usr%" $RPM_BUILD_ROOT%_gamesbindir/pysol
cd pysol-sound-server-%pssver/src
python setup.py install --root=$RPM_BUILD_ROOT
cd ../..
# they don't support python 2.4 yet
rm -f %buildroot%_gamesdatadir/%name/*pyc
mkdir %buildroot%_gamesdatadir/%name/BINARIES
cp -r %name-%version/src/* %buildroot%_gamesdatadir/%name/BINARIES
cat > $RPM_BUILD_ROOT/%_gamesbindir/pysol << EOF
#!/bin/sh
exec python %_gamesdatadir/%name/BINARIES/pysol.py --pkgdatadir=%_gamesdatadir/%name/ --bindir=%_gamesdatadir/%name/BINARIES/ ${1+"$@"}

echo "$0: running $PYTHON failed !"
exit 1
EOF
chmod 755 $RPM_BUILD_ROOT/%_gamesbindir/pysol

# Menu support
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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
rm -rf $RPM_BUILD_ROOT

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


