#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		khelpcenter
Summary:	khelpcenter
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	96b899e36e6e42b00deeacf55b64e95c
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.2
BuildRequires:	Qt6DBus-devel >= 5.15.2
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Widgets-devel >= 5.15.2
BuildRequires:	Qt6Xml-devel >= 5.15.2
BuildRequires:	cmake >= 3.20
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	gettext-devel
BuildRequires:	gettext-devel
BuildRequires:	grantlee-qt6-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.83.0
BuildRequires:	kf6-karchive-devel >= 5.83.0
BuildRequires:	kf6-kauth-devel >= %{kframever}
BuildRequires:	kf6-kbookmarks-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= 5.83.0
BuildRequires:	kf6-kdoctools-devel >= 5.83.0
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-kjobwidgets-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= 5.83.0
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= 5.83.0
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	kf6-sonnet-devel >= %{kframever}
BuildRequires:	libxml2-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xapian-core-devel
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Requires:	python3
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
ExcludeArch:	x32 i686
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE Help Center.

%description -l pl.UTF-8
Centrum pomocy KDE.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/khelpcenter
%attr(755,root,root) %{_prefix}/libexec/khc_mansearch.py
%attr(755,root,root) %{_prefix}/libexec/khc_xapianindexer
%attr(755,root,root) %{_prefix}/libexec/khc_xapiansearch

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/khelpcenter
%{_datadir}/qlogging-categories6/khelpcenter.categories
%{_desktopdir}/org.kde.khelpcenter.desktop
%{_datadir}/dbus-1/services/org.kde.khelpcenter.service
%{_datadir}/metainfo/org.kde.khelpcenter.metainfo.xml
