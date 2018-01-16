# surfaceanalysis


docker run -ti -v /Users/dmargulies/Dropbox/01_code/surfaceanalysis/:/Users/dmargulies/Dropbox/01_code/surfaceanalysis/ -w /Users/dmargulies/Dropbox/01_code/surfaceanalysis/ --entrypoint /bin/bash margulies/surfacenalaysis:dev

python /opt/surfaceanalysis.py --participant_label 0001 --freesurfer_dir data/freesurfer --seed_masks S_central data data
