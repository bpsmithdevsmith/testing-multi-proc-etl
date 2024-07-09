#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Enable trace mode for debugging
set -x

python perf_test.py drop-table --table processes
python perf_test.py create-table --table processes
# python perf_test.py test-multiprocess --table processes --nrows 100000 --json-kbs 40
python perf_test.py test-multiprocess --table processes --nrows 500000 --json-kbs 10 --batch-size 1000 --method batch