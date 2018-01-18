# How to go from a local python script to cbrain

If you would like to run your own pipeline on the cbrain platform, follow the following steps:

## 1. Begin by creating a working python script

Write a pipeline in python that will take variables, such as `participant_label`, on this command line. For example:

    python /opt/surfaceanalysis.py \
      data data --freesurfer_dir data/freesurfer \
      --seed_masks S_central --participant_label 0001

## 2. Run python script using docker

Begin by writing a `dockerfile`.

Then build the docker image:

    docker build -t margulies/surfaceanalysis:dev .

Run the docker image:

    docker run -ti \
      -v ${dir_path}:${dir_path} \
      -w ${dir_path} \
      --entrypoint /bin/bash margulies/surfaceanalysis:dev

Run the python script within docker image terminal prompt:

    python /opt/surfaceanalysis.py \
      data data --freesurfer_dir data/freesurfer \
      --seed_masks S_central --participant_label 0001

When it's ready to go, push the dockerfile to dockerhub:

    docker push margulies/surfaceanalysis:dev

Now you're ready to build the boutique portion for deploying your docker image on cbrain.

## 3. Create a boutique .json file with command line specifications

Create a `.json` file that specifies how to use your python script on the command line.

Then test the `.json` file:

    bosh validate surfaceanalysis.json

The following command will output an example command with random options. Use this output to ensure the variable specifications in the `.json` file are correct.

    bosh exec simulate surfaceanalysis.json -r

### Create example input file

Create an `invocation.json` file that includes actual command line parameters and test:

    bosh exec simulate surfaceanalysis.json -i invocation.json

### Test scripts locally

    bosh exec launch surfaceanalysis.json invocation.json

## 6. Deploy on cbrain

Send an email to the fine folks at cbrain with the link to your repository as well as a link to example data.
