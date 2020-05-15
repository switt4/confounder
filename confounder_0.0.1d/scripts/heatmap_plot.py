import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_tsv(inTSV):
	dataTSV = pd.read_table(inTSV)
	dataTSV.head()
	return dataTSV

def heatmap_plot(inArray,XLabels,YLabels,Title,Filename):
	fig,ax = plt.subplots()
	ax.imshow(inArray,labels=Labels)
	ax.set_title(Title,fontsize='xx-large')
    ax.set_xticks(np.arange(np.shape(inArray)[0]))
    ax.set_yticks(np.arange(np.shape(inArray)[1]))
    ax.set_xticklabels(XLabels,rotation=45,ha='right',rotation_mode='anchor')
	ax.set_yticklabels(YLabels)
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_xlabel('correlation')
	plt.tight_layout()
	plt.savefig(Filename,format='svg')
	plt.close()

parser = argparse.ArgumentParser(description='Heatmap plot entrypoint script.')
parser.add_argument('confounds_tsv', help='Input confounds.tsv to plot.')
parser.add_argument('boldsignal_txt', help="Input boldsignal.txt to plot")
parser.add_argument('output_svgfile', help='Filename and path for output svg.')
parser.add_argument('--confounds_use', help='Config file input with list of confounds to test.')
parser.add_argument('--trial_use',help='Config file input with trial names.')
args = parser.parse_args()

confounds = read_tsv(args.confounds_tsv)

confounds_dictionary = args.confounds_use
confounds_names = list(confounds_dictionary.values())
flat_names = [item for sublist in confounds_names for item in sublist]
flat_names_unique = list(set(flat_names))
flat_names_unique = flat_names_unique.sort()

bold_signal = np.loadtxt(args.boldsignal_txt)

bold_confound_correlation = []

for bold in range(np.shape(bold_signal)[1]):
    for conf in range(len(flat_names_unique)):
        corr_temp = np.correlate(bold_signal[:,bold],np.nan_to_num(np.array(confounds[flat_names_unique[conf]])))
        bold_confound_correlation.append(corr_temp)

bold_confound_correlation = np.array(bold_confound_correlation)
bold_confound_correlation = np.reshape(bold_confound_correlation,(np.shape(bold_signal)[1],len(flat_names_unique)))

heatmap_plot(bold_confound_correlation.T,flat_names_unique,args.trial_use,'Correlation between Bold Signal and Confounds',args.output_svgfile)

