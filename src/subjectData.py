from mvpa2.suite import *


class subjectData:
    """ This class imports and organizes both behavioral data (in a form of similarity matrix)
    and neural data (in a form of fmri_dataset in mvpa2)
    """

    def __init__(self, rootDir, ID, valence, hemisphere=None):
        """
        Below are the required input.

        :param rootDir: The directory where all the data, masks and codes in.
        :param ID: Subject ID, which starts with 1
        :param valence: "P" indicates positive trait matrix; "N" indicates negative trait matrix
        :param hemisphere: "L" indicates left hemisphere mask; "R" indicates right hemisphere mask
        """


        # check the directory input and make sure the format is correct

        if not os.path.exists(rootDir):
            print 'ERROR: %s does not exist!' % rootDir
        if not rootDir.endswith('/'):
            rootDir = ''.join([rootDir, '/'])

        # set the root directory
        self.rootDir = rootDir

        # set the subject ID
        self.ID = ID

        # set the valence for the dataset
        self.valence = valence

        # set the directory for betaseries
        self.betaDir = os.path.join(rootDir, "betaseries", "betaData", "Subject{n}".format(n=ID),
                                    "sub{n}_betaMerge.nii.gz".format(n=ID))

        # set the directory for attribution files (use valence index as target)
        self.attrDir = os.path.join(rootDir, "attributionFiles", "Subject{n}".format(n=ID),
                                    "sub{n}_att_val.txt".format(n=ID))

        # set the directory for hemisphere brain mask

        self.maskDir = hemisphere if hemisphere is not None else os.path.join(self.rootDir, "brainMask", "MNI152_hemisphere_{h}.nii.gz".format(h=hemisphere))

        # set the directory for trait similarity matrix
        self.traitDir = os.path.join(rootDir, "RSA", "similarityMatrix", "Subject{n}".format(n=ID),
                                     "sub{n}_similarity_{v}.txt".format(n=ID, v=valence.lower()))

    def importSimilarity(self):
        """
        This function is for importing the trait similarity matrix for a given valence and putting it into a vector
        :return: A vector of the lower triangle of the similarity matrix
        """
        # load the trait similarity matrix
        trait_sim = np.loadtxt(self.traitDir)

        # take lower triangle of the trait similarity matrix and flatten it into a vector
        trait_sim_flat = np.tril(trait_sim, k=-1).flatten()

        # the output is a vector
        return trait_sim_flat

    def importNeural(self):
        """
        This funciton is to load and organize the brain activity data in a format recognized by mvpa module.
        It then subsets the data based on valence, and z score them within each chunk
        :return: a fmri dataset for a given valence after z-score the beta within runs
        """

        # convert attribution file format
        self.att = SampleAttributes(self.attrDir)

        # load brain activity data
        brainData = fmri_dataset(
                            samples=os.path.join(self.betaDir),
                            targets=np.array(self.att.targets,dtype='float32'),
                            chunks=self.att.chunks,
                            mask=os.path.join(self.maskDir))

        # subset the dataset based on valence
        if self.valence == "P":
            brainData_subset = brainData[brainData.targets == 1]
        else:
            brainData_subset = brainData[brainData.targets == -1]

        # remove invariant features of the dataset to free some memory
        brainData_subset = remove_invariant_features(brainData_subset)

        # delete the original dataset to free some memory
        del brainData

        # z-score the beta within each run
        zscore(brainData_subset, chunks_attr='chunks', dtype='float32')

        # return the neural dataset of a given valence
        return brainData_subset










