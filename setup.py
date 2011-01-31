# Distutils script using distutils2 setup.cfg to call the
# distutils.core.setup() with the right args.

import os
from distutils.core import setup
from ConfigParser import RawConfigParser

def generate_distutils_kwargs_from_setup_cfg(file='setup.cfg'):
    """ Distutils2 to distutils1 compatibility util.

        This method uses an existing setup.cfg to generate a dictionnary of
        keywords that can be used by distutils.core.setup(kwargs**).

        :param file:
            The setup.cfg path.
        :raises DistutilsFileError:
            When the setup.cfg file is not found.

    """
    # We need to declare the following constants here so that it's easier to
    # generate the setup.py afterwards, using inspect.getsource.
    D1_D2_SETUP_ARGS = {
        # D1 name             : (D2_section, D2_name)
        "name"                : ("metadata",),
        "version"             : ("metadata",),
        "author"              : ("metadata",),
        "author_email"        : ("metadata",),
        "maintainer"          : ("metadata",),
        "maintainer_email"    : ("metadata",),
        "url"                 : ("metadata", "home_page"),
        "description"         : ("metadata", "summary"),
        "long_description"    : ("metadata", "description"),
        "download-url"        : ("metadata",),
        "classifiers"         : ("metadata", "classifier"),
        "platforms"           : ("metadata", "platform"), # Needs testing
        "license"             : ("metadata",),
        "requires"            : ("metadata", "requires_dist"),
        "provides"            : ("metadata", "provides_dist"), # Needs testing
        "obsoletes"           : ("metadata", "obsoletes_dist"), # Needs testing
    
        "packages"            : ("files",),
        "scripts"             : ("files",),
        "py_modules"          : ("files", "modules"), # Needs testing
    }

    MULTI_FIELDS = ("classifiers",
                    "requires",
                    "platforms",
                    "packages",
                    "scripts")

    def has_get_option(config, section, option):
        if config.has_option(section, option):
            return config.get(section, option)
        elif config.has_option(section, option.replace('_', '-')):
            return config.get(section, option.replace('_', '-'))
        else:
            return False

    # The method source code really starts here.
    config = RawConfigParser()
    if not os.path.exists(file):
        raise DistutilsFileError("file '%s' does not exist" %
                                 os.path.abspath(file))
    config.read(file)

    kwargs = {}
    for arg in D1_D2_SETUP_ARGS:
        if len(D1_D2_SETUP_ARGS[arg]) == 2:
            # The distutils field name is different than distutils2's.
            section, option = D1_D2_SETUP_ARGS[arg]

        elif len(D1_D2_SETUP_ARGS[arg]) == 1:
            # The distutils field name is the same thant distutils2's.
            section = D1_D2_SETUP_ARGS[arg][0]
            option = arg

        in_cfg_value = has_get_option(config, section, option)
        if not in_cfg_value:
            # There is no such option in the setup.cfg
            if arg == "long_description":
                filename = has_get_option(config, section, "description_file")
                print "We have a filename", filename
                if filename:
                    in_cfg_value = open(filename).read()
            else:
                continue

        if arg in MULTI_FIELDS:
            # Special behaviour when we have a multi line option
            if "\n" in in_cfg_value:
                in_cfg_value = in_cfg_value.strip().split('\n')
            else:
                in_cfg_value = list((in_cfg_value,))

        kwargs[arg] = in_cfg_value

    return kwargs


kwargs = generate_distutils_kwargs_from_setup_cfg()
setup(**kwargs)
