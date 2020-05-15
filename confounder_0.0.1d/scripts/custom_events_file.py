import argparse
import pandas as pd

def read_tsv(inTSV):
	dataTSV = pd.read_table(inTSV)
	dataTSV.head()
	return dataTSV

parser = argparse.ArgumentParser(description='Create custon EV text files for FEAT design.')
parser.add_argument('events_tsv', help='Input events.tsv to parse.')
parser.add_argument('custom_event_file', help='Ouput filename for custom EV text file.')
parser.add_argument('--trial_names',help='Config file input with trial names.')
args = parser.parse_args()


# load in events.tsv file
event_file = args.events_tsv
task_timings = read_tsv(event_file)

# define trial name variable
ev_names = args.trial_names

for ev in range(len(ev_names)):
	evTemp = ev + 1
	timings = task_timings[task_timings.trial_type == ev_names[ev]]
	timings = timings[['onset','duration']]
	timings = np.column_stack((timings,np.ones(len(timings))))
	np.savetxt(args.custom_event_file,timings,delimiter='\t')  
	