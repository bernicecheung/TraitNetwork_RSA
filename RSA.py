import argparse
from subjectData import subjectData
from neuroCorrelation import neuroCorrelation
from mvpa2.suite import *

if __name__ == "__main__":
    # define import arguments
    parser = argparse.ArgumentParser(description='RSA dataset parameters')
    parser.add_argument('--rootDir', dest='rootDir', default='', help='Path to the root directory of all inputs')
    parser.add_argument('--ID', dest='ID', type=int, default='', help='Subject ID (starts with 1)')
    parser.add_argument('--valence', dest='valence', type=str,
                        choices=["P", "N"], default='',
                        help='Choose the valence of the dataset. P for positive, N for negative')
    parser.add_argument('--hemisphere', dest='hemisphere', type=str,
                        choices=["R", "L"], default='', help='Choose the hemisphere mask. R for right, L for left')
    parser.add_argument('--rad', dest='rad', type=int,
                        default='', help='Set the radius for search light')

    # generate inputs
    inputs = parser.parse_args()

    print ("Start with subject{n}".format(n=inputs.ID))

    # create an object from the subjectData class
    subject = subjectData(inputs.rootDir, inputs.ID, inputs.valence, inputs.hemisphere)

    # load the trait similarity data
    traitData = subject.importSimilarity()

    # load the neural data
    neuralData = subject.importNeural()

    print ("Complete loading neural data")

    # create an object from the neuroCorrelation class
    matrixCorr = neuroCorrelation(traitData)

    # set up searchlight parameters
    # set the radius based on the input
    rad = inputs.rad

    # Fisher's z-transformation for correlation coefficient
    FisherTransform = FxMapper('features', lambda r: 0.5 * np.log((1 + r) / (1 - r)))

    # create the search light
    sl = sphere_searchlight(matrixCorr.correlate, rad, postproc=FisherTransform)

    print ("Complete search light set-up")

    # apply the search light function to the neural data
    sl_output = sl(neuralData)

    print ("Search light completed")

    # transform the search light output to an image data
    sl_image = map2nifti(data=sl_output, dataset=neuralData)

    # save the output
    outputDir = os.path.join(inputs.rootDir, "RSA", "searchLightResult", "Subject{n}".format(n=inputs.ID),
                             "sub{n}_sl_results_{v}{h}_P_R{r}.nii.gz".format(n=inputs.ID, v=inputs.valence, h=inputs.hemisphere, r=inputs.rad))
    sl_image.to_filename(outputDir)

    print ("Complete with subject{n}".format(n=inputs.ID))
