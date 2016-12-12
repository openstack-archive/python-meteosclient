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


class Learning(base.Resource):
    resource_name = 'Learning'


class LearningManager(base.ResourceManager):
    resource_class = Learning
    NotUpdated = base.NotUpdated()

    def create(self, display_name=None, display_description=None,
               model_id=None, method=None, args=None):
        """Create a Learning."""

        data = {
            'display_name': display_name,
            'display_description': display_description,
            'model_id': model_id,
            'method': method,
            'args': base64.b64encode(str(args)),
        }

        body = {'learning': data}

        return self._create('/learnings', body, 'learning')

    def list(self, search_opts=None, limit=None, marker=None,
             sort_by=None, reverse=None):
        """Get a list of Learnings."""
        query = base.get_query_string(search_opts, limit=limit, marker=marker,
                                      sort_by=sort_by, reverse=reverse)
        url = "/learnings%s" % query
        return self._page(url, 'learnings', limit)

    def get(self, learning_id, show_progress=False):
        """Get information about a Learning."""
        url = ('/learnings/%(learning_id)s?%(params)s' %
               {"learning_id": learning_id,
                "params": parse.urlencode({"show_progress": show_progress})})

        return self._get(url, 'learning')

    def delete(self, learning_id):
        """Delete a Learning."""
        self._delete('/learnings/%s' % learning_id)
