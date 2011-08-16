### RPM external fastjet 2.4.4
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-2.1.0-nobanner
Patch2: fastjet-2.3.4-siscone-banner
Patch3: fastjet-2.4.4-noemptyareawarning
Patch4: fastjet-2.4.4-nodegeneracywarning

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p0


./configure --enable-shared --enable-cmsiterativecone --enable-atlascone --prefix=%i --enable-allcxxplugins

%build
make

%install
make install

%post
%{relocateConfig}lib/libCDFConesPlugin.la
%{relocateConfig}lib/libSISConePlugin.la
%{relocateConfig}lib/libsiscone.la
%{relocateConfig}lib/libJadePlugin.la
