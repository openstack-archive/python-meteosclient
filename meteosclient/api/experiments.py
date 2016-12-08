# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from six.moves.urllib import parse

from meteosclient.api import base


class Experiment(base.Resource):
    resource_name = 'Experiment'


class ExperimentManager(base.ResourceManager):
    resource_class = Experiment
    NotUpdated = base.NotUpdated()

    def create(self, display_name=None, display_description=None,
               template_id=None, key_name=None,
               neutron_management_network=None):
        """Create a Experiment."""

        data = {
            'display_name': display_name,
            'display_description': display_description,
            'template_id': template_id,
            'key_name': key_name,
            'neutron_management_network': neutron_management_network,
        }

        body = {'experiment': data}

        return self._create('/experiments', body, 'experiment')

    def list(self, search_opts=None, limit=None, marker=None,
             sort_by=None, reverse=None):
        """Get a list of Experiment Experiments."""
        query = base.get_query_string(search_opts, limit=limit, marker=marker,
                                      sort_by=sort_by, reverse=reverse)
        url = "/experiments%s" % query
        return self._page(url, 'experiments', limit)

    def get(self, experiment_id, show_progress=False):
        """Get information about a Experiment."""
        url = ('/experiments/%(experiment_id)s?%(params)s' %
               {"experiment_id": experiment_id,
                "params": parse.urlencode({"show_progress": show_progress})})

        return self._get(url, 'experiment')

    def delete(self, experiment_id):
        """Delete a Experiment Experiment."""
        self._delete('/experiments/%s' % experiment_id)
