# Consensus Algorithm For Education


## Prepare package before execute
1. Install [Python](https://www.python.org/) version 3.13
2. Create virtual environment and install package as follow:
```command line
python -m venv .venv

# window
.\.venv\Scripts\activate.bat

pip install -r requirement.txt
```

## How to run server
```command line
uvicorn Program:app --host 0.0.0.0 --port 8000
```
> You can change Ip address of host and the number of port

## Test Simulation
``` command line
# window
python .\simulator.py > output.txt
```