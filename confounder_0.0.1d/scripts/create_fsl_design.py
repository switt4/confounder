import os
import argparse
import fsl.data.featanalysis as FA

#create_fsl_design {input.feat_dir} {input.func_file} {input.event_file} {input.confounds_tsv} 
#	{output.design_fsf} --confounds_dict {input.confounds_dict} 
# 	--bold_reps {params.bold_reps} --tr {params.TR}

parser = argparse.ArgumentParser(description='Create FEAT design.')
parser.add_argument('feat_dir', help='Input FEAT directory with example design.fsf.')
parser.add_argument('func_file', help='Func file from fmriprep dir.')
parser.add_argument('custom_event_file', help='Filename for custom EV text file.')
parser.add_argument('output_design_fsf',help='Output filepath for design.fsf.')
parser.add_argument('--bold_reps', help='Config param with number of bold repititions.')
parser.add_argument('--tr', help='Config param with TR.')
args = parser.parse_args()


# get full path to $FSLDIR
FSLDIR = os.path.expandvars('$FSLDIR')

# get path of output design.fsf file
feat_subdir = os.path.split(args.output_design_fsf)[0]

# set variables

# load in design.fsf
design = FA.loadSettings(args.feat_dir)

custom = [('custom%d'%evTemp,'"%s"'%args.custom_event_file)]
design.update(custom)

# first step in tedious process of rebuilding design.fsf 
feat_files = [('feat_files(1)','"%s"'%args.func_file)]
design.update(feat_files)
npts = [('npts','%d'%args.bold_reps)]
design.update(npts)
tr = [('tr','%f'%args.tr)]
design.update(tr)

featwatcher = [('featwatcher_yn',0)]
design.update(featwatcher)
regstandard = [('regstandard','"%s/data/standard/MNI152_T1_2mm_brain"'%FSLDIR)]
design.update(regstandard)
gdc = [('gdc', '""')]
design.update(gdc)
motionevsbeta = [('motionevsbeta','""')]
design.update(motionevsbeta)
scriptevsbeta = [('scriptevsbeta','""')]
design.update(scriptevsbeta)
alternative_mask = [('alternative_mask','""')]
design.update(alternative_mask)
init_initial_highres = [('init_initial_highres','""')]
design.update(init_initial_highres)
init_highres = [('init_highres','""')]
design.update(init_highres)
init_standard = [('init_standard','""')]
design.update(init_standard)

feat_output_dir = [('outputdir','"%s"'%feat_subdir)]
design.update(feat_output_dir)

trial = []
for key,value in design.items():
	trial.append("set fmri({}) {}".format(key,value))
	trial = [sub.replace('set fmri(feat_files(1))','set feat_files(1)') for sub in trial]

with open(args.output_design_fsf, 'w') as f:
	for item in trial:
	f.write("%s\n" % item)