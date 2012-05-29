#!/usr/bin/env python
#
# Copyright 2012 Major Hayden
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
import ConfigParser
import os
import re
import subprocess


class SuperNova:

    def __init__(self):
        self.nova_creds = None
        self.nova_env = None
        self.env = os.environ
        pass

    def check_deprecated_options(self):
        creds = self.get_nova_creds()
        if creds.has_option(self.nova_env, 'insecure'):
            print "WARNING: the 'insecure' option is deprecated. " \
                  "Consider using NOVACLIENT_DEBUG=1 instead."

    def get_nova_creds(self):
        if self.nova_creds:
            return self.nova_creds

        possible_configs = [os.path.expanduser("~/.supernova"), '.supernova']
        self.nova_creds = ConfigParser.RawConfigParser()
        self.nova_creds.read(possible_configs)
        return self.nova_creds

    def is_valid_environment(self):
        valid_envs = self.get_nova_creds().sections()
        return self.nova_env in valid_envs

    def prep_nova_creds(self):
        self.check_deprecated_options()
        creds = self.get_nova_creds().items(self.nova_env)
        nova_re = re.compile(r"(^nova_|^os_|^novaclient)")
        return [(x[0].upper().strip("\"'"), x[1].strip("\"'"))
            for x in creds if nova_re.match(x[0])]

    def prep_shell_environment(self):
        for k, v in self.prep_nova_creds():
            self.env[k] = v

    def run_novaclient(self, nova_args):
        self.prep_shell_environment()
        p = subprocess.Popen(['nova'] + nova_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=self.env
        )
        for line in p.stdout:
            print line.rstrip("\n")
