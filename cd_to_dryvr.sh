# !/bin/bash

mkdir /tmp/drake-dryvr

cd drake-distro
# bridge2 takes info from user and stores it in a file in the above mentioned directory
python bridge2.py

# now make a call to drake to run the simulation
# in this process, simulation data is being written to a file in the same directory
bazel run drake/automotive:demo -- --dragway_length=1000 --num_dragway_lanes=1 --driving_command_gui_names=0


# DryVR analyzes data and returns output, which has yet a direction to take
# python main.py inputFile/ENTER INPUT HERE


# get rid of tmp
# rm -d -r -f /tmp/drake-dryvr
