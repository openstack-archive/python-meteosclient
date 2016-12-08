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


class Dataset(base.Resource):
    resource_name = 'Dataset'


class DatasetManager(base.ResourceManager):
    resource_class = Dataset
    NotUpdated = base.NotUpdated()

    def create(self, method=None, source_dataset_url=None, display_name=None,
               display_description=None, experiment_id=None, params=None,
               swift_tenant=None, swift_username=None, swift_password=None):
        """Create a Dataset."""

        data = {
            'method': method,
            'source_dataset_url': source_dataset_url,
            'display_name': display_name,
            'display_description': display_description,
            'experiment_id': experiment_id,
            'params': base64.b64encode(str(params)),
            'swift_tenant': swift_tenant,
            'swift_username': swift_username,
            'swift_password': swift_password,
        }

        body = {'dataset': data}

        return self._create('/datasets', body, 'dataset')

    def list(self, search_opts=None, limit=None, marker=None,
             sort_by=None, reverse=None):
        """Get a list of Dataset Datasets."""
        query = base.get_query_string(search_opts, limit=limit, marker=marker,
                                      sort_by=sort_by, reverse=reverse)
        url = "/datasets%s" % query
        return self._page(url, 'datasets', limit)

    def get(self, dataset_id, show_progress=False):
        """Get information about a Dataset."""
        url = ('/datasets/%(dataset_id)s?%(params)s' %
               {"dataset_id": dataset_id,
                "params": parse.urlencode({"show_progress": show_progress})})

        return self._get(url, 'dataset')

    def delete(self, dataset_id):
        """Delete a Dataset Dataset."""
        self._delete('/datasets/%s' % dataset_id)
