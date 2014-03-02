# System packages
class system {
    # Update package list
    exec { 'apt-get update':
        path => '/usr/bin',
    }

    # Development tools
    package { ['vim',
               'tmux',
               'htop',
               'tree',
               'make',
               'pkg-config',
               'graphviz',
               'libgraphviz-dev']:
        ensure => installed,
        require => Exec['apt-get update'],
    }

    # Python package dependencies
    package { [ # Theano dependencies
               'python-numpy',
               'python-scipy',
               'python-dev',
               'python-pip',
               'python-nose',
               'g++',
               'libopenblas-dev',
               'git',
               # neo dependencies
               'libhdf5-serial-dev',
               'cython',
               # gtk3 stuff
               'gir1.2-gtk-3.0',
               'python-gi',
               # matplotlib dependencies
               'libpng12-dev',
               'libfreetype6-dev']:
        ensure => installed,
        require => Exec['apt-get update'],
    }
}

# Python packages
class python {
    package { ['Theano',
               'quantities',
               'numexpr',
               'tables',
               'neo',
               'ipython',
               'pytest',
               'sphinx',
               'networkx',
               'pygraphviz',
               'distribute',
               'matplotlib',
               'git+git://github.com/mcchong/nengo.git',
               'git+git://github.com/amtinits/nengo_theano.git']:
        ensure => installed,
        provider => 'pip',
    }
}

# Run the classes
class { 'system': }
class { 'python':
    require => Class['system'],
}
