from consensus.PBFT_Simulator import PBFT_Simulator
from consensus.QPBFT_Simulator import QPBFT_Simulator
from consensus.Proposed_Simulator import Proposed_Simulator
import sys

argument = sys.argv[1:]
print(argument)

match argument[0]:
    case "pbft":
        consensus = PBFT_Simulator(int(argument[1]), output=True)
        consensus.send_request("Hello world")
    case "qpbft":
        consensus = QPBFT_Simulator(int(argument[1]), int(argument[2]), output=True)
        consensus.send_request("Hello world")
    case "proposed":
        consensus = Proposed_Simulator(int(argument[1]), int(argument[2]), int(argument[3]), output=True)
        consensus.send_request("Hello world")
        
    case _:
        print("Please Consensus's Name")