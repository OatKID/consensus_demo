from consensus.PBFT_Simulator import PBFT_Simulator

consensus = PBFT_Simulator(10)

consensus.send_request("Hello world")