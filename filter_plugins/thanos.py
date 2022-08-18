# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

import os
import re
from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'validate_file_sd': self.validate_file_sd,
            'thanos_checksum': self.checksum,
        }

    def validate_file_sd(self, data, targets):
        """
        """
        result = []
        sublist = []
        config_files = []

        for scrape in data:
            """
            """
            file_sd = scrape.get("file_sd_configs", None)

            if isinstance(file_sd, list):
                file_sd = file_sd[0]
                files = file_sd.get("files", [])

                if len(files) > 0:
                    sublist.append(files)

        config_files = sum(sublist, [])

        display.v("  - files: {}".format(config_files))

        for f in config_files:
            name, extension = os.path.basename(f).split(".")

            display.v("    - name: {} / extenstion {}".format(name, extension))

            if name not in targets or extension not in ["yml", "yaml"]:
                result.append(os.path.basename(f))

        display.v("{}".format(result))

        return result

    def checksum(self, data, os, arch):
        """
        """
        checksum = None

        if isinstance(data, list):
            # filter OS
            # linux = [x for x in data if re.search(r".*thanos-.*.{}.*.tar.gz".format(os), x)]
            # filter OS and ARCH
            checksum = [x for x in data if re.search(r".*thanos-.*.{}-{}.tar.gz".format(os, arch), x)][0]

        if isinstance(checksum, str):
            checksum = checksum.split(" ")[0]

        # display.v("= checksum: {}".format(checksum))

        return checksum

