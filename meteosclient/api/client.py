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

import warnings

from keystoneauth1 import adapter
from keystoneauth1 import exceptions
from keystoneauth1.identity import v2
from keystoneauth1.identity import v3
from keystoneauth1 import session as keystone_session
from keystoneauth1 import token_endpoint

from meteosclient.api import templates
from meteosclient.api import experiments
from meteosclient.api import datasets
from meteosclient.api import models
from meteosclient.api import model_evaluations
from meteosclient.api import learnings


USER_AGENT = 'python-meteosclient'


class HTTPClient(adapter.Adapter):

    def request(self, *args, **kwargs):
        kwargs.setdefault('raise_exc', False)
        return super(HTTPClient, self).request(*args, **kwargs)


class Client(object):
    """Client for the OpenStack Data Processing v1 API.

        :param str username: Username for Keystone authentication.
        :param str api_key: Password for Keystone authentication.
        :param str project_id: Keystone Tenant id.
        :param str project_name: Keystone Tenant name.
        :param str auth_url: Keystone URL that will be used for authentication.
        :param str meteos_url: Meteos REST API URL to communicate with.
        :param str endpoint_type: Desired Meteos endpoint type.
        :param str service_type: Meteos service name in Keystone catalog.
        :param str input_auth_token: Keystone authorization token.
        :param session: Keystone Session object.
        :param auth: Keystone Authentication Plugin object.
        :param boolean insecure: Allow insecure.
        :param string cacert: Path to the Privacy Enhanced Mail (PEM) file
                              which contains certificates needed to establish
                              SSL connection with the identity service.
        :param string region_name: Name of a region to select when choosing an
                                   endpoint from the service catalog.
    """
    def __init__(self, username=None, api_key=None, project_id=None,
                 project_name=None, auth_url=None, meteos_url=None,
                 endpoint_type='publicURL', service_type='machine-learning',
                 input_auth_token=None, session=None, auth=None,
                 insecure=False, cacert=None, region_name=None, **kwargs):

        if not session:
            warnings.simplefilter('once', category=DeprecationWarning)
            warnings.warn('Passing authentication parameters to meteosclient '
                          'is deprecated. Please construct and pass an '
                          'authenticated session object directly.',
                          DeprecationWarning)
            warnings.resetwarnings()

            if input_auth_token:
                auth = token_endpoint.Token(meteos_url, input_auth_token)

            else:
                auth = self._get_keystone_auth(auth_url=auth_url,
                                               username=username,
                                               api_key=api_key,
                                               project_id=project_id,
                                               project_name=project_name)

            verify = True
            if insecure:
                verify = False
            elif cacert:
                verify = cacert

            session = keystone_session.Session(verify=verify)

        if not auth:
            auth = session.auth

        # NOTE(Toan): bug #1512801. If meteos_url is provided, it does not
        # matter if service_type is orthographically correct or not.
        # Only find Meteos service_type and endpoint in Keystone catalog
        # if meteos_url is not provided.
        if not meteos_url:
            service_type = self._determine_service_type(session,
                                                        auth,
                                                        service_type,
                                                        endpoint_type)

        kwargs['user_agent'] = USER_AGENT
        kwargs.setdefault('interface', endpoint_type)
        kwargs.setdefault('endpoint_override', meteos_url)

        client = HTTPClient(session=session,
                            auth=auth,
                            service_type=service_type,
                            region_name=region_name,
                            **kwargs)

        self.templates = templates.TemplateManager(client)
        self.experiments = experiments.ExperimentManager(client)
        self.datasets = datasets.DatasetManager(client)
        self.models = models.ModelManager(client)
        self.model_evaluations = model_evaluations.ModelEvaluationManager(client)
        self.learnings = learnings.LearningManager(client)

    def _get_keystone_auth(self, username=None, api_key=None, auth_url=None,
                           project_id=None, project_name=None):
        if not auth_url:
            raise RuntimeError("No auth url specified")

        if 'v2.0' in auth_url:
            return v2.Password(auth_url=auth_url,
                               username=username,
                               password=api_key,
                               tenant_id=project_id,
                               tenant_name=project_name)
        else:
            # NOTE(jamielennox): Setting these to default is what
            # keystoneclient does in the event they are not passed.
            return v3.Password(auth_url=auth_url,
                               username=username,
                               password=api_key,
                               user_domain_id='default',
                               project_id=project_id,
                               project_name=project_name,
                               project_domain_id='default')

    @staticmethod
    def _determine_service_type(session, auth, service_type, interface):
        """Check a catalog for machine-learning or data_processing"""

        # NOTE(jamielennox): calling get_endpoint forces an auth on
        # initialization which is required for backwards compatibility. It
        # also allows us to reset the service type if not in the catalog.
        for st in (service_type, service_type.replace('-', '_')):
            try:
                url = auth.get_endpoint(session,
                                        service_type=st,
                                        interface=interface)
            except exceptions.Unauthorized:
                raise RuntimeError("Not Authorized")
            except exceptions.EndpointNotFound:
                # NOTE(jamielennox): bug #1428447. This should not be
                # raised, instead None should be returned. Handle in case
                # it changes in the future
                url = None

            if url:
                return st

        raise RuntimeError("Could not find Meteos endpoint in catalog")
