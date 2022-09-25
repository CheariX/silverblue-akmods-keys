Name:           akmods-keys
Version:        0.0.2
Release:        8%{?dist}
Summary:        Keys for akmods

License:        MIT
URL:            http://rpmfusion.org/Packaging/KernelModules/Akmods

# We are upstream, these files are maintained directly in pkg-git
Source0:        public_key.der
Source1:        private_key.priv
Source2:        macros.kmodtool

BuildArch:      noarch

Supplements:    akmods


%description
Akmods ostree keys for signing modules.

%prep
%setup -q -c -T


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_sysconfdir}/pki/%{name}/certs \
         %{buildroot}%{_sysconfdir}/pki/%{name}/private \
         %{buildroot}%{_sysconfdir}/rpm/

install -pm 0640 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/%{name}/certs/
install -pm 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/%{name}/private/
install -pm 0640 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/

%pre

%post

%preun

%postun

%files
%attr(0644,root,root) %{_sysconfdir}/pki/%{name}/certs
%attr(0644,root,root) %{_sysconfdir}/pki/%{name}/private
%attr(0644,root,root) %{_sysconfdir}/rpm/macros.kmodtool

%changelog
* Tue Jun 28 2022 Christian Mainka <Christian.Mainka@rub.de> - 0.0.2
- Used macros.kmodtool to avoid filename conflicts

* Mon Jun 27 2022 Christian Mainka <Christian.Mainka@rub.de> - 0.0.1
- First Version
