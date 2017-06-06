from pymote import *
net_gen = NetworkGenerator(100)
net = net_gen.generate_random_network()
from pymote.algorithms.tree import SpanningTree
from pymote.algorithms.saturationCenterFinding import FullSaturationCenter
net.algorithms = ( SpanningTree, FullSaturationCenter, )
sim = Simulation(net)
sim.run()