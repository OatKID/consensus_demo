from consensus.PBFT_Simulator import PBFT_Simulator
from consensus.QPBFT_Simulator import QPBFT_Simulator
from consensus.Proposed_Simulator import Proposed_Simulator

consensus1 = PBFT_Simulator(10, 2)
consensus2 = QPBFT_Simulator(7, 3, 2)
consensus3 = Proposed_Simulator(7, 3, 5)

consensus3.send_request("Hello world")