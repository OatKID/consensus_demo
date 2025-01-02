# Consensus Algorithm For Education

## Prepare package before execute
1. Install [Python](https://www.python.org/) version 3.12
2. Create virtual environment and install package as follow:
```command line
python -m venv .venv

# window
.\.venv\Scripts\activate.bat

pip install -r requirement.txt
```

## Test Simulation
### Test PBFT
``` bash
# python simulator.py pbft <num-nodes> > pbft_result.txt

# Example
python simulator.py pbft 10 > pbft_result.txt
```

### Test QPBFT
``` bash
# python simulator.py qpbft <num-management-nodes> <num-vote-nodes> > qpbft_result.txt

# Example
python simulator.py qpbft 6 4 > qpbft_result.txt
```

### Test Proposed
``` bash
# python simulator.py proposed <num-master-nodes> <num-slave-nodes> <num-sample> > proposed_result.txt

# Example
python simulator.py proposed 6 4 5 > proposed_result.txt
```