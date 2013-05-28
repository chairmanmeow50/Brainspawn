jrom neo import io

# instantiates a io object that can read neo hdf5 files
r = io.NeoHdf5IO( filename = "spa_sequence/sequence.hd5" )

# returns basic info about what data is stored within the io object
r.get_info()

# in neo, hierarchy is block->segment-> various neuro physiological data objects
block = r.read_block()

# get all segments
list_of_segments = block.segments

# iterate through all segments
for segment in list_of_segments:
   # gets spike trains in this segment
   # spike trains are objects that represent a series of spikes
   array_of_spiketrains = segment.spiketrains
   spiketrain = array_of_spiketrains[0]
   print "spiketrain"
   print "sampling rate: " + str(spiketrain.sampling_rate) 
   print "spike times: " + str(spiketrain.times) 

   # iterate through all spikes
   # spiketrain inherits from a NumPy ndarray
   #for spike in spiketrains:
   #   print spike

   # gets analog signals in this segment
   # analog signals are a sampling of a continuous analog signal 
   array_of_analogsignals = segment.analogsignals
   analogsignal = array_of_analogsignals[0]
   print "analog signal"
   print "sampling rate: " + str(analogsignal.sampling_rate) 
   print "times: " + str(analogsignal.times) 

r.close()

