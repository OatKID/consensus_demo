@echo off

echo PBFT
python simulator.py pbft 10 2 > pbft_result.txt
pause

echo QPBFT
python simulator.py qpbft 6 4 2 > qpbft_result.txt
type -Tail 1 qpbft_result.txt
pause

echo Proposed
python simulator.py proposed 6 4 5 2 > proposed_result.txt
pause

echo Finish