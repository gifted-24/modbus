#!/usr/bin/env bash
set -euo pipefail

HOST=127.0.0.1:5020
UNIT=1

echo "=== Read 10 holding registers (0..9) ==="
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 0 -c 10 || echo "mbpoll read failed"

echo
echo "=== Write 555 to holding register 20 ==="
# mbpoll write syntax: mbpoll -m tcp host -a unit -t <type> -r <address> <value>
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 20 555 || echo "mbpoll write failed"

echo
echo "=== Read register 20 back ==="
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 20 -c 1 || echo "mbpoll read failed"


echo
echo "=== Read large block (50 regs starting @ 30) ==="
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 30 -c 50 || echo "mbpoll read failed"


echo
echo "=== Done ==="