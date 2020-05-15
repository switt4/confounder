rule create_custom_events:
	input:
		events_tsv = join(bids_dir,subj_sess_dir,'func',f'{subj_sess_prefix}_task-{task}_run-{run}_events.tsv')
	params:
		trial_names = config['task_params']['trial_names']
	output:
		event_file = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'trial-{trial_name}_onsets.txt')
	script:
		custom_events_file {input.events_tsv} {output.event_file} --trial_names {params.trial_names}

rule create_confound_files:
	input:
		confounds_tsv = join(fmriprep_dir,subj_sess_dir,'func',f'{subj_sess_prefix}_task-{task}_run-{run}_desc-confounds_regressors.tsv')
		confounds_dictionary = join(confounder_dir,'temp',f'confounds_dictionary.json')
	output:
		confound_file = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'confounds-{confound_name}.txt')
	script:
		create_confound_files {input.confounds_tsv} {input.confounds_dictionary} {output.confound_file}

rule create_fsl_design:
	input:
		feat_dir = config['FEAT_DIR']
		func_file = join(fmriprep_dir,subj_sess_dir,func,f'{subj_sess_prefix}-task-{task}_run-{run}_bold.nii.gz')
		event_file = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'trial-{trial_name}_onsets.txt')
	params:
		bold_reps = config['sequence_params']['bold_reps']
		TR = config['sequence_params']['TR']
	output:
		design_fsf = join(feat_dir,'task-{task}',subj_sess_dir,'confound-none','run-{run}',f'design.fsf')
	script:
		create_fsl_design {input.feat_dir} {input.func_file} {input.event_file} {output.design_fsf} --bold_reps {params.bold_reps} --tr {params.TR}

rule create_fsl_design_confounds:
	input:
		feat_dir = config['FEAT_DIR']
		func_file = join(fmriprep_dir,subj_sess_dir,func,f'{subj_sess_prefix}-task-{task}_run-{run}_bold.nii.gz')
		event_file = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'trial-{trial_name}_onsets.txt')
		confound_file = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'confounds-{confound_name}.txt')
	params:
		bold_reps = config['sequence_params']['bold_reps']
		TR = config['sequence_params']['TR']
	output:
		design_fsf = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'design.fsf')
	script:
		create_fsl_design {input.feat_dir} {input.func_file} {input.event_file} {input.confound_file} {output.design_fsf} --bold_reps {params.bold_reps} --tr {params.TR}

rule estimate_fsl_design:
	input:
		design_fsf = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'design.fsf')
	output:
		
	shell:
		'feat_model {input}'