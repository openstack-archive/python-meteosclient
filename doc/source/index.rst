Python bindings to the OpenStack Meteos API
===========================================

This is a client for OpenStack Meteos API. There's :doc:`a Python API
<api>` (the :mod:`meteosclient` module), and a :doc:`command-line utility
<shell>` (installed as an OpenStackClient plugin). Each implements the entire
OpenStack Meteos API.

You'll need credentials for an OpenStack cloud that implements the
Data Processing API, in order to use the meteos client.

You may want to read the `OpenStack Meteos Docs`__  -- the overview, at
least -- to get an idea of the concepts. By understanding the concepts
this library should make more sense.

 __ http://docs.openstack.org/developer/meteos/

Contents:

.. toctree::
   :maxdepth: 2

   api
   shell
   cli
   how_to_participate

Contributing
============

Code is hosted in `review.o.o`_ and mirrored to `github`_ and `git.o.o`_ .
Submit bugs to the Meteos project on `launchpad`_ and to the Meteos client on
`launchpad_client`_. Submit code to the openstack/python-meteosclient project
using `gerrit`_.

.. _review.o.o: https://review.openstack.org
.. _github: https://github.com/openstack/python-meteosclient
.. _git.o.o: http://git.openstack.org/cgit/openstack/python-meteosclient
.. _launchpad: https://launchpad.net/meteos
.. _launchpad_client: https://launchpad.net/python-meteosclient
.. _gerrit: http://docs.openstack.org/infra/manual/developers.html#development-workflow

