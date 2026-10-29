Name:           ign-config
Version:        26
Release:        1
Summary:        IGOS Nusantara terminal defaults: bash prompt and aliases, tmux, fastfetch
License:        GPL-3.0-or-later
URL:            https://github.com/igosnusantara/config
BuildArch:      noarch
Source0:        ign.sh
Source1:        tmux.conf
Source2:        fastfetch.jsonc
Source3:        ign-fastfetch.txt

%description
IGOS Nusantara's terminal defaults, system-wide, from igosnusantara/config: a
colored prompt (red for root, its own inside tmux), aliases (ll, .., rm -i,
df -h, update/install/search for dnf...) and the ex extract function for
interactive bash; tmux with the prefix C-a, the mouse, v/h splits and Alt to
move between panes; and fastfetch with the IGOS Nusantara logo. A user's
~/.bashrc, ~/.tmux.conf and fastfetch config still win.

%prep

%build

%install
install -D -p -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/profile.d/ign.sh
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/tmux.conf
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/fastfetch/config.jsonc
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/ign-config/ign-fastfetch.txt

%files
%config(noreplace) %{_sysconfdir}/profile.d/ign.sh
%config(noreplace) %{_sysconfdir}/tmux.conf
%config(noreplace) %{_sysconfdir}/xdg/fastfetch/config.jsonc
%{_datadir}/ign-config

%changelog
* Thu Oct 29 2026 Eka Tresna Irawan <anak10thn@gmail.com> - 26-1
- From igosnusantara/config (igos-nusantara/bayu#99): the prompt, aliases and
  ex in /etc/profile.d, tmux in /etc/tmux.conf, fastfetch's logo in
  /etc/xdg/fastfetch; M-Down goes down, C-a r reloads /etc/tmux.conf, ex
  quotes its file, without the dnf wrapper, the date alias and
  ign-config-update
