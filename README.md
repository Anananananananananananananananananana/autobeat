# Autobeat
An automated mapping utility for beat saber that uses a markov model to generate maps.

Notes are classified via a 4 character ID, which indicates
 - location (0x0-0xb)
 - cut direction (0-8)
 - handedness (0-1)
 - parity (0-1)
respectively.

The datasets are compiled by running Generation.py, which gets the probabilities of subsequent notes from either recent ranked maps or a given directory of maps.
MapCreator.py is the main script that calls functions from the other files to generate a folder containing the .dat file.
