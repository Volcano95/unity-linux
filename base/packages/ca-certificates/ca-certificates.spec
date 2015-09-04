Name:		ca-certificates
Version:	20150426
Release:	1%{?dist}
Summary:	A CA root certificate bundle

Group:		System Environment/Base
License:	GPL-v2+ and MPL-2.0
URL:		http://packages.debian.org/sid/ca-certificates
Source0:	http://ftp.no.debian.org/debian/pool/main/c/%{name}/%{name}_%{version}.tar.xz
Source1:	update-ca-certificates

BuildRequires:	python
Requires:	openssl lua5.2	

BuildArch: noarch

%description
This package includes PEM files of CA certificates to allow SSL-based applications to check 
for the authenticity of SSL connections. It includes, among others, certificate authorities 
used by the Debian infrastructure and those shipped with Mozilla's browsers.

%prep
%setup -q


%build
make %{?_smp_mflags}


%install
install -d -m755 %{buildroot}/etc/ca-certificates/update.d \
		%{buildroot}/usr/sbin \
		%{buildroot}/usr/share/ca-certificates \
		%{buildroot}/usr/local/share/ca-certificates \
		%{buildroot}/etc/ssl/certs \

make DESTDIR=%{buildroot} install
install -D -m644 sbin/update-ca-certificates.8 \
		%{buildroot}/usr/share/man/man8/update-ca-certificates.8 \

(
echo "# Automatically generated by %{name}-%{version}-%{release}"
echo "# $(date -u)"
echo "# Do not edit."
cd %{buildroot}/usr/share/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > %{buildroot}/etc/ca-certificates.conf

install -m755 %{SOURCE1} %{buildroot}/usr/sbin \

%post
exec /usr/sbin/update-ca-certificates --fresh

%files
/etc/ca-certificates.conf
/usr/sbin/update-ca-certificates
%dir /usr/share/ca-certificates
%dir /usr/share/ca-certificates/spi-inc.org
%dir /usr/share/ca-certificates/mozilla
/usr/share/ca-certificates/spi-inc.org/spi-cacert-2008.crt
/usr/share/ca-certificates/mozilla/*.crt


%changelog
