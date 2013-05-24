# Brainspawn Vagrant Box

This is a Vagrant + Puppet configuration with the dependencies for Nengo and
Brainspawn.

1. Install [Virtualbox][0] and [Vagrant][1] if don't have them already.
1. Edit the `Vagrantfile` to change the synced folder settings to suit your
needs. These are the lines starting with `config.vm.synced_folder`. See the
[Vagrant Documentation][2] for more information.
1. Boot the VM with `vagrant up`.  This will take a while, since it'll be
downloading a base Ubuntu image for the VM, booting the machine, and installing
packages.
1. Once booted, you can SSH into the box. You'll want to enable X forwarding, so
run a command like this: `vagrant ssh -- -Y`

[0]: https://www.virtualbox.org/wiki/Downloads
[1]: http://docs.vagrantup.com/v2/installation/index.html
[2]: http://docs.vagrantup.com/v2/synced-folders/basic_usage.html
