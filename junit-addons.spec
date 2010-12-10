# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define	section		free

Name:		junit-addons
Summary:	JUnitX helper classes for JUnit
Url:		http://sourceforge.net/projects/junit-addons/
Version:	1.4
Release:	%mkrel 2.0.3
Epoch:		0
License:	Apache Software License
Group:		Development/Java
BuildArch:	noarch
Source0:	%{name}-%{version}.zip
Source1:	%{name}-build.xml
BuildRequires:	ant
BuildRequires:	jakarta-commons-logging
BuildRequires:	jaxen
BuildRequires:	jdom
BuildRequires:	junit
BuildRequires:	xerces-j2
BuildRequires:	xml-commons-apis
BuildRequires:  java-rpmbuild
Requires:	ant
Requires:	jakarta-commons-logging
Requires:	jaxen
Requires:	jdom
Requires:	junit
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JUnit-addons is a collection of helper classes for JUnit. 
This library can be used with both JUnit 3.7 and JUnit 3.8.x

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
chmod -R go=u-w *
jar xf src.jar
%remove_java_binaries
cp %{SOURCE1} build.xml

%build
%ant \
	-Dant.build.javac.source=1.4 \
	-Djdom.jar=$(build-classpath jdom) \
	-Djaxen.jar=$(build-classpath jaxen) \
	-Dsaxpath.jar=$(build-classpath jaxen) \
	-Dant.jar=$(build-classpath ant) \
	-Djunit.jar=$(build-classpath junit) \
	-Dxerces.jar=$(build-classpath xerces-j2) \
	-Dxml-apis.jar=$(build-classpath xml-commons-apis) \
	-Dcommons-logging.jar=$(build-classpath commons-logging) \
	-Dproject.name=junit-addons \
	-Dproject.version=1.4 \
	release

%install
rm -Rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# examples
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/examples
cp -pr src/example/* $RPM_BUILD_ROOT%{_datadir}/%{name}/examples

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc {LICENSE,README,WHATSNEW}
%{_javadir}/*
%{_datadir}/%{name}

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
