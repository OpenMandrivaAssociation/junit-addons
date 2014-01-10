%{?_javapackages_macros:%_javapackages_macros}
Name:          junit-addons
Version:       1.4
Release:       5.0%{?dist}
Summary:       JUnitX helper classes for JUnit

License:       ASL 1.1
Url:           http://sourceforge.net/projects/%{name}/
Source0:       http://sourceforge.net/projects/%{name}/files/JUnit-addons/JUnit-addons%20%{version}/%{name}-%{version}.zip
# from http://junit-addons.cvs.sourceforge.net/viewvc/junit-addons/junit-addons/build.xml?view=markup&pathrev=release_1_4
Source1:       %{name}-build.xml
Source2:       http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
BuildRequires: java-devel
BuildRequires: jpackage-utils

BuildRequires: ant
BuildRequires: apache-commons-logging
BuildRequires: jaxen
BuildRequires: jdom
BuildRequires: junit4
BuildRequires: xerces-j2
BuildRequires: xml-commons-apis

Requires:      ant
Requires:      jaxen
Requires:      jdom
Requires:      junit4
Requires:      xerces-j2

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description
JUnit-addons is a collection of helper classes for JUnit. 

%package javadoc

Summary:       Javadoc for %{name}
Requires:      jpackage-utils

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%jar xf src.jar
find . -name "*.class" -delete
find . -type f -name "*.jar" -delete
find . -type f -name "*.zip" -delete

rm -r api
cp -p %{SOURCE1} build.xml

# fix non ASCII chars
for s in src/main/junitx/framework/TestSuite.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# disable test
# some tests fails with the regenerate test resource
# tests.jar
# tests.zip
sed -i "s| test, ||" build.xml

%build
# regenerate test resource
#(
#  cd src/example
#  mkdir test
#  javac -d test -source 1.4 -target 1.4 $(find . -name "*.java") -cp $(build-classpath junit4)
#  rm test/junitx/example/*.class
#  cp -p junitx/example/packageA/SampleA.txt test/junitx/example/packageA/
#  cp -p junitx/example/packageA/packageB/SampleB.txt test/junitx/example/packageA/packageB/
#  (
#    cd test
#    jar -cf ../tests.jar *
##    zip -r ../tests.zip *
#  )
#  cp -p tests.jar tests.zip
#  rm -r test
#)

export CLASSPATH=
export OPT_JAR_LIST=:
%ant \
  -Dant.build.javac.source=1.4 \
  -Djdom.jar=$(build-classpath jdom) \
  -Djaxen.jar=$(build-classpath jaxen) \
  -Dsaxpath.jar=$(build-classpath jaxen) \
  -Dant.jar=$(build-classpath ant.jar) \
  -Djunit.jar=$(build-classpath junit4) \
  -Dxerces.jar=$(build-classpath xerces-j2) \
  -Dxml-apis.jar=$(build-classpath xml-commons-apis) \
  -Dcommons-logging.jar=$(build-classpath commons-logging) \
  -Dproject.name=%{name} \
  -Dproject.version=%{version} \
  release

%install

mkdir -p %{buildroot}%{_javadir}
install -m 644 dist/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE README WHATSNEW

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 gil cattaneo <puntogil@libero.it> 1.4-2
- remove pre-compiled artefacts
- add requires ant, jaxen, jdom

* Sat May 05 2012 gil cattaneo <puntogil@libero.it> 1.4-1
- initial rpm

