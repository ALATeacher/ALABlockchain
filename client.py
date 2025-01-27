import datetime
import hashlib
import json
import jsonpickle
import sys
import asyncio
import os


class Block:
    index = 0
    text = ""
    previousBlock = ""
    nonce = ""
    difficulty = 0
    minedDate = ""
    def __init__(self):
        self.minedDate = str(datetime.datetime.now())
    def getJson(self):
        return json.dumps(self)
    def getHash(self):
        json = self.getJson()
        encodedJson = json.encode("utf-8")
        return hashlib.md5(encodedJson).hexdigest()

class Client:
    def __init__(self):
        INITIALIZE = False
        if (INITIALIZE):
            firstBlock = Block()
            firstBlock.index = 0
            firstBlock.text=""
            firstBlock.nonce=0
            firstBlock.difficulty=0
            self.chain = [firstBlock]
            pickledJson = jsonpickle.encode(self.chain, unpicklable=False)
            with open("blocks.json", "w") as file:
                file.write(json.dumps(pickledJson))
        self.chain = []
        #try:
        self.importChain()
        #except:
        self.checkForChain()
        asyncio.run(self.listen('172.17.13.40', '12999'))
    
    def importChain(self):
        print("Checking for blockchain on system...")
        with open("blocks.json", "r") as file:
            jsonString = file.read()
        unpickled = jsonpickle.decode(jsonString)
        self.chain = json.loads(unpickled)
        print(self.chain)
        lastBlock = self.chain[-1]
        print("Blockchain loaded successfully.  Last block was mined %s with index:%s" % (lastBlock["minedDate"], lastBlock["index"]))
            
    
    def checkForChain(self):
        #print("No blockchain found on system.  Checking with peers...")
        pass
    
    def createBlock(self, previousBlock):
        pass
        
        
    async def handleClient(self, reader, writer):
        print('New client connected...')
        line = str()
        while line.strip() != 'quit':
            line = (await reader.readline()).decode('utf8')
            if line.strip() == '': continue
            print(f'Received: {line.strip()}')
            writer.write(line.encode('utf8'))
        writer.close()
        print('Client disconnected...')
        
    async def listen(self, host, port):
        server = await asyncio.start_server(self.handleClient, host, port)
        print(f'Listening on {host}:{port}...')
        async with server:
            await server.serve_forever()

class Miner:
    chain = []
    def __init__(self):
        self.importChain()
        self.mine(self.chain[-1])
    def importChain(self):
        print("Checking for blockchain on system...")
        with open("blocks.json", "r") as file:
            jsonString = file.read()
        unpickled = jsonpickle.decode(jsonString)
        self.chain = json.loads(unpickled)
        print(self.chain)
        lastBlock = self.chain[-1]
        print("Blockchain loaded successfully.  Last block was mined %s with index:%s" % (lastBlock["minedDate"], lastBlock["index"]))
    
    #To mine, the previous block is added to a number, then hashed.  
    #If the resulting has is less than the maximum hash value minus
    #the difficulty of the previous hash, the block is mined.  The nonce
    #is sent to known clients to validate.  When validated, the next block is 
    #generated and forwarded to clients.
    
    def mine(self, previousBlock):
        lastHash = json.dumps(previousBlock)
        lastHash = lastHash.encode("utf-8")
        lastHash = hashlib.md5(lastHash).hexdigest()
        print(lastHash)
        dec = int(lastHash, 16)
        difficulty = dec - int(previousBlock["difficulty"])
        nonce = 0
        while True:
            if (nonce%100000==0):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Trying %d" % nonce)
            testStr = lastHash+str(nonce)
            testStr = testStr.encode("utf-8")
            test = hashlib.md5(testStr).hexdigest()
            testDec = int(test, 16)
            if (testDec<difficulty):
                print("I found it!  Nonce:%d" % nonce)
                break
            nonce+=1
        
#client = Client()
miner = Miner()
