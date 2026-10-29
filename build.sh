#!/usr/bin/env bash
# Builds the IGN packages (ign-release, ign-logos, ign-berkas) from this
# repository into out/: source and binary RPMs, in an AlmaLinux 10 container.
#   ./build.sh [PACKAGE...]        default: every directory with a .spec
#   IMAGE=almalinux:10              the build container
set -Eeuo pipefail
ROOT=$(realpath "$(dirname "$0")")
IMAGE=${IMAGE:-docker.io/library/almalinux:10}
cd "$ROOT"
packages=("$@")
((${#packages[@]})) || packages=($(ls -d */ | tr -d / | while read -r d; do [ -e "$d/$d.spec" ] && echo "$d"; done))
mkdir -p out

for package in "${packages[@]}"; do
  echo "==> $package"
  podman run --rm -v "$ROOT/$package":/src:ro,Z -v "$ROOT/out":/out:Z "$IMAGE" bash -euc '
    dnf -y -q install rpm-build dnf-plugins-core >/dev/null
    dnf config-manager --set-enabled crb >/dev/null 2>&1 || true
    mkdir -p /root/rpmbuild/SOURCES /root/rpmbuild/SPECS
    cp -a /src/. /root/rpmbuild/SOURCES/
    spec=/root/rpmbuild/SOURCES/'"$package"'.spec
    dnf -y -q builddep "$spec" >/dev/null
    rpmbuild -ba "$spec" >/tmp/build.log 2>&1 || { tail -40 /tmp/build.log; exit 1; }
    cp /root/rpmbuild/SRPMS/*.src.rpm /root/rpmbuild/RPMS/*/*.rpm /out/'
done
ls -l out
