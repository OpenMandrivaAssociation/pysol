%define	pssver	3.01

Summary:	Provides several solitaire card games
Name:		pysol
Version:	2.21.0
Release:	1
License:	GPLv2
Group:		Games/Cards
# Discontinued original version http://www.oberhumer.com/opensource/pysol/
Url:		https://pysolfc.sourceforge.io/
Source0:	https://downloads.sourceforge.net/project/pysolfc/PySolFC/PySolFC-%{version}/PySolFC-%{version}.tar.xz
Source1:	https://downloads.sourceforge.net/project/pysolfc/PySolFC-Cardsets/PySolFC-Cardsets-2.2/PySolFC-Cardsets-2.2.tar.bz2
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python%{pyver}dist(setuptools)

%description
PySol has several solitaire card games, written in 100%% pure
Python. It has many features:	unlimited undo and redo, load & save
games, player statistics, hint system, game plug-ins, and more!
Contains:	klondike, freecel, spider, golf, etc.

%prep
%setup -n PySolFC-%{version} -a 1
%autopatch -p1

%build
%py_build

%install
%py_install
%find_lang pysol

cd %{buildroot}%{_datadir}/PySolFC
tar x --strip-components=1 -f %{S:1}

%files -f pysol.lang
%{_bindir}/pysol.py
%{_datadir}/PySolFC
%{_datadir}/icons/*/*/*/pysol.*
%{_datadir}/applications/*.desktop
%{python_sitelib}/pysollib
%{python_sitelib}/*.*-info
