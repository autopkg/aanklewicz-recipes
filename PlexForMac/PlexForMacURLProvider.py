#!/usr/bin/env python
#
# Copyright 2023 Dan Kuehling, based on work by Allister Banks and Hannes Juutilainen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import urllib.parse
import json

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["PlexForMacURLProvider"]

FEED_URL = "https://plex.tv/api/downloads/6.json"

class PlexForMacURLProvider(URLGetter):
    """Provides the download URL for the latest Plex for Mac app."""

    input_variables = {}
    output_variables = {
        "url": {
            "description": "Download URL for the latest Plex for Mac app."
        }
    }
    description = __doc__

    def get_url(self, FEED_URL):
        """"""
        try:
            json_string = self.download(FEED_URL)
        except Exception as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))

        root = json.loads(json_string)   
        url = next((item['url'] for item in root['computer']['MacOS']['releases'] if item['build'] == "darwin-universal"), None)
        
        return url

    def main(self):
        self.env["url"] = self.get_url(FEED_URL)
        self.output("Found download URL: %s" % self.env['url'])

if __name__ == "__main__":
    processor = PlexForMacURLProvider()
    processor.execute_shell()
