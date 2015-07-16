#!/usr/bin/env python
#
# Copyright 2014 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Takes care of the basic setup of the config files and does some preliminary
sanity checks
"""
import os


from configobj import ConfigObj


nova_creds = None


def run_config():
    """
    Runs sanity checks and prepares the global nova_creds variable
    """
    global nova_creds
    check_environment_presets()
    nova_creds = load_config()


def check_environment_presets():
    """
    Checks for environment variables that can cause problems with supernova
    """
    presets = [x for x in os.environ.copy().keys() if x.startswith('NOVA_') or
               x.startswith('OS_')]
    if len(presets) < 1:
        return True
    else:
        print("_" * 80)
        print("*WARNING* Found existing environment variables that may "
              "cause conflicts:")
        for preset in presets:
            print("  - %s" % preset)
        print("_" * 80)
        return False


def load_config(config_file_override=None):
    """
    Pulls the supernova configuration file and reads it
    """
    supernova_config = get_config_file(config_file_override)

    # Can we successfully read the configuration file?
    nova_creds = ConfigObj(supernova_config)

    return nova_creds


def get_config_file(override_files=None):
    """
    Looks for the most specific configuration file available.  An override
    can be provided as a string if needed.
    """
    if override_files:
        if isinstance(override_files, list):
            possible_configs = override_files
        else:
            raise Exception("Config file override must be a list of paths")
    else:
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.expanduser('~/.config')
        possible_configs = [os.path.join(xdg_config_home, "supernova"),
                            os.path.expanduser("~/.supernova"),
                            ".supernova"]

    for config_file in reversed(possible_configs):
        if os.path.isfile(config_file):
            return config_file

    raise Exception("Couldn't find a valid configuration file to parse")
