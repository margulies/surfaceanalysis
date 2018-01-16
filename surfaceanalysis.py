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

def surf_analysis(base_dir, out_dir, subject_label="", region=""):

    # eventually add in hemisphere loop
    for hemi in ['lh', 'rh']:

        surf = nib.freesurfer.read_geometry(os.path.join(base_dir, 'sub-%s/surf/%s.pial' % (subject_label, hemi)))
        cort = np.sort(nib.freesurfer.read_label(os.path.join(base_dir, 'sub-%s/label/%s.cortex.label' % (subject_label, hemi))))
        sulc = nib.freesurfer.read_morph_data(os.path.join(base_dir, 'sub-%s/surf/%s.sulc' % (subject_label, hemi)))

        #region = seed_mask #'S_central'
        src  = sd.load.load_freesurfer_label(os.path.join(base_dir, 'sub-%s/label/%s.aparc.a2009s.annot' % (subject_label, hemi)), region, cort)

        # calculate distance
        dist = sd.surfdist.dist_calc(surf, cort, src)

        dist1 = dist.copy()
        dist1[cort] = (dist1[cort] - np.max(dist1[cort])) * -1

        out_file = os.path.join(out_dir, "sub-%s.%s.%s.tsv" % (subject_label, hemi, region))

        df = pd.DataFrame()
        df = df.append([dist1])
        df.to_csv(out_file, sep="\t", index=False)
        print("FINISHED. Saved %s %s" % (subject_label, out_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('bids_dir', help='The directory with the input dataset '
                                         'formatted according to the BIDS standard.')
    parser.add_argument('out_dir', help='Results are put into {out_dir}/surfaceanalysis.')
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
    parser.add_argument('--seed_masks',
                        help='List of freesurfer label names, e.g., S_central',
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

    for subject in args.participant_label:
        # check for presence of freesurfer output. If not there, run FreeSurfer:

        #for seed_mask in args.seed_masks:
        # Run analysis
        surf_analysis(freesurfer_dir, out_dir, subject_label=subject, region=args.seed_masks)
