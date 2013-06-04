from base64 import b64encode

from twisted.internet import ssl, reactor
from twisted.internet.protocol import ClientFactory, Protocol

from drozer.server.receivers.http import HTTPRequest, HTTPResponse

def upload(resource, data, magic=None):
    factory = UploaderFactory(resource, data, magic)
    #reactor.connectSSL('localhost', 31415, factory, ssl.ClientContextFactory())
    reactor.connectTCP('localhost', 31415, factory)
    reactor.run()

class Uploader(Protocol):
    
    def connectionMade(self):
        request = HTTPRequest(verb="POST", resource=self.factory.resource, body=self.factory.data)
        request.headers["Authorization"] = "Basic %s" % b64encode("aaa:bbb")
        request.headers["Content-Length"] = len(self.factory.data)
        if self.factory.magic != None:
            request.headers["X-Drozer-Magic"] = self.factory.magic
        
        self.transport.write(str(request))

    def dataReceived(self, data):
        response = HTTPResponse.parse(data)
        
        if response.status == 201:
            print response.body
        else:
            print response.headers
            print response.body
            
        self.transport.loseConnection()
                
class UploaderFactory(ClientFactory):
    
    protocol = Uploader

    def __init__(self, resource, data, magic=None):
        self.resource = resource
        self.data = data
        self.magic = magic
        
    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()
        