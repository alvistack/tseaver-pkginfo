import os
import sys
import types
import wsgiref
import warnings

import pytest

def _make_installed(filename=None, metadata_version=None):
    from pkginfo.installed import Installed

    if metadata_version is not None:
        return Installed(filename, metadata_version)

    return Installed(filename)

def test_installed_ctor_w_package_no___file__():
    from pkginfo.distribution import UnknownMetadataVersion

    with warnings.catch_warnings(record=True) as warned:

        installed = _make_installed(sys)

    assert(installed.package == sys)
    assert(installed.package_name == 'sys')
    assert(installed.metadata_version == None)

    assert(len(warned) == 2)
    assert str(warned[0].message).startswith('No PKG-INFO found')
    assert warned[1].category is UnknownMetadataVersion

def test_installed_ctor_w_package():
    import pkginfo
    from pkginfo.tests import _checkSample
    from pkginfo.tests import _defaultMetadataVersion

    EXPECTED =  _defaultMetadataVersion()

    installed = _make_installed(pkginfo)

    assert(installed.package == pkginfo)
    assert(installed.package_name == 'pkginfo')
    assert(installed.metadata_version == EXPECTED)
    _checkSample(None, installed)

def test_installed_ctor_w_no___package___falls_back_to___name__():
    from pkginfo.distribution import UnknownMetadataVersion

    with warnings.catch_warnings(record=True) as warned:
        installed = _make_installed(wsgiref)

    assert(installed.package == wsgiref)
    assert(installed.package_name == 'wsgiref')
    assert(installed.metadata_version == None)

    assert(len(warned) == 2)
    assert str(warned[0].message).startswith('No PKG-INFO found')
    assert warned[1].category is UnknownMetadataVersion

def test_installed_ctor_w_package_no_PKG_INFO():
    from pkginfo.distribution import UnknownMetadataVersion

    with warnings.catch_warnings(record=True) as warned:
        installed = _make_installed(types)

    assert(installed.package == types)
    assert(installed.package_name == 'types')
    assert(installed.metadata_version == None)

    assert(len(warned) == 2)
    assert str(warned[0].message).startswith('No PKG-INFO found')
    assert warned[1].category is UnknownMetadataVersion

def test_installed_ctor_w_package_and_metadata_version():
    import pkginfo
    from pkginfo.tests import _checkSample

    installed = _make_installed(pkginfo, metadata_version='1.2')

    assert(installed.metadata_version == '1.2')
    assert(installed.package.__name__ == 'pkginfo')
    _checkSample(None, installed)

def test_installed_ctor_w_name():
    import pkginfo
    from pkginfo.tests import _checkSample
    from pkginfo.tests import _defaultMetadataVersion

    EXPECTED = _defaultMetadataVersion()

    installed = _make_installed('pkginfo')

    assert(installed.metadata_version == EXPECTED)
    assert(installed.package == pkginfo)
    assert(installed.package_name == 'pkginfo')
    _checkSample(None, installed)

def test_installed_ctor_w_name_and_metadata_version():
    import pkginfo
    from pkginfo.tests import _checkSample

    installed = _make_installed('pkginfo', metadata_version='1.2')
    assert(installed.metadata_version == '1.2')
    assert(installed.package == pkginfo)
    assert(installed.package_name == 'pkginfo')
    _checkSample(None, installed)

def test_installed_ctor_w_invalid_name():
    from pkginfo.distribution import UnknownMetadataVersion

    with warnings.catch_warnings(record=True) as warned:
        installed = _make_installed('nonesuch')

    assert(installed.package == None)
    assert(installed.package_name == 'nonesuch')
    assert(installed.metadata_version == None)

    assert(len(warned) == 2)
    assert str(warned[0].message).startswith('No PKG-INFO found')
    assert warned[1].category is UnknownMetadataVersion

def test_installed_ctor_w_egg_info_as_file():
    import pkginfo.tests.funny

    installed = _make_installed('pkginfo.tests.funny')

    assert(installed.metadata_version == '1.0')
    assert(installed.package == pkginfo.tests.funny)
    assert(installed.package_name == 'pkginfo.tests.funny')

def test_installed_ctor_w_dist_info():
    from packaging import version
    import wheel

    installed = _make_installed('wheel')

    assert(installed.package == wheel)
    assert(installed.package_name == 'wheel')

    # See: https://bugs.launchpad.net/pkginfo/+bug/2090840
    installed_version = version.Version(installed.version)
    if installed_version < version.Version('0.44.dev0'):
        assert(installed.metadata_version == '2.1')
    else:
        assert(installed.metadata_version == '2.3')

def test_installed_namespaced_pkg_installed_via_setuptools():
    where, _ = os.path.split(__file__)
    wonky = os.path.join(where, 'wonky')
    oldpath = sys.path[:]
    try:
        sys.path.append(wonky)

        with warnings.catch_warnings(record=True):
            import namespaced.wonky

        installed = _make_installed('namespaced.wonky')

    finally:
        sys.path[:] = oldpath
        sys.modules.pop('namespaced.wonky', None)
        sys.modules.pop('namespaced', None)

    assert(installed.metadata_version == '1.0')
    assert(installed.package == namespaced.wonky)
    assert(installed.package_name == 'namespaced.wonky')

def test_installed_namespaced_pkg_installed_via_pth():
    # E.g., installed by a Linux distro
    where, _ = os.path.split(__file__)
    manky = os.path.join(where, 'manky')
    oldpath = sys.path[:]
    try:
        sys.path.append(manky)

        with warnings.catch_warnings(record=True):
            import namespaced.manky

        installed = _make_installed('namespaced.manky')

    finally:
        sys.path[:] = oldpath
        sys.modules.pop('namespaced.manky', None)
        sys.modules.pop('namespaced', None)

    assert(installed.metadata_version == '1.0')
    assert(installed.package == namespaced.manky)
    assert(installed.package_name == 'namespaced.manky')
