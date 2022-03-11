# abstract websocket class for BaseConnector
# it has to implement some methods, described below...
# Instance of child class is sent to BaseConnector.init method
class AbsWebSocket:

    async def handshake(self, uri, headers=[]):
        '''
        Method is used to set connection with server.
        '''
        pass

    async def open(self, new_val: bool = None):
        '''
        Method returns the state of connection
        '''
        pass

    async def recv(self):
        '''
        Method read data from socket. All special packets are not returned.
        '''
        pass

    async def send(self, buf):
        '''
        Method send data to server.
        '''
        pass
