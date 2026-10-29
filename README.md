# IGN packages

Sources of the IGOS Nusantara 26 packages that make a system IGN, as opposed
to AlmaLinux, and the scripts that build and publish them:

| Package | What it is |
|---|---|
| `ign-release` | `/etc/os-release` and the release files, the dist macros, systemd presets; with `ign-repos` (`/etc/yum.repos.d/igos.repo`, `bayu.repo`) and `ign-gpg-keys` |
| `ign-logos` | IGN's logos and pictures (anaconda, boot loader, icons, backgrounds), with `ign-logos-httpd` and `ign-logos-classic` |
| `ign-berkas` | IGN's own files, in `/usr/share/ign-berkas` |
| `ign-config` | IGN's terminal defaults from [igosnusantara/config](https://github.com/igosnusantara/config), system-wide: the bash prompt, aliases and `ex` (`/etc/profile.d/ign.sh`), tmux (`/etc/tmux.conf`) and fastfetch's IGN logo (`/etc/xdg/fastfetch`); a user's own files win |

Each directory holds its `.spec` and its sources.

## Enterprise Linux compatibility

IGN 26 is built on AlmaLinux 10.2, and its packages and EPEL 10's ask for the
EL release, not IGN's: `ign-release` provides `redhat-release`,
`system-release` and `$releasever` as **10.2**, `platform:el10`, and
`%rhel 10` / `%dist .el10`. IGN 26.1 is the name in `/etc/os-release` only.
With 2026 there, EPEL's `epel-release` and anything asking for EL 10 failed to
install (issue igos-nusantara/bayu#100).

`ign-release`, `ign-repos` and `ign-gpg-keys` replace AlmaLinux's
(`Obsoletes`), and `ign-logos` stands for AlmaLinux's desktop backgrounds,
which would otherwise pull `almalinux-logos` in over IGN's files
(igos-nusantara/bayu#82).

All of them have **Epoch 1**: the packages before them were versioned by the
year, 2026, which sorts above 26.

## Build

Needs podman. Builds in an AlmaLinux 10 container, into `out/`:

```shell
./build.sh                  # every package
./build.sh ign-release      # one
```

## Publish

Copies `out/`'s binary RPMs to the repo host's `26/ign`, rebuilds and signs its
metadata there, and mirrors it to R2 (`https://r2.igos-nusantara.or.id/26/ign/`),
where installed systems read it (the `igos-ign` repository):

```shell
./publish.sh                # REPO_HOST=igos@103.175.219.85 by default
```

Raise `Release` in the `.spec` (and add to its `%changelog`) for every change.

## License

Each package's own, in its `.spec`.
