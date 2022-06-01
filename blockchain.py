import hashlib
import datetime

blocks = []

def hash(content):
    if not isinstance(content, bytes):
        content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()

class Block(object):
    def __init__(self, previous_hash, file_checksum, owner, type='CREATE'):
        self.previous_hash = previous_hash
        self.file_checksum = file_checksum
        self.type = type
        self.owner = owner
        self.date = datetime.datetime.now().ctime()
        self.block_hash = hash(self.previous_hash+self.type+self.owner + self.date+self.file_checksum)
        

    
    def __repr__(self):
        return '<Block type="{}" hash="{}">'.format(self.type, self.block_hash)

class BlockManager(object):
    def __init__(self):
        self.blocks = []

    def get_last_block(self):
        prev = ''
        block = None
        if len(self.blocks) > 0:
            block = self.blocks[-1]
            prev = block.block_hash
            
        return prev, block
    
    def add_block(self, block):
        self.blocks.append(block)

mng = BlockManager()
    
def create_block(file_checksum, owner):
    prev, _ = mng.get_last_block()
    print(prev)
    new_block = Block(prev, file_checksum, owner)
    mng.add_block(new_block)
    return new_block

def change_block(file_checksum, owner):
    pass

def verify_chain():
    n = len(mng.blocks)-1
    while n > 0:
        block = mng.blocks[n]
        prev_block = mng.blocks[n-1]
        
        previous_hash = hash(prev_block.previous_hash+prev_block.type+prev_block.owner + prev_block.date+prev_block.file_checksum)
        assert previous_hash == block.previous_hash, "Chain broken at: " +repr(prev_block)
        n-=1
    print('Chain OK')



a = create_block('12454', 'user145')
b = create_block('12454', 'user145')
c = create_block('12454', 'user145')

print(mng.blocks)
verify_chain()
print('\nchanging a block')
b.file_checksum = 'HDJSAYEG'
verify_chain() 


