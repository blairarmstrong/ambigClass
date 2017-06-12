

Brief overview and instructions for using this package:

Run files in this order:
semspace.py
(if needed) SUBTLparser to convert non-wiki input from SUBTL/FAN norms to a wiki-like format consistent with the original pipeline.
wikitocritwindow.py (or, if serial processing is desired/faster for lots of small files, wikitocriticalwindow_serial.py)
filtertargetdefs.py
comparison.py


semspace.py
-preprocesses a set of vectors (currently glove vectors) for each read
in as a pickled dictionary with word-vector key-value pairs.

wikitocritwindow.py
-this is where most of the complex work gets done.  This file preprocesses
the wiki dump, split into files, and converts it into text and vector representations.  Other datafiles can be input as well, for instance, the free association norms or the SUBTL norms, by using the preprocessing script to convert those inputs to one line per file versions.  Use the SUBTLparser code to facilitate this process.

comparison.py
-used to compute comparisons between dictionary vectors and vectors created from a corpus (e.g., wikipedia).  Creates output files in ouput.txt summarizing performance for each item and the overall correlation.  For the SUBTL
parse there are some additional fringe cases that generate errors that are not possible (or at least did not occur) in the wiki case.  Other than the fringe case processing, the two files work the same way.  This fringe processing
code is still in development and the case checking should still be examined in more detail to double check it is behaving as expected.


