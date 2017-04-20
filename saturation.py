from pymote.algorithm import NodeAlgorithm
from pymote.message import Message


class FullSaturation(NodeAlgorithm):
    required_params = {}
    default_params = {'neighborsKey': 'Neighbors'}
    
    def initializer(self):
            for node in self.network.nodes():
                node.memory[self.neighborsKey] = \
                node.compositeSensor.read()['Neighbors']
                node.status = 'AVAILABLE'
                
            ini_node = self.network.nodes()[0]
            self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI,
                                                 destination=ini_node))

    def available(self, node, message):
        # Samo inicijator SPONTANEOUSLY
        if message.header == NodeAlgorithm.INI:
            
            node.send(Message(header='Activate',
                      destination=node.memory[self.neighborsKey]))
            Neighbours = list(node.memory[self.neighborsKey])
            length = len(Neighbours)
            #ako je list
            if length == 1:
                #posalji poruku parentu
                node.memory['parent'] = Neighbours[0]
                node.send(Message(header='M',data = "Saturation", 
                                  destination = node.memory['parent']))
                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'
        
        else:
            Neighbours = list(node.memory[self.neighboursKey])
            Neighbours.remove(message.source)
            node.send(Message(header='Activate',destination = Neighbours))
            #ako je list
            if (len(node.memory[self.neighboursKey]) == 1):
                node.memory['parent'] = Neighbours[0]
                node.send(Message(header='M',data = "Saturation", 
                                  destination = node.memory['parent']))
                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'
                           
            

    def active(self, node, message):
        if message.header == 'M':
            
            #Process Message
            
            #End Process Message
            node.memory['neigh'] = list(node.memory[self.neighborsKey])
            node.memory['neigh'].remove(message.source)
            
            length = len(node.memory['neigh'])
            if length == 1:
                #prepare message
                node.memory['parent'] = node.memory['neigh'][0]
                node.send((Message(header='M',data = "Saturation", 
                                  destination = node.memory['parent'])))
                node.status = 'PROCESSING'
                
                
    def processing(self, node, message):
        if message.header == 'M':
            #Process MEssage
            
            #End Process Message
            #resolve
            node.status = 'SATURATED'
            #start resolution
                

    def saturated(self, node, message):
        pass

    STATUS = {
              'AVAILABLE': available,
              'ACTIVE': active,
              'PROCESSING': processing,
              'SATURATED': saturated,
             }