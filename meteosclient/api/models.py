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

import base64
from six.moves.urllib import parse

from meteosclient.api import base


class Model(base.Resource):
    resource_name = 'Model'


class ModelManager(base.ResourceManager):
    resource_class = Model
    NotUpdated = base.NotUpdated()

    def create(self, display_name=None, display_description=None,
               source_dataset_url=None, experiment_id=None,
               model_type=None, model_params=None, dataset_format=None,
               swift_tenant=None, swift_username=None,
               swift_password=None):
        """Create a Model."""

        data = {
            'display_name': display_name,
            'display_description': display_description,
            'source_dataset_url': source_dataset_url,
            'experiment_id': experiment_id,
            'model_type': model_type,
            'model_params': base64.b64encode(model_params),
            'dataset_format': dataset_format,
            'swift_tenant': swift_tenant,
            'swift_username': swift_username,
            'swift_password': swift_password,
        }

        body = {'model': data}

        return self._create('/models', body, 'model')

    def list(self, search_opts=None, limit=None, marker=None,
             sort_by=None, reverse=None):
        """Get a list of Model Models."""
        query = base.get_query_string(search_opts, limit=limit, marker=marker,
                                      sort_by=sort_by, reverse=reverse)
        url = "/models%s" % query
        return self._page(url, 'models', limit)

    def get(self, model_id, show_progress=False):
        """Get information about a Model."""
        url = ('/models/%(model_id)s?%(params)s' %
               {"model_id": model_id,
                "params": parse.urlencode({"show_progress": show_progress})})

        return self._get(url, 'model')

    def delete(self, model_id):
        """Delete a Model Model."""
        self._delete('/models/%s' % model_id)

    def load(self, model_id):
        """Load a Model."""
        url = '/models/%s/action' % model_id
        body = {'os-load': None}

        self._post(url, body)

    def unload(self, model_id):
        """Unload a Model."""
        url = '/models/%s/action' % model_id
        body = {'os-unload': None}

        self._post(url, body)

    def recreate(self, model_id, display_name=None, display_description=None,
                 source_dataset_url=None, model_type=None, model_params=None,
                 dataset_format=None, swift_tenant=None, swift_username=None,
                 swift_password=None):
        """Recreate a Model."""

        data = {
            'display_name': display_name,
            'display_description': display_description,
            'source_dataset_url': source_dataset_url,
            'model_type': model_type,
            'model_params': base64.b64encode(model_params),
            'dataset_format': dataset_format,
            'swift_tenant': swift_tenant,
            'swift_username': swift_username,
            'swift_password': swift_password,
        }

        url = '/models/%s/action' % model_id
        body = {'os-recreate': data}

        return self._post(url, body, 'model')
