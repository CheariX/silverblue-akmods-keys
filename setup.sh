#!/bin/sh

set -e

mkdir -p ./rpmbuild/SOURCES
mkdir -p ./tmp

sudo cp \
  macros.kmodtool \
  /etc/pki/akmods/private/private_key.priv \
  /etc/pki/akmods/certs/public_key.der \
  ./rpmbuild/SOURCES

// This makes your private key accessible 
// to your current user and its programs.
// DO NOT DO THIS IF YOU ARE NOT SURE
sudo setfacl -R -m $USER:r ./rpmbuild/SOURCES

// Use toolbox instead of rpm-ostree, to
// keep layered packages as minimal as possible
toolbox run sudo dnf install -y bubblewrap rpmdevtools

// Setup a chroot-like environment to isolate 
// user home directory from the real one.
// The current directory becomes the home directory.
toolbox run bwrap \
    --proc /proc \
    --ro-bind /usr /usr \
    --ro-bind /var/lib /var/lib \
    --ro-bind /etc /etc \
    --symlink usr/lib64 /lib64 \
    --symlink usr/bin /bin \
    --symlink usr/sbin /sbin \
    --bind . /home \
    --dev-bind /dev/null /dev/null \
    --tmpfs /var/tmp \
    --symlink var/tmp /tmp \
    --tmpfs /run/user \
    --unshare-all \
    --uid 1000 --gid 1000 \
    --hostname fedora \
    --clearenv \
    --setenv PATH /usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin \
    --setenv HOME /home \
    --setenv XDG_RUNTIME_DIR /run/user/1000 \
    --chdir /home \
    rpmbuild -ba akmods-keys.spec

// Clean up unnecessary messes
mv ./rpmbuild/RPMS/noarch/* .
rm -rf ./rpmbuild
