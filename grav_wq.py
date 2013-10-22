# This script uses grav.py functions to compute gravity for
# a single point whose data is provided on the command line. 
# Input: See print_usage() for the input parameter.
# Output: a single file that with one line containing the
# position ID, timestep and gravity measurement.
# Author: Rachel Gladysz 

from work_queue import *
import sys

start_timestep = 1
end_timestep = 55


num_args = 1 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0] 
    print "sys.argv[0] : Indicate the script file name"
    sys.exit(1)

if (len(sys.argv) != 1):
    print_usage()
elif len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()


grav_pos_file = "grav_pos.txt"


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
		density_file = "%d_density_grid.txt" % (i)
		command = "python grav_per_point.py density_file %s %s %s %s" % (gp_list[count][0], gp_list[count][1], gp_list[count][2], gp_list[count][3])
		#print command
		id = str(gp_list[count][0])
		outfile = id+"%d_density_grid.txt.out" % (i)
		#print outfile
		
		T = Task(command)
		T.specify_file(grav_file, grav_file, WORK_QUEUE_INPUT, cache = TRUE)
		T.specify_file(density_file, density_file, WORK_QUEUE_INPUT, cache = TRUE)
		T.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache = FALSE)
		taskid = Q.submit(T)
	count += 1
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
