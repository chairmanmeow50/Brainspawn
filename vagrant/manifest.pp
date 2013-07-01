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
               'tree']:
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
               'python-numexpr',
               'cython',
               # matplotlib
               'python-matplotlib']:
        ensure => installed,
        require => Exec['apt-get update'],
    }
}

# Python packages
class python {
    package { ['Theano',
               'quantities',
               'tables',
               'neo',
               'ipython',
               'pytest',
               'sphinx',
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
