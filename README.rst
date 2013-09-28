README
======

Introduction
------------

This is a fairly simple module to help handle files compressed with
various common unix file compression algorithms like .gz and .bz2.
It assumes that the compressed file contains a single file and not a
collection of files like with tar or zip.

As time progressed I also added some support to handle being passed
streams or urls.

Usage
-----

..code: python
  from autoopen import autoopen

  stream = autoopen('file.fastq.gz', 'r')
  for line in stream:
     # do something
     pass

License
-------

This work was funded by the ENCODE[#encode] project, in the Wold
lab[#wold]. I'm publishing it so I can discuss it with other
collaborators. Unfortunately I haven't figured out what license I can
actually put this code under.

.. [#encode] http://encodeproject.org/ENCODE/
.. [#wold] https://woldlab.caltech.edu
