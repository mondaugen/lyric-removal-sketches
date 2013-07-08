from connection_functions import *

strip = [0,0,2,0,0,0,1,0,0,0,2,0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,1,0,0,2,0,2]

bridges = all_horizontal_bridges_in_strip(strip,0)
print bridges
states = states_from_bridge_pairs(strip, bridges)
print states
