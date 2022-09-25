#!/bin/sh
set -e
mkdir -p /root/rpmbuild/SOURCES/
cp \
  macros.kmodtool \
  /etc/pki/akmods/private/private_key.priv \
  /etc/pki/akmods/certs/public_key.der \
  /root/rpmbuild/SOURCES
rpmbuild -ba akmods-keys.spec
mv /root/rpmbuild/RPMS/noarch/akmods-keys-0.0.2-8.fc$(rpm -E %fedora).noarch.rpm .
rm -f $(find /root/rpmbuild -type f | grep -E 'akmods-keys|public_key.der|private_key.priv|macros.kmodtool')
find /root/rpmbuild -type d | sort -r | while read d; do
  rm -df "$d" 2>/dev/null
done
