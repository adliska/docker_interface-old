# Copyright 2018 Spotify AB

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from .base import Plugin, ExecutePlugin


class GoogleCloudCredentialsPlugin(Plugin):
    """
    Mount Google Cloud credentials in the Docker container.
    """
    ORDER = 560
    COMMANDS = ['run']

    def apply(self, configuration, schema, args):
        configuration['run'].setdefault('mount', []).append({
            'type': 'bind',
            'source': '${env/HOME}/.config/gcloud',
            'destination': '#{/run/env/HOME}/.config/gcloud'
        })
        return configuration


class GoogleContainerRegistryPlugin(ExecutePlugin):
    """
    Configure docker authorization for Google services such as Google Container Registry.
    """
    # We want to authorize before any other plugins that may depend on access to Google's services.
    ORDER = 10
    COMMANDS = 'all'
    ENABLED = False

    def build_command(self, configuration):
        return ['gcloud', 'docker', '--authorize-only', '--quiet']
