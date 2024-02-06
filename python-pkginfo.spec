# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: python-pkginfo
Epoch: 100
Version: 1.10.0
Release: 1%{?dist}
BuildArch: noarch
Summary: Query metadatdata from sdists / bdists / installed packages
License: MIT
URL: https://pypi.org/project/pkginfo/#history
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: fdupes
BuildRequires: python-rpm-macros
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
This package provides an API for querying the distutils metadata written
in the PKG-INFO file inside a source distriubtion (an sdist) or a binary
distribution (e.g., created by running bdist\_egg). It can also query
the EGG-INFO directory of an installed distribution, and the \*.egg-info
stored in a “development checkout” (e.g, created by running setup.py
develop).

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%py3_build

%install
%py3_install
find %{buildroot}%{python3_sitelib} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitelib}

%check

%if 0%{?suse_version} > 1500
%package -n python%{python3_version_nodots}-pkginfo
Summary: Query metadatdata from sdists / bdists / installed packages
Requires: python3
Provides: python3-pkginfo = %{epoch}:%{version}-%{release}
Provides: python3dist(pkginfo) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-pkginfo = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(pkginfo) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-pkginfo = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(pkginfo) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-pkginfo
This package provides an API for querying the distutils metadata written
in the PKG-INFO file inside a source distriubtion (an sdist) or a binary
distribution (e.g., created by running bdist\_egg). It can also query
the EGG-INFO directory of an installed distribution, and the \*.egg-info
stored in a “development checkout” (e.g, created by running setup.py
develop).

%files -n python%{python3_version_nodots}-pkginfo
%license LICENSE.txt
%{_bindir}/*
%{python3_sitelib}/*
%endif

%if !(0%{?suse_version} > 1500)
%package -n python3-pkginfo
Summary: Query metadatdata from sdists / bdists / installed packages
Requires: python3
Provides: python3-pkginfo = %{epoch}:%{version}-%{release}
Provides: python3dist(pkginfo) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-pkginfo = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(pkginfo) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-pkginfo = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(pkginfo) = %{epoch}:%{version}-%{release}

%description -n python3-pkginfo
This package provides an API for querying the distutils metadata written
in the PKG-INFO file inside a source distriubtion (an sdist) or a binary
distribution (e.g., created by running bdist\_egg). It can also query
the EGG-INFO directory of an installed distribution, and the \*.egg-info
stored in a “development checkout” (e.g, created by running setup.py
develop).

%files -n python3-pkginfo
%license LICENSE.txt
%{_bindir}/*
%{python3_sitelib}/*
%endif

%changelog
