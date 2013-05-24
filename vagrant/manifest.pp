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
        ensure => latest,
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
        ensure => latest,
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
               'git+git://github.com/ctn-waterloo/nengo_theano.git']:
        ensure => latest,
        provider => 'pip',
    }
}

# Run the classes
class { 'system': }
class { 'python':
    require => Class['system'],
}
