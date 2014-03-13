# System packages
class system {
    # Update package list
    exec { 'apt-get update':
        path => '/usr/bin',
    }

    # Development tools
    package { ['vim',
               'tmux',
               'git',
               'htop',
               'tree',
               'build-essential',
               'pkg-config']:
        ensure => installed,
        require => Exec['apt-get update'],
    }

    # Python package dependencies
    package { ['python-numpy',
               'python-scipy',
               'python-dev',
               'python-pip',
               # gtk3 stuff
               'gir1.2-gtk-3.0',
               'python-gi-cairo',
               # matplotlib dependencies
               'python-gtk2-dev',
               'libpng12-dev',
               'libfreetype6-dev',
               # networkx dependencies
               'graphviz',
               'libgraphviz-dev']:
        ensure => installed,
        require => Exec['apt-get update'],
    }
}

# Python packages round 1
class python1 {
    package { ['ipython',
               'pytest',
               'sphinx',
               'distribute',
               'networkx',
               'pygraphviz',
               'git+git://github.com/mcchong/nengo.git']:
        ensure => latest,
        provider => 'pip',
    }
}

# Python packages round 2
class python2 {
    package { ['matplotlib']:
        ensure => latest,
        provider => 'pip',
    }
}

# Run the classes
class { 'system': }
class { 'python1':
    require => Class['system'],
}
class { 'python2':
    require => Class['python1'],
}
