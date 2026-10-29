%global distro  IGOS Nusantara
%define release_name    Ciremai
%global major   26
%global minor   1
%global eol_date 2035-06-01
# The Enterprise Linux release IGN is built on: what packages of EL 10 and EPEL
# 10 ask for (redhat-release >= 10, $releasever 10, platform:el10, %%rhel 10).
# IGN's own 26.1 is only its name (issue #100).
%global el_major 10
%global el_minor 2

Name:           ign-release
# Above the 2026.1 packages before; their version was IGN's year.
Epoch:          1
Version:        %{major}.%{minor}
Release:        9
Summary:        %{distro} release files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://igos-nusantara.or.id

Provides:       centos-release = %{el_major}.%{el_minor}
# When running a compose for ELN, we want to make sure that we pull in the
# correct templates when lorax is installed. This Suggests: will clue
# libdnf to use this set of templates instead of lorax-templates-generic.
Suggests:       lorax-templates-ign

# Required for a lorax run (to generate install media)
Requires:       ign-repos = %{epoch}:%{version}-%{release}
Provides:       almalinux-release-eula
Provides:       centos-release-eula
Provides:       redhat-release-eula

# In place of AlmaLinux's, as its EL release.
Provides:       almalinux-release = %{el_major}.%{el_minor}
Obsoletes:      almalinux-release < %{el_major}.99
Provides:       redhat-release = %{el_major}.%{el_minor}

# required by dnf
# https://github.com/rpm-software-management/dnf/blob/4.2.23/dnf/const.py.in#L26
Provides:       system-release = %{el_major}.%{el_minor}
Provides:       system-release(releasever) = %{el_major}
Provides:       system-release(releasever_major) = %{el_major}
Provides:       system-release(releasever_minor) = %{el_minor}

# required by libdnf
# https://github.com/rpm-software-management/libdnf/blob/0.48.0/libdnf/module/ModulePackage.cpp#L472
Provides:       base-module(platform:el%{el_major})

Source200:      EULA
Source201:      LICENSE

Source300:      85-display-manager.preset
Source301:      90-default.preset
Source302:      90-default-user.preset
Source303:      99-default-disable.preset
Source304:      50-redhat.conf

Source500:      igos.repo
Source501:      bayu.repo

Source600:      RPM-GPG-KEY-AlmaLinux-10
Source601:      RPM-GPG-KEY-ign2026

Source700:      macros.x86_64_v2

%package -n ign-repos
Summary:        %{distro} package repositories
Requires:       ign-release = %{epoch}:%{version}-%{release}
# Required by CentOS SIGs release packages
Provides:       centos-stream-repos = %{el_major}
# IGN's repositories take AlmaLinux's place.
Provides:       almalinux-repos = %{el_major}.%{el_minor}
Obsoletes:      almalinux-repos < %{el_major}.99

%package -n ign-gpg-keys
Summary:        %{distro} RPM keys
# Required by CentOS SIGs release packages
Provides:       centos-gpg-keys = %{el_major}
Provides:       almalinux-gpg-keys = %{el_major}.%{el_minor}
Obsoletes:      almalinux-gpg-keys < %{el_major}.99

%description
%{distro} release files.

%description -n ign-repos
This package provides the package repository files for %{distro}.

%description -n ign-gpg-keys
This package provides the RPM signature keys for %{distro}.

%install
# copy license and contributors doc here for %%license and %%doc macros
mkdir -p ./docs
cp %{SOURCE201} ./docs

# create /etc/system-release and /etc/redhat-release
install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro} release %{major}.%{minor}%{?beta: %{beta}} (%{release_name})" > %{buildroot}%{_sysconfdir}/ign-release
ln -s ign-release %{buildroot}%{_sysconfdir}/system-release
ln -s ign-release %{buildroot}%{_sysconfdir}/redhat-release

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec
%global dist_vendor IGOS Nusantara
%global dist_name   %{distro}

# The namespace for purl
# https://github.com/package-url/purl-spec
# for example as in: pkg:rpm/ign/python-setuptools@69.2.0-10.el10?arch=src"
%global dist_purl_namespace ign

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://igos-nusantara.or.id/

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://bugs.igos-nusantara.or.id/

# debuginfod server, as used in elfutils.spec.
# %global dist_debuginfod_url https://debuginfod.centos.org/
# -------------------------------------------------------------------------


# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{dist_name}"
VERSION="%{major}.%{minor} (%{release_name})"
ID="ign"
ID_LIKE="rhel centos fedora"
VERSION_ID="%{major}.%{minor}"
VERSION_CODENAME="ciremai"
PLATFORM_ID="platform:el%{el_major}"
PRETTY_NAME="%{distro} %{major}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;34"
LOGO="ign-logo-icon"
CPE_NAME="cpe:/o:ign:ign:%{major}.%{minor}"
HOME_URL="%{dist_home_url}"
DOCUMENTATION_URL="https://wiki.igos-nusantara.or.id/"
VENDOR_NAME="IGOS Nusantara"
VENDOR_URL="%{dist_home_url}"
BUG_REPORT_URL="%{dist_bug_report_url}"

IGOSNUSANTARA_MANTISBT_PROJECT="IGOS Nusantara-%{major}"
IGOSNUsANTARA_MANTISBT_PROJECT_VERSION="%{major}.%{minor}"
REDHAT_SUPPORT_PRODUCT="%{distro}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{major}.%{minor}%{?beta: %{beta}}"
SUPPORT_END=%{eol_date}
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:ign:ign:%{major}.%{minor}" > %{buildroot}%{_sysconfdir}/system-release-cpe

# create /etc/issue, /etc/issue.net and /etc/issue.d
echo '\S' > %{buildroot}%{_sysconfdir}/issue
echo 'Kernel \r on an \m' >> %{buildroot}%{_sysconfdir}/issue
cp %{buildroot}%{_sysconfdir}/issue{,.net}
echo >> %{buildroot}%{_sysconfdir}/issue
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

# set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%ign_ver %{major}
%%ign %{major}
%%centos_ver %{el_major}
%%centos %{el_major}
%%rhel %{el_major}
%%el%{el_major} 1
%%distcore            .el%{el_major}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?distsuffix}%%{?with_bootstrap:%{__bootstrap}}
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_purl_namespace %{dist_purl_namespace}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
EOF

# make ign-release a protected package
install -p -d -m 755 %{buildroot}%{_sysconfdir}/dnf/protected.d/
touch ign-release.conf
echo ign-release > ign-release.conf
install -p -c -m 0644 ign-release.conf %{buildroot}%{_sysconfdir}/dnf/protected.d/
rm -f ign-release.conf

# use unbranded datadir
install -d -m 0755 %{buildroot}%{_datadir}/ign-release
ln -s ign-release %{buildroot}%{_datadir}/redhat-release
install -p -m 0644 %{SOURCE200} %{buildroot}%{_datadir}/ign-release/

# copy systemd presets
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/user-preset
install -p -m 0644 %{SOURCE300} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE301} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE302} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# installing the same file for both system and user presets to set the same behavior for both
install -p -m 0644 %{SOURCE303} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE303} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# copy sysctl presets
mkdir -p %{buildroot}/%{_prefix}/lib/sysctl.d/
install -m 0644 %{SOURCE304} %{buildroot}/%{_prefix}/lib/sysctl.d/

# Create stub yum repos
mkdir %{buildroot}%{_sysconfdir}/yum.repos.d
touch %{buildroot}%{_sysconfdir}/yum.repos.d/redhat.repo

# copy yum repos
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE500} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE501} %{buildroot}%{_sysconfdir}/yum.repos.d/

# Replace basearch to x86_64_v2
%ifarch x86_64_v2
sed -i "s/\$basearch/x86_64_v2/g" %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo
sed -i '/^mirrorlist=/ s|$|?arch=x86_64_v2|g' %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo
%endif

# Replace $releasever variable with beta if it is set
%if %{defined beta}
sed -i "s/\$releasever/%{major}.%{minor}-beta/g" %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo
sed -i "s|https://repo.igos-nusantara.or.id/|https://vault.igos-nusantara.or.id/|g" %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo
%endif

# dnf variables
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/vars
echo "%{el_major}-stream" > %{buildroot}%{_sysconfdir}/dnf/vars/stream

# copy GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE600} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
install -p -m 0644 %{SOURCE601} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

# These variables should be set in the build environment to change rpm names
mkdir -p %{buildroot}%{_sysconfdir}/rpm
%ifarch x86_64_v2
install -p -m 0644 %{SOURCE700}  %{buildroot}%{_sysconfdir}/rpm/
%endif


%files
%license docs/LICENSE
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/ign-release
%config(noreplace) %{_sysconfdir}/os-release
%config %{_sysconfdir}/system-release-cpe
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%{_sysconfdir}/dnf/protected.d/ign-release.conf
%dir %{_sysconfdir}/yum.repos.d
%ghost %{_sysconfdir}/yum.repos.d/redhat.repo
%{_rpmmacrodir}/macros.dist
%{_datadir}/redhat-release
%{_datadir}/ign-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%{_prefix}/lib/systemd/user-preset/*
%{_prefix}/lib/sysctl.d/50-redhat.conf
%ifarch x86_64_v2
%config(noreplace) %{_sysconfdir}/rpm/macros.x86_64_v2
%endif

%files -n ign-repos
%config(noreplace) %{_sysconfdir}/yum.repos.d/igos.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/bayu.repo
%config(noreplace) %{_sysconfdir}/dnf/vars/stream

%files -n ign-gpg-keys
%{_sysconfdir}/pki/rpm-gpg

%changelog
* Fri Oct 30 2026 Eka Tresna Irawan <anak10thn@gmail.com> - 1:26.1-9
- Codename Ciremai: IGOS Nusantara 26 (Ciremai) as PRETTY_NAME, shown as the
  system version

* Thu Oct 29 2026 Eka Tresna Irawan <anak10thn@gmail.com> - 1:26.1-8
- Provide redhat-release, system-release and $releasever as EL 10.2, with
  %%rhel 10 and platform:el10: EL 10 and EPEL 10 packages such as
  epel-release installed no longer (issue #100)
- ign-repos: IGN's repositories on R2 (igos.repo) and Bayu's (bayu.repo), in
  place of the 2026 paths that no host serves; replaces almalinux-repos
- Epoch 1, above the 2026.1 packages

* Sun Feb 1 2026 Nana Suryana <bantuan@igos-nusantara.or.id> - 2026.1-16
- 2026.1 stable
