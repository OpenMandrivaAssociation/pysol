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
Source2:	http://www.pysol.org/download/pysol/%{name}-%{version}-src.tar.bz2
Patch:		pysol-4.81-srcrelease.patch
Patch1:		pysol-4.82-sound.patch
Requires:	tkinter >= 1.5.2
Requires:	python(abi) = 2.7
BuildRequires:	pkgconfig(python)
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

cp pysol-sound-server-%{pssver}/NEWS NEWS.pysol-sound-server
cp pysol-sound-server-%{pssver}/README README.pysol-sound-server

%build
cd pysol-sound-server-%{pssver}/src
./configure --libdir=%{_libdir}
%make


%install
make prefix=%{_prefix} bindir=%{buildroot}%{_gamesbindir} pkgdatadir=%{buildroot}%{_gamesdatadir}/%{name} \
  install-bin install-data install-man mandir=%{buildroot}/%{_mandir}

perl -pi -e "s%%{buildroot}/usr%/usr%" %{buildroot}%{_gamesbindir}/pysol
cd pysol-sound-server-%{pssver}/src
python setup.py install --root=%{buildroot}
cd ../..

rm -f %{buildroot}%{_gamesdatadir}/%{name}/*pyc

mkdir %{buildroot}%{_gamesdatadir}/%{name}/BINARIES
cp -r %{name}-%{version}/src/* %{buildroot}%{_gamesdatadir}/%{name}/BINARIES
cat > %{buildroot}/%{_gamesbindir}/pysol << EOF
#!/bin/sh
exec python %{_gamesdatadir}/%{name}/BINARIES/pysol.py --pkgdatadir=%{_gamesdatadir}/%{name}/ --bindir=%{_gamesdatadir}/%{name}/BINARIES/ ${1+"$@"}

echo "$0: running $PYTHON failed !"
exit 1
EOF

chmod 755 %{buildroot}/%{_gamesbindir}/pysol

# Menu support
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
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
%{_datadir}/applications/*
%{py_platsitedir}/*
