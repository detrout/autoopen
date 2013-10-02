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

"""
Helpful utilities for turning random names/objects into streams.
"""
import os
import gzip
import bz2
import types
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def isfilelike(file_ref, mode):
    """Does file_ref have the core file operations?
    """
    # if mode is w/a check to make sure we writeable ops
    # but always check to see if we can read
    read_operations = ['read', 'readline', 'readlines']
    write_operations = [ 'write', 'writelines' ]
    if mode[0] in ('w', 'a'):
        for o in write_operations:
            if not hasattr(file_ref, o):
                return False
    for o in read_operations:
        if not hasattr(file_ref, o):
            return False

    return True

def isurllike(file_ref, mode):
    """
    does file_ref look like a url?
    (AKA does it start with protocol:// ?)
    """
    #what if mode is 'w'?
    parsed = urlparse(file_ref)
    schema, netloc, path, params, query, fragment = parsed

    return len(schema) > 0

def autoopen(file_ref, mode='r'):
    """
    Attempt to intelligently turn file_ref into a readable stream
    """
    # catch being passed a file
    if type(file_ref) is types.FileType:
        return file_ref
    # does it look like a file?
    elif isfilelike(file_ref, mode):
        return file_ref
    elif isurllike(file_ref, mode):
        return urllib2.urlopen(file_ref)
    elif os.path.splitext(file_ref)[1] == ".gz":
        return gzip.open(file_ref, mode)
    elif os.path.splitext(file_ref)[1] == '.bz2':
        return bz2.BZ2File(file_ref, mode)
    else:
        return open(file_ref,mode)
