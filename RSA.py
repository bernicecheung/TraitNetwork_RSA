from mvpa2.suite import *
from numpy import log, savetxt
import numpy as np
import sys,os
import argparse



# define import arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'RSA dataset parameters')
    parser.add_argument('--rootDir', dest='rootDir', default='', help='Path to the root directory of all inputs')
    parser.add_argument('--ID', dest='ID',type = int, default='', help='Subject ID (starts with 1)')
    parser.add_argument('--valence', dest='valence', type=str,
                        choices=["P", "N"], default='', help='Choose the valence of the dataset. P for positive, N for negative')
    parser.add_argument('--hemisphere', dest='hemisphere', type=str,
                        choices=["R", "L"],default = '', help = 'Choose the hemisphere mask. R for right, L for left')

    args = parser.parse_args()

