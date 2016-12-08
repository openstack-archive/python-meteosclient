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


class Template(base.Resource):
    resource_name = 'Template'


class TemplateManager(base.ResourceManager):
    resource_class = Template
    NotUpdated = base.NotUpdated()

    def create(self, display_name=None, display_description=None,
               image_id=None, master_nodes_num=None, master_flavor_id=None,
               worker_nodes_num=None, worker_flavor_id=None,
               spark_version=None, floating_ip_pool=None):
        """Create a Experiment Template."""

        data = {
            'display_name': display_name,
            'display_description': display_description,
            'image_id': image_id,
            'master_nodes_num': master_nodes_num,
            'master_flavor_id': master_flavor_id,
            'worker_nodes_num': worker_nodes_num,
            'worker_flavor_id': worker_flavor_id,
            'spark_version': spark_version,
            'floating_ip_pool': floating_ip_pool,
        }

        body = {'template': data}

        return self._create('/templates', body, 'template')

    def list(self, search_opts=None, limit=None, marker=None,
             sort_by=None, reverse=None):
        """Get a list of Experiment Templates."""
        query = base.get_query_string(search_opts, limit=limit, marker=marker,
                                      sort_by=sort_by, reverse=reverse)
        url = "/templates%s" % query
        return self._page(url, 'templates', limit)

    def get(self, template_id, show_progress=False):
        """Get information about a Template."""
        url = ('/templates/%(template_id)s?%(params)s' %
               {"template_id": template_id,
                "params": parse.urlencode({"show_progress": show_progress})})

        return self._get(url, 'template')

    def delete(self, template_id):
        """Delete a Experiment Template."""
        self._delete('/templates/%s' % template_id)
