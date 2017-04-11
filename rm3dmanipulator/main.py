from rm3d_reader import RM3DReader
from rm3d_writer import RM3DWriter
from trade import GenericTrade
import logging

logging.basicConfig(level=logging.DEBUG)

# read rm3d input
logging.debug('reading input file ...')
file_in = open('rm3d.out', 'r') 
rm3d_string = file_in.read() 
file_in.close()

reader = RM3DReader()
rm3d_list = reader.process(rm3d_string)

# generate trade list
logging.debug('generating trade list ...')
trade_list = [GenericTrade(t) for t in rm3d_list]

# reset ignore_fx_flag
logging.debug('resetting ignore_fx flag ...')
for t in trade_list: t.set_ignore_fx('0')

# write output
logging.debug('writing output ...')
rm3d_out_list = [t.get_serialized() for t in trade_list]

writer = RM3DWriter()
rm3d_out_string = writer.produce_string(rm3d_out_list)

file_out = open('rm3d_processed.out', 'w') 
file_out.write(rm3d_out_string)
file_out.close()

logging.debug('done. Exiting...')
