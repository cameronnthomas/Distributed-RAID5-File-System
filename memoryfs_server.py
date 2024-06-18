import pickle, logging
import argparse
import time
import dbm
import os.path
#import hashlib

# For locks: RSM_UNLOCKED=0 , RSM_LOCKED=1
RSM_UNLOCKED = bytearray(b'\x00') * 1
RSM_LOCKED = bytearray(b'\x01') * 1

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2', )


class DiskBlocks():

  def __init__(self, total_num_blocks, block_size):
    # This class stores the raw block array
    self.block = []
    # Initialize raw blocks
    for i in range(0, total_num_blocks):
      putdata = bytearray(block_size)
      self.block.insert(i, putdata)


if __name__ == "__main__":

  # Construct the argument parser
  ap = argparse.ArgumentParser()

  ap.add_argument('-nb',
                  '--total_num_blocks',
                  type=int,
                  help='an integer value')
  ap.add_argument('-bs', '--block_size', type=int, help='an integer value')
  ap.add_argument('-port', '--port', type=int, help='an integer value')
  ap.add_argument('-cblk', '--cblk', type=int, help='an integer value')
  args = ap.parse_args()

  if args.total_num_blocks:
    TOTAL_NUM_BLOCKS = args.total_num_blocks
  else:
    print('Must specify total number of blocks')
    quit()

  if args.block_size:
    BLOCK_SIZE = args.block_size
  else:
    print('Must specify block size')
    quit()

  if args.cblk:
    CBLK = args.cblk
  else:
    CBLK = None

  if args.port:
    PORT = args.port
  else:
    print('Must specify port number')
    quit()

  # initialize blocks
  RawBlocks = DiskBlocks(TOTAL_NUM_BLOCKS, BLOCK_SIZE)

  # create empty dict to store block number and hash pairs
  # initialize all checksums to 0s
  hash_dict = {}
  for i in range (TOTAL_NUM_BLOCKS):
    hash_dict.update({i : 0})
  #h = hashlib.new('md5')

  # Create server
  server = SimpleXMLRPCServer(("127.0.0.1", PORT),
                              requestHandler=RequestHandler)

  # def Get(block_number):
  #   result = RawBlocks.block[block_number]
  #   with dbm.open('checksum', 'c') as db:
  #     checksum = db[str(block_number)]
  #     if checksum != hashlib.md5(result):
  #       return -1
  #   # if there's a a checksum error, function returns without printing the logging error
  #   if CBLK:
  #     logging.error('Get: CHECKSUM ERROR on block: ' + str(CBLK))
  #     return -1
  #   return result

  # server.register_function(Get)

  # need to add cblk logic
  def Get(block_number):
    #print("GET: Block Number:", block_number) 
    # for k, v in hash_dict.items():
    #   if (k < 10):
    #     print(k, v)
    result = RawBlocks.block[block_number]
    print("GET: block number:", block_number)
    checksum = hash_dict.get(block_number) 
    # print("hashlib result:", sum(result))
    # print("hash_dict checksum:", checksum)
    # have special put request to a down server and when you repair when the server gets the special message, it will ignore cblk
    #if ((checksum != sum(result))
    if (checksum != result[0]) or (CBLK == block_number):
      logging.error("CORRUPTED_BLOCK" + str(block_number))
      return -2, "CORRUPTED_BLOCK " + str(block_number)  #i made up that -2 number lol
    return result, "SUCCESS"

  server.register_function(Get)

  # def Put(block_number, data):
  #   RawBlocks.block[block_number] = data.data
  #   with dbm.open('checksum', 'c') as db:
  #     db[str(block_number)] = hashlib.md5(data.data)

  #   return 0

  # server.register_function(Put)


  def Put(block_number, data):
    print("PUT: Block Number:", block_number)
    RawBlocks.block[block_number] = data.data
    #hash_dict.update({block_number: sum(data.data)})
    hash_dict.update({block_number: data.data[0]})
    print('Updating checksum during PUT for block:', block_number, 'checksum: ', data.data[0])
    return 0

  server.register_function(Put)

  # def RSM(block_number):
  #   result = RawBlocks.block[block_number]
  #   # RawBlocks.block[block_number] = RSM_LOCKED
  #   with dbm.open('checksum', 'c') as db:
  #     checksum = db[str(block_number)]
  #     if checksum != hashlib.md5(result):
  #       return -1
  #   if CBLK:
  #     logging.error('Get: CHECKSUM ERROR on block: ' + str(CBLK))
  #     return -1
  #   RawBlocks.block[block_number] = bytearray(RSM_LOCKED.ljust(BLOCK_SIZE,b'\x01'))
  #   return result

  # server.register_function(RSM)


  def RSM(block_number):
    result = RawBlocks.block[block_number]
    # RawBlocks.block[block_number] = RSM_LOCKED
    RawBlocks.block[block_number] = bytearray(RSM_LOCKED.ljust(BLOCK_SIZE, b'\x01'))
    return result

  server.register_function(RSM)

  # Run the server's main loop
  print("Running block server with nb=" + str(TOTAL_NUM_BLOCKS) + ", bs=" +
        str(BLOCK_SIZE) + " on port " + str(PORT))
  server.serve_forever()
