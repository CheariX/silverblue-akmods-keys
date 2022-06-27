Name:           akmods-keys
Version:        0.0.1
Release:        8%{?dist}
Summary:        Keys for akmods

License:        MIT
URL:            http://rpmfusion.org/Packaging/KernelModules/Akmods

# We are upstream, these files are maintained directly in pkg-git
Source0:        public_key.der
Source1:        private_key.priv

BuildArch:      noarch

Supplements:    akmods


%description
Akmods ostree keys for signing modules.

%prep
%setup -q -c -T


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_sysconfdir}/pki/akmods/certs \
         %{buildroot}%{_sysconfdir}/pki/akmods/private

install -pm 0640 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/akmods/certs/
install -pm 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/akmods/private/

%pre

%post

%preun

%postun

%files
%attr(0644,root,root) %{_sysconfdir}/pki/akmods/certs
%attr(0644,root,root) %{_sysconfdir}/pki/akmods/private

%changelog
* Mon June 27 2022 Christian Mainka <Christian.Mainka@rub.de> - 0.0.1
- First Version
