#!/bin/sh
set -e
mkdir -p /root/rpmbuild/SOURCES/
cp macros.kmodtool private_key.priv public_key.der /root/rpmbuild/SOURCES
rpmbuild -ba akmods-keys.spec
mv /root/rpmbuild/RPMS/noarch/akmods-keys-0.0.2-8.fc36.noarch.rpm .
