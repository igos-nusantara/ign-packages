#!/usr/bin/env bash
# Publishes out/'s binary RPMs to IGN's repository: into 26/ign on the repo
# host, whose metadata is rebuilt and signed there (/opt/repo-sync/createrepo.sh),
# then mirrored to R2 (r2:repo/26/ign), where installed systems read it.
# Needs SSH to the host, with sudo and its rclone remote "r2".
#   REPO_HOST=igos@103.175.219.85
set -Eeuo pipefail
ROOT=$(realpath "$(dirname "$0")")
HOST=${REPO_HOST:-igos@103.175.219.85}
DIR=/var/www/html/26/ign

shopt -s nullglob
rpms=("$ROOT"/out/*.noarch.rpm "$ROOT"/out/*.x86_64.rpm)
((${#rpms[@]})) || { echo "No RPMs in out/; run ./build.sh first" >&2; exit 1; }

scp -q "${rpms[@]}" "$HOST:/tmp/"
names=$(printf '%s ' "${rpms[@]##*/}")
ssh -o BatchMode=yes "$HOST" bash --norc -euc "'
  cd /tmp
  # createrepo.sh writes the metadata as apache.
  sudo chown -R apache: $DIR
  sudo install -o apache -g apache -m 0644 $names $DIR/
  rm -f $names
  # Every package, the new ones and any published before signing was.
  for f in $DIR/*.rpm; do
    rpm -qp --qf \"%{SIGPGP:pgpsig}\" \"\$f\" 2>/dev/null | grep -q \"Key ID\" && continue
    sudo env GNUPGHOME=/opt/repo-sync/gnupg rpmsign --addsign \\
      --define \"_gpg_name repo@igos-nusantara.or.id\" \"\$f\" >/dev/null
    echo \"signed \${f##*/}\"
  done
  sudo /opt/repo-sync/createrepo.sh ign
  export RCLONE_CONFIG=\$HOME/.config/rclone/rclone.conf
  rclone sync $DIR r2:repo/26/ign --exclude index.html --checksum --stats-one-line -v 2>&1 | tail -1
'"
echo "Published: $names"
