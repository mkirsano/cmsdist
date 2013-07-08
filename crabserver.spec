### RPM cms crabserver 3.2.0pre13
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES


%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 0.9.77
%define crabutils 0.0.1pre13

Source0: git://github.com/dmwm/WMCore.git?obj=master/%{wmcver}&export=WMCore-%{wmcver}&output=/WMCore-%{n}-%{wmcver}.tar.gz
Source1: git://github.com/dmwm/CRABServer.git?obj=master/%{realversion}&export=CRABServer-%{realversion}&output=/CRABServer-%{realversion}.tar.gz
#Source2: http://git.cern.ch/pub/CAFUtilities

Requires: python cherrypy py2-cjson rotatelogs py2-pycurl py2-httplib2 py2-sqlalchemy py2-cx-oracle py2-pyopenssl 
BuildRequires: py2-sphinx
Patch0: crabserver3-setup

%prep
%setup -D -T -b 1 -n CRABServer-%{realversion}
%setup -T -b 0 -n WMCore-%{wmcver}
%patch0 -p0

%build
#cafutilities
cd ../
git clone http://git.cern.ch/pub/CAFUtilities
cd CAFUtilities
git checkout %{crabutils}
cd -
mv CAFUtilities CAFUtilities-%{crabutils}

cd WMCore-%{wmcver}
python setup.py build_system -s crabserver
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../CRABServer-%{realversion}
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/crabserver/conf.py
python setup.py build_system -s CRABInterface

%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
## CAFUtilities selected modules
CAFUTILSMOD='PandaServerInterface.py TaskStateMachine Databases'
for mod in $CAFUTILSMOD; do cp -r ../CAFUtilities-%{crabutils}/src/python/$mod %i/$PYTHON_LIB_SITE_PACKAGES/; done
cd ../WMCore-%{wmcver}
python setup.py install_system -s crabserver --prefix=%i
cd ../CRABServer-%{realversion}
python setup.py install_system -s CRABInterface --prefix=%i

find %i -name '*.egg-info' -exec rm {} \;

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES/CRABServer || true

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc