#! /usr/bin/env python

import argparse
import nibabel as nib
import numpy as np
import pandas as pd
import os, sys
import surfdist as sd
from surfdist import viz, load, utils, surfdist
from bids.grabbids import BIDSLayout
from pkg_resources import resource_filename, Requirement

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('bids_dir', help='The directory with the input dataset '
                                         'formatted according to the BIDS standard.')
    parser.add_argument('out_dir', help='Results are put into {out_dir}/surfaceanalysis.')
    parser.add_argument('analysis_level', default='participant')
    parser.add_argument('--participant_label', help='The label of the participant that should be analyzed. The label '
                                                    'corresponds to sub-<participant_label> from the BIDS spec '
                                                    '(so it does not include "sub-"). If this parameter is not '
                                                    'provided all subjects should be analyzed. Multiple '
                                                    'participants can be specified with a space separated list.',
                        nargs="+")
    parser.add_argument('--freesurfer_dir', help="Folder with FreeSurfer subjects formatted according "
                                                 "to BIDS standard. If subject's recon-all folder "
                                                 "cannot be found, recon-all will be run. "
                                                 "If not specified freesurfer data will be saved to {"
                                                 "out_dir}/freesurfer")
    parser.add_argument('--license_key',
                        help='FreeSurfer license key - letters and numbers after "*" in the email you '
                             'received after registration. To register (for free) visit '
                             'https://surfer.nmr.mgh.harvard.edu/registration.html',
                        required=True)
    parser.add_argument('--n_cpus', help='Number of CPUs/cores available to use.', default=1, type=int)
    args = parser.parse_args()

    # set up output dirs
    if args.freesurfer_dir:
        freesurfer_dir = args.freesurfer_dir
    else:
        freesurfer_dir = os.path.join(args.out_dir, "freesurfer")
    out_dir = os.path.join(args.out_dir, "surfaceanalysis")
    if not os.path.isdir(freesurfer_dir):
        os.makedirs(freesurfer_dir)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    run("bids-validator " + args.bids_dir)
    layout = BIDSLayout(args.bids_dir)

    #data_files = run_prepare_all(args.bids_dir, freesurfer_dir, out_dir, subjects_to_analyze,
    #                                 args.n_cpus, args.license_key)
    for subject in args.participant_label:

        # check for presence of freesurfer output. If not there, run FreeSurfer

        # Then run analysis:
        surf_analysis(freesurfer_dir, out_dir, subject_label=subject)
    '''
        for subject, d in data_files.items():
            d["out_dir"] = out_dir
            d["subject_label"] = subject
            run_surface_analysis(**d)
    '''
def surf_analysis(base_dir, out_dir, subject_label=""):

    # eventually add in hemisphere loop

    surf = nib.freesurfer.read_geometry(os.path.join(base_dir, '%s/surf/lh.pial' % subject_label))
    cort = np.sort(nib.freesurfer.read_label(os.path.join(base_dir, '%s/label/lh.cortex.label' % subject_label)))
    sulc = nib.freesurfer.read_morph_data(os.path.join(base_dir, '%s/surf/lh.sulc' % subject_label))

    region = 'S_central'
    src  = sd.load.load_freesurfer_label(os.path.join(base_dir, '%s/label/lh.aparc.a2009s.annot' % subject_label), region, cort)

    # calculate distance
    dist = sd.surfdist.dist_calc(surf, cort, src)

    dist1 = dist.copy()
    dist1[cort] = (dist1[cort] - np.max(dist1[cort])) * -1

    out_file = os.path.join(out_dir, subject_label + "_predicted_age.tsv")

    df = pd.DataFrame([])
    df = df.append(dist1)
    df.to_csv(out_file, sep="\t", index=False)
    print("FINISHED. Saved %s %s" % (subject_label, out_file))
