# Author: Diane Trout
# Date: 2013 Sept 27
#
# This file contains the initialization information from the autoopen package.
#
# Copyright (c) 2013 by California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the California Institute of Technology nor
# the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior
# written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CALTECH
# OR THE CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
#

import bz2
import gzip
import os
from shutil import rmtree
from StringIO import StringIO
from tempfile import mkdtemp
from unittest import TestCase

from autoopen import autoopen

class TestAutoOpen(TestCase):
    def setUp(self):
        self.tempdir = mkdtemp(prefix='tmp_autoopen_')

    def tearDown(self):
        rmtree(self.tempdir)

    def test_compressed_files(self):
        extensions = ['.gz', '.bz2']
        for ext in extensions:
            filename = os.path.join(self.tempdir, 'temp' + ext)
            text = 'hello'
            with autoopen(filename, 'w') as outstream:
                outstream.write(text)

            with autoopen(filename, 'r') as instream:
                read_text = instream.read()

            self.assertEqual(text, read_text)

            with open(filename, 'r') as instream:
                compressed_text = instream.read()

            self.assertNotEqual(text, compressed_text)

    def test_string_io(self):
        text = 'hello'
        filelike = StringIO()
        # sadly in py27 StringIO doesn't have the __exit__
        # member needed to use the context manager.
        stream = autoopen(filelike, 'w')
        stream.write(text)
        stream.seek(0)
        read_text = stream.read()
        self.assertEqual(read_text, text)
