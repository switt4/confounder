rule run_cosine_angle:
	input: 
		stats_file = join(feat_dir,'task-{task}',subj_sess_dir,'confound-{confound_name}','run-{run}',f'stats.nii.gz')
        param_estimate_files = join(feat_dir,f'param_estimate_file_list.txt')
	output:
		cosine_dictionary = join(confounder_dir,subj_sess_dir,'task-{task}',f'{subj_sess_prefix}_cosine.json')
		mean_cosine_dictionary = join(confounder_dir,subj_sess_dir,'task-{task}',f'{subj_sess_prefix}_mean_cosine.json')
	script:
        cosine_angle {input.stats_file} {input.param_estimate_files} {output.cosine_dictionary} {output.mean_cosine_dictionary}