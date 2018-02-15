# This file is part of Fedora Community.
# Copyright (C) 2018  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
:mod:`fedoracommunity.connectors.specconnector` - Spec Connector
=======================================================================

This Connector returns a package spec file using src.fp.o as a source

"""
import logging

import requests
from tg import config

log = logging.getLogger(__name__)


class SpecConnector(object):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, package, branch='master'):
        self.pkg = package
        self.branch = branch
        self.baseurl = config.get(
            'fedoracommunity.connector.spec.baseurl',
            'https://src.fedoraproject.org')

    def get_spec(self):
        resp = requests.get(
            '{url}/rpms/{pkg}/raw/{branch}/f/{pkg}.spec'
            .format(url=self.baseurl, pkg=self.pkg, branch=self.branch))
        if resp.ok:
            return resp.text
