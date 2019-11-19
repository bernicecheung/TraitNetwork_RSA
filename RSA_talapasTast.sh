#!/bin/bash
#SBATCH --partition=ctn        ### Partition (like a queue in PBS)
#SBATCH --job-name=trait_RSA      ### Job Name
#SBATCH --output=trait_RSA.out         ### File in which to store job output
#SBATCH --error=trait_RSA.err          ### File in which to store job error messages
#SBATCH --time=5-00:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --cpus-per-task=4               ### Number of CPU needed for the job
#SBATCH --mem=50G              ### Total memory
#SBATCH --account=sanlab      ### Account used for job submission

module load prl
module load python/2.7.13
PYTHONPATH="${PYTHONPATH}:/projects/sanlab/kcheung3/traitNetwork_MVPA/RSA/src"
export PYTHONPATH
python /projects/sanlab/kcheung3/traitNetwork_MVPA/RSA/RSA.py --rootDir /projects/sanlab/kcheung3/traitNetwork_MVPA/ --ID 1 --valence P --rad 5
