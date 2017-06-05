#FullSaturation ne radi, koristiti FullSaturation2

from pymote.algorithm import NodeAlgorithm
from pymote.message import Message
    
             
class FullSaturation2(NodeAlgorithm):
    required_params = {}
    default_params = {'neighborsKey': 'Neighbors'}
    
    def initializer(self):
            for node in self.network.nodes():
                node.memory[self.neighborsKey] = \
                node.compositeSensor.read()['Neighbors']
                node.status = 'AVAILABLE'
                node.memory['neigh'] = list(node.memory['tree'])
                
            ini_node = self.network.nodes()[0]
            self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI,
                                                 destination=ini_node))

    def available(self, node, message):
        # Samo inicijator SPONTANEOUSLY
        if message.header == NodeAlgorithm.INI:
            
            node.send(Message(header='Activate',
                      destination=node.memory['tree']))
            Neighbours = list(node.memory['tree'])
            length = len(Neighbours)
            #ako je list
            if length == 1:
                #posalji poruku parentu
                node.memory['parentSat'] = Neighbours[0]
                node.send(Message(header='M',data = "Saturation", 
                                  destination = node.memory['parentSat']))
                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'
                            
            #node.memory['unvisited'] = list(node.memory[self.neighborsKey])
            #node.memory['initiator'] = 1
            
        elif message.header == 'Activate':
            Neighbours = list(node.memory['tree'])
            Neighbours.remove(message.source)
            node.send(Message(header='Activate',destination = Neighbours))
            Neighbours = list(node.memory['tree'])
            #ako je list
            if (len(Neighbours) == 1):
                
                node.memory['parentSat'] = Neighbours[0]
                node.send(Message(header='M',data = "Saturation", 
                                  destination = node.memory['parentSat']))
                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'
                           
            

    def active(self, node, message):
        if message.header == 'M':
            
            #Process Message
            
            #End Process Message
            
            node.memory['neigh'].remove(message.source)
            
            length = len(node.memory['neigh'])
            if length == 1:
                #prepare message
                node.memory['parentSat'] = node.memory['neigh'][0]
                node.send((Message(header='M',data = "Saturation", 
                                  destination = node.memory['parentSat'])))
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
             
class FullSaturationCenter(NodeAlgorithm):
    required_params = {}
    default_params = {'neighborsKey': 'Neighbors'}
    
    def initializer(self):
            for node in self.network.nodes():
                node.memory[self.neighborsKey] = \
                node.compositeSensor.read()['Neighbors']
                node.status = 'AVAILABLE'
                node.memory['neigh'] = list(node.memory['tree'])
                
            ini_node = self.network.nodes()[0]
            self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI,
                                                 destination=ini_node))

    def available(self, node, message):
        # Samo inicijator SPONTANEOUSLY
        if message.header == NodeAlgorithm.INI:
            
            node.send(Message(header='Activate',
                      destination=node.memory['tree']))
            ###Initialize
            node.memory['Max_Value'] = 0
            node.memory['Max2_Value'] = 0
            
            ###end Initialize
            Neighbours = list(node.memory['tree'])
            length = len(Neighbours)
            #ako je list
            if length == 1:
                #posalji poruku parentu
                
                
                ###Prepare_Message
                
                node.memory['parentSat'] = Neighbours[0]
                node.send(Message(header='M',data = (node.memory['Max_Value']+1), 
                                  destination = node.memory['parentSat']))
                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'
                            
            #node.memory['unvisited'] = list(node.memory[self.neighborsKey])
            #node.memory['initiator'] = 1
            
        elif message.header == 'Activate':
            Neighbours = list(node.memory['tree'])
            Neighbours.remove(message.source)
            ###Initialize
            node.memory['Max_Value'] = 0
            node.memory['Max2_Value'] = 0
            
            ###end Initialize
            node.send(Message(header='Activate',destination = Neighbours))
            Neighbours = list(node.memory['tree'])
            #ako je list
            if (len(Neighbours) == 1):
                
                ###Prepare message
                #dolje
                
                
                
                node.memory['parentSat'] = Neighbours[0]
                node.send(Message(header='M',data = (node.memory['Max_Value']+1), 
                                  destination = node.memory['parentSat']))
                node.status = 'PROCESSING'
            else:
                node.status = 'ACTIVE'
                           
            

    def active(self, node, message):
        if message.header == 'M':
            
            ####Process Message
            
            Received_Value = message.data
            
            if node.memory['Max_Counter'] < Received_Value:
                node.memory['Max2_Value'] = node.memory['Max_Value']
                node.memory['Max_Value'] = Received_Value
                node.memory['Max_Neighbour'] = message.source
            else:
                if node.memory['Max2_Value'] < Received_Value:
                    node.memory['Max2_Value'] = Received_Value
            
            
            #End Process Message
            
            node.memory['neigh'].remove(message.source)
            
            length = len(node.memory['neigh'])
            if length == 1:
                
                ###Prepare message
                
                node.memory['parentSat'] = node.memory['neigh'][0]
                node.send((Message(header='M',data = (node.memory['Max_Value']+1), 
                                  destination = node.memory['parentSat'])))
                node.status = 'PROCESSING'
                
                
    def processing(self, node, message):
        if message.header == 'Center':
            ####Process Message
            Received_Value = message.data
            
            if node.memory['Max_Counter'] < Received_Value:
                node.memory['Max2_Value'] = node.memory['Max_Value']
                node.memory['Max_Value'] = Received_Value
                node.memory['Max_Neighbour'] = message.source
            else:
                if node.memory['Max2_Value'] < Received_Value:
                    node.memory['Max2_Value'] = Received_Value
            
            #End Process Message
            ####resolve
            
            if (node.memory['Max_Value'] - node.memory['Max2_Value']) == 1:
                if node.memory['Max_Neighbour'] != node.memory['parentSat']:
                    node.send(Message(header='Center',
                                      data = node.memory['Max2_Value'],
                                      destination = node.memory['Max_Neighbour']))
                node.status = 'CENTER'
            else:
                if (node.memory['Max_Value'] - node.memory['Max2_Value']) > 1:
                    node.send(Message(header='Center', 
                                      data = node.memory['Max2_Value'],
                                      destination = node.memory['Max_Neighbour']))
                else:
                    node.status = 'CENTER'
            
            ###endResolve
            node.status = 'SATURATED'
            #start resolution
            
                

    def saturated(self, node, message):
        pass
    
    def center(self, node, message):
        pass
    
    
    STATUS = {
              'AVAILABLE': available,
              'ACTIVE': active,
              'PROCESSING': processing,
              'SATURATED': saturated,
              'CENTER': center
             }