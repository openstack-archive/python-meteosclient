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


class ModelEvaluation(base.Resource):
    resource_name = 'ModelEvaluation'


class ModelEvaluationManager(base.ResourceManager):
    resource_class = ModelEvaluation
    NotUpdated = base.NotUpdated()

    def create(self, display_name=None, model_id=None,
               source_dataset_url=None, dataset_format=None):
        """Create a ModelEvaluation."""

        data = {
            'display_name': display_name,
            'model_id': model_id,
            'source_dataset_url': source_dataset_url,
            'dataset_format': dataset_format,
        }

        body = {'model_evaluation': data}

        return self._create('/model_evaluations', body, 'model_evaluation')

    def list(self, search_opts=None, limit=None, marker=None,
             sort_by=None, reverse=None):
        """Get a list of ModelEvaluations."""
        query = base.get_query_string(search_opts, limit=limit, marker=marker,
                                      sort_by=sort_by, reverse=reverse)
        url = "/model_evaluations%s" % query
        return self._page(url, 'model_evaluations', limit)

    def get(self, model_evaluation_id, show_progress=False):
        """Get information about a ModelEvaluation."""
        url = ('/model_evaluations/%(model_evaluation_id)s?%(params)s' %
               {"model_evaluation_id": model_evaluation_id,
                "params": parse.urlencode({"show_progress": show_progress})})

        return self._get(url, 'model_evaluation')

    def delete(self, model_evaluation_id):
        """Delete a ModelEvaluation."""
        self._delete('/model_evaluations/%s' % model_evaluation_id)
