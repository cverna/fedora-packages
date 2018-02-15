# This file is part of Fedora Community.
# Copyright (C) 2011  Red Hat, Inc.
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

import tw2.core as twc

from pygments import highlight
from pygments.formatters import HtmlFormatter
from fedoracommunity.connectors.api import get_connector
from fedoracommunity.connectors.specconnector import SpecConnector
from fedoracommunity.lib.utils import RpmSpecLexer


class ReleaseFilter(twc.Widget):
    on_change = twc.Param('The name of the javascript function to call upon change')
    package = twc.Param('The name of the package')
    template = 'mako:fedoracommunity.widgets.package.templates.release_filter'

    def prepare(self):
        super(ReleaseFilter, self).prepare()
        releases = []
        bodhi = get_connector('bodhi')

        for collection in bodhi.get_all_releases():
            if collection['state'] != 'current':
                continue
            name = collection['id_prefix']
            ver = collection['version']
            label = collection['long_name']
            value = ""
            branchname = collection['branch']
            if branchname:
                value = branchname
            if label != 'Fedora devel' and name in ('FEDORA', 'FEDORA-EPEL'):
                releases.append({
                    'label': label,
                    'value': value,
                    'version': ver,
                    })
        self.releases_table = sorted(releases, reverse=True,
                                     cmp=lambda x, y: cmp(x['version'], y['version']))
        self.releases_table.insert(0, {'label': 'Rawhide', 'value': 'master'})


class Sources(twc.Widget):
    kwds = twc.Param(default=None)
    text = twc.Variable('The text of the specfile')
    template = 'mako:fedoracommunity.widgets.package.templates.package_spec'
    releases = ReleaseFilter

    def prepare(self):
        super(Sources, self).prepare()
        self.package_name = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of')
        self.branch = self.kwds.get('branch', 'master')
        if self.subpackage_of:
            main_package = self.subpackage_of
        else:
            main_package = self.package_name
        spec = SpecConnector(main_package, self.branch)
        self.text = highlight(spec.get_text(), RpmSpecLexer(),
                              HtmlFormatter(full=True, linenos=True, nobackground=True))
