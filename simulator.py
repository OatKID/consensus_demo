from consensus.PBFT_Simulator import PBFT_Simulator

consensus = PBFT_Simulator(10, 2)

# for node in consensus.nodes:
#     print(node)

consensus.send_request("Hello world")