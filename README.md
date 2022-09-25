# Who needs it?

*Fedora Silverblue* users with *SecureBoot* enabled and `akmod`s such as `akmod-nvidia` or `akmod-VirtualBox`.

# What is akmods-keys?

`akmods-keys` provides my solution for [Issue 272](https://github.com/fedora-silverblue/issue-tracker/issues/272) on Fedora Silverblue.

On Fedora Workstation, `akmods` signs the kernel modules it creates in its `%post` operation.

On Fedora Silverblue, the signing does not work because the keys, which are typically stored in `/etc/pki/akmods/{certs,private}`, are [not accessible](https://github.com/fedora-silverblue/issue-tracker/issues/272#issuecomment-1161463356).

`akmods-keys` solves this issue with @travier's [idea](https://github.com/fedora-silverblue/issue-tracker/issues/272#issuecomment-1143474213).

# How does it work?

Basic idea:

- We create a local package `akmods-keys` that provides these keys in `/etc/pki/akmods-keys/{certs,private}`.
- We let the original `akmods` use them, but with the configuration in `/etc/rpm/macros.kmodtool` that points to our keys in `akmods-keys`.

# How to ..

## .. use this project?

```sh
### Requirements ###
rpm-ostree install rpmdevtools

### Install your Machine Owner Key (MOK) ###
kmodgenca
mokutil --import /etc/pki/akmods/certs/public_key.der

### Build akmods-keys
bash setup.sh
rpm-ostree install akmods-keys-0.0.2-8.fc$(rpm -E %fedora).noarch.rpm
```
Note: `setup.sh` is very rudimentary. Please check before using.

## .. install modules?

I tested it with
```sh
rpm-ostree install akmod-nvidia akmod-VirtualBox
```
The modules are automatically signed.


# Quriks

Some notes to myself :)

## Check if the module is signed

OSTrees are located in `/sysroot/ostree/deploy/fedora/deploy/`.

This command was handy for me to find out whether `akmods` signed a module after an `rpm-ostree` operation without rebooting the system.

```sh
modinfo -F signature /sysroot/ostree/deploy/fedora/deploy/(rpm-ostree status --json | jq -r ".deployments[0].checksum").0/usr/lib/modules/*/extra/nvidia*/nvidia.ko.xz
```

# FAQ

## What is the status of this project?

It works for me. Hopefully also for you. I did not do any deep testing with it.

## Why do you use `/etc/pki/akmods-keys` in contrast to `/etc/pki/akmods`?

To be honest, this was the first solution that worked for me. Maybe they could also be placed in `/etc/pki/akmods,` but I thought it would be a good idea to have a unique place that does not lead to conflicts.

## Are the keys readable by regular users?

I checked the key location in
```
ls -al /sysroot/ostree/deploy/fedora/deploy/(rpm-ostree status --json | jq ".deployments[0].checksum" | sed 's/"//g').0/etc/pki/akmods-keys/{certs,private}
Permission denied (os error 13)
```
They seem to be readable by root only.
However, I'd recommend deleting the `akmods-keys-0.0.2-8.fc36.noarch.rpm` file.

## Is this the final solution?

No. It is still a [work-around](https://github.com/fedora-silverblue/issue-tracker/issues/272#issuecomment-1160653984), although it works pretty well (at least for me).

According to [@travier](https://github.com/travier), the ideal solution would be (https://github.com/fedora-silverblue/issue-tracker/issues/272#issuecomment-1160653984):

> The only potential fix that I'm aware of would be to store those keys into the kernel keyring and then request them while building the module during the rpm-ostree transaction.

This is something that `akmods-keys` cannot accomplish (or at least I don't know how), and Fedora Silverblue would have to adopt.
Any further development/investigation should be moved to the CoreOS issue: https://github.com/coreos/rpm-ostree/issues/3885


# Acknowledgements

- Thanks to [@nelsonaloysio](https://github.com/nelsonaloysio) for all the help with signed modules, `akmods` and for showing me [how to create RPM spec files and build them](https://github.com/nelsonaloysio/build-kmod-nvidia-signed-rpm).
- Thanks to [@travier](https://github.com/travier). Actually, he described exactly this solution in his [first answer](https://github.com/fedora-silverblue/issue-tracker/issues/272#issuecomment-1143474213), but I was unable to understand it. His further answers help me to do so.
- Thanks to [@NVieville](https://github.com/NVieville) for the idea with [/etc/rpm/macros/macros.kmodtool](https://github.com/fedora-silverblue/issue-tracker/issues/272#issuecomment-1161356618)
