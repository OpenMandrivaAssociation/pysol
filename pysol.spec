%define	pssver	3.01

Summary:	Provides several solitaire card games
Name:		pysol
Version:	4.82
Release:	17
License:	GPLv2
Group:		Games/Cards
Url:		http://www.oberhumer.com/opensource/pysol/
Source0:	%{name}-%{version}.tar.bz2
Source1:	http://www.oberhumer.com/opensource/pysol/download/pysol-sound-server-%{pssver}.tar.bz2
Source2:	%{name}-%{version}-src.tar.bz2
#gw use the pysol.py from the source release instead of the bytecode
Patch0:		pysol-4.81-srcrelease.patch
Patch1:		pysol-4.82-sound.patch
Patch2:		pysol-4.82-tk-geometry-fix.patch
BuildRequires:	smpeg-devel
BuildRequires:	pkgconfig(python)
Requires:	tkinter >= 1.5.2

%description
PySol has several solitaire card games, written in 100%% pure
Python. It has many features:	unlimited undo and redo, load & save
games, player statistics, hint system, game plug-ins, and more!
Contains:	klondike, freecel, spider, golf, etc.

%prep
%setup -q -a 1 -a 2
%apply_patches

cp pysol-sound-server-%{pssver}/NEWS NEWS.pysol-sound-server
cp pysol-sound-server-%{pssver}/README README.pysol-sound-server

%build
cd pysol-sound-server-%{pssver}/src
./configure --libdir=%{_libdir}
%make


%install
make \
	prefix=%{_prefix} \
	bindir=%{buildroot}%{_gamesbindir} \
	pkgdatadir=%{buildroot}%{_gamesdatadir}/%{name} \
	install-bin \
	install-data \
	install-man \
	mandir=%{buildroot}/%{_mandir}
perl -pi -e "s%%{buildroot}/usr%/usr%" %{buildroot}%{_gamesbindir}/pysol
cd pysol-sound-server-%{pssver}/src
python setup.py install --root=%{buildroot}
cd ../..
# they don't support python 2.4 yet
rm -f %{buildroot}%{_gamesdatadir}/%{name}/*pyc
mkdir %{buildroot}%{_gamesdatadir}/%{name}/BINARIES
cp -r %{name}-%{version}/src/* %{buildroot}%{_gamesdatadir}/%{name}/BINARIES
cat > %{buildroot}/%{_gamesbindir}/pysol << EOF
#!/bin/sh
exec python %{_gamesdatadir}/%{name}/BINARIES/pysol.py --pkgdatadir=%{_gamesdatadir}/%{name}/ --bindir=%{_gamesdatadir}/%{name}/BINARIES/ ${1+"$@"}

echo "$0:	running $PYTHON failed !"
exit 1
EOF
chmod 755 %{buildroot}/%{_gamesbindir}/pysol

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

%files
%doc NEWS* README*
%{_gamesdatadir}/pysol/
%{_gamesbindir}/pysol
%{_mandir}/man6/pysol.6*
%_datadir/applications/mandriva*
%{py_platsitedir}/*

