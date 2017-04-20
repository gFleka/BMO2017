from pymote.algorithm import NodeAlgorithm
from pymote.message import Message


class SpanningTree(NodeAlgorithm):
    required_params = {}
    default_params = {'neighborsKey' : 'Neighbors'}
    
    def initializer(self):
        for node in self.network.nodes():            
            node.memory[self.neighborsKey] = \
                node.compositeSensor.read()['Neighbors']
            node.status = 'IDLE'
        ini_node = self.network.nodes()[0]
        ini_node.status = 'INITIATOR'

        self.network.outbox.insert(0, Message(header = NodeAlgorithm.INI,
                                              destination = ini_node))
        
        
    def initiator(self, node, message):
        if message.header == NodeAlgorithm.INI:
            node.memory['root'] = 'True'
            node.memory['counter'] = 0
            node.memory['tree'] = []
            node.memory['neigh'] = len(node.memory[self.neighborsKey])
            node.send(Message(header = 'Q',
                    destination = node.memory[self.neighborsKey]))
            node.status = 'ACTIVE'

    def idle(self, node, message): 
        if message.header == 'Q':
            tree = []
            node.memory['root'] = 'False'
            node.memory['parent'] = message.source
            
            tree.append(message.source)
            node.memory['tree'] = list(tree)
            node.memory['neigh'] = len(node.memory[self.neighborsKey])
            
            node.send(Message(header = 'Yes', destination = message.source))
            node.memory['counter'] = 1
            if node.memory['counter'] == node.memory['neigh']:
                node.status = 'DONE'
            else:
                node.memory['N_P'] = list(node.memory[self.neighborsKey])
                node.memory['N_P'].remove(node.memory['parent'])
                node.send(Message(header = 'Q',
                                destination = node.memory['N_P']))
                node.status = 'ACTIVE'
        
    def active(self, node, message):
        if message.header == 'Q':
            node.send(Message(header = 'No',
                    destination = message.source))
        elif message.header == 'Yes':
            node.memory['tree'].append(message.source)
            node.memory['counter'] = node.memory['counter'] + 1
            if node.memory['counter'] == node.memory['neigh']:
                node.status = 'DONE'
        else:
            node.memory['counter'] = node.memory['counter'] + 1
            if node.memory['counter'] == node.memory['neigh']:
                node.status = 'DONE'

    
    def done(self, node):
        pass

    
    STATUS = {
            'INITIATOR' : initiator,
            'ACTIVE'   : active,
            'IDLE'      : idle, 
            'DONE'      : done,
            }