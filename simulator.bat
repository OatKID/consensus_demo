@echo off

echo PBFT
python simulator.py pbft 10 > pbft_result.txt
pause

echo QPBFT
python simulator.py qpbft 6 4 > qpbft_result.txt
pause

echo Proposed
python simulator.py proposed 6 4 5 > proposed_result.txt
pause

echo Finish