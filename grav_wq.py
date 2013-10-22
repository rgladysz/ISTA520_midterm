# This script uses grav.py functions to compute gravity for
# a single point whose data is provided on the command line. 
# Input: See print_usage() for the input parameters and their order.
# Output: a single file that with one line containing the
# position ID, timestep and gravity measurement.
# Author: Rachel Gladysz 

from work_queue import *
import sys

start_timestep = 1
end_timestep = 55


num_args = 4 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0], " <Path to scripts> <Path to inputs> <Path to outputs>"
    print "<Path to scripts> : Indicate which directory contains the scripts file"
    print "<Path to inputs> : Indicate which directory contains the inputs file"
    print "<Path to outputs> : Indicate which directory contains the outputs file"
    sys.exit(1)

if (len(sys.argv) == 1):
    print_usage()
elif len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()


grav_calc = sys.argv[1]+"/scripts/"+sys.argv[0]
#density_file = sys.argv[2]+"/inputs/density_grid.txt"
grav_pos_file = sys.argv[2]+"/inputs/grav_pos.txt"


try:
	Q = WorkQueue(port=0)
except:
	print "could not instantiate Work Queue master"
	sys.exit(1)

print "Listening on port %d." % Q.port


gp_list = []
gp = open(grav_pos_file, 'r')

count = 0
for line in gp:
	gp_list.append(line.split())
	for i in range(start_timestep, end_timestep):
		command = "python grav.py" +i+"_density_grid.txt %s %s %s %s" % (gp_list[count][0], gp_list[count][1], gp_list[count][2], gp_list[count][3])
		print command
		outfile = sys.argv[3]+"/outputs/"+str(gp_list[count][0]) +"_"+i+"_density_grid.txt.out"
		print outfile
		count += 1
		T = Task(command)
		T.specify_file(grav_file, grav_file, WORK_QUEUE_INPUT, cache = TRUE)
		T.specify_file(density_file, density_file, WORK_QUEUE_INPUT, cache = TRUE)
		T.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache = FALSE)
		taskid = Q.submit(T)
print "Done."
gp.close()
sys.exit(0)

 
print "Waiting for tasks to complete..."
while not Q.empty():
    T = Q.wait(5)
    if T:
        print "Task (id# %d) complete: %s (return code %d)" % (T.id, T.command, T.return_status)
    	print T.result

print "done."
