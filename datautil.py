import tifffile as tiff
import matplotlib.pyplot as plt
import shutil
import numpy as np
import os
from matplotlib import cm

IM2015_PATH = '../preliminary/quickbird2015.tif'
IM2017_PATH = '../preliminary/quickbird2017.tif'
CADA_PATH = '../cadastral2015.tif'
SAMPLE_PATH = '../tinysample.tif'

x_start = 0; x_end = 256
y_start = 39*256; y_end = 40*256

im2015_0_39_name = 'im2015_0_39.csv'
im2017_0_39_name = 'im2017_0_39.csv'
imcada_0_39_name = 'imcada_0_39.csv'
imsamp_0_39_name = 'imsamp_0_39.csv'
csvPath = './csvData/'

def plotImg(imMat, title=None, **kwargs):
    plt.imshow(imMat, **kwargs)
    if title:
        plt.title(title)
    plt.show()

def create_clean_dir(dirname="csvData"):
    """Create an empty directory

    Args:
        dirname (str): An empty directory name to create
    """

    if os.path.exists(dirname):
        shutil.rmtree(dirname)

    assert os.path.exists(dirname) is False

    os.mkdir(dirname)

    assert len(os.listdir(dirname)) == 0

def check_csvdata(dirname="csvData"):
    if os.path.exists(dirname) and len(os.listdir(dirname)) != 0:
        return True
    else:
        return False

def scale_percentile(matrix):
    w, h, d = matrix.shape
    matrix = np.reshape(matrix, [w * h, d]).astype(np.float64)
    # Get 2nd and 98th percentile
    mins = np.percentile(matrix, 1, axis=0)
    maxs = np.percentile(matrix, 99, axis=0) - mins
    matrix = (matrix - mins[None, :]) / maxs[None, :]
    matrix = np.reshape(matrix, [w, h, d])
    matrix = matrix.clip(0, 1)
    return matrix

print('loading data...')
havecsvData = check_csvdata()
if havecsvData:
    im2015_0_39 = np.loadtxt(csvPath+im2015_0_39_name, dtype=int, delimiter=',')
    im2017_0_39 = np.loadtxt(csvPath+im2017_0_39_name, dtype=int, delimiter=',')
    imcada_0_39 = np.loadtxt(csvPath+imcada_0_39_name, dtype=int, delimiter=',')
    imsamp_0_39 = np.loadtxt(csvPath+imsamp_0_39_name, dtype=int, delimiter=',')
    im2015_0_39 = im2015_0_39.reshape((256,256,4))
    im2017_0_39 = im2017_0_39.reshape((256,256,4))
    imcada_0_39 = imcada_0_39.reshape((256,256))
    imsamp_0_39 = imsamp_0_39.reshape((256,256))
else:
    create_clean_dir()
    im2015 = tiff.imread(IM2015_PATH).transpose([1,2,0])
    im2017 = tiff.imread(IM2017_PATH).transpose([1,2,0])
    imcada = tiff.imread(CADA_PATH)
    imsamp = tiff.imread(SAMPLE_PATH)
    im2015_0_39 = im2015[x_start:x_end, y_start:y_end]
    im2017_0_39 = im2017[x_start:x_end, y_start:y_end]
    imcada_0_39 = imcada[x_start:x_end, y_start:y_end]
    imsamp_0_39 = imsamp[x_start:x_end, y_start:y_end]
    np.savetxt(csvPath+im2015_0_39_name, im2015_0_39.astype(int).reshape((1,-1)), delimiter=',', fmt='%d')
    np.savetxt(csvPath+im2017_0_39_name, im2017_0_39.astype(int).reshape((1,-1)), delimiter=',', fmt='%d')
    np.savetxt(csvPath+imcada_0_39_name, imcada_0_39.astype(int).reshape((1,-1)), delimiter=',', fmt='%d')
    np.savetxt(csvPath+imsamp_0_39_name, imsamp_0_39.astype(int).reshape((1,-1)), delimiter=',', fmt='%d')
print('data loaded.')

plotImg(scale_percentile(im2015_0_39[:,:,:3]), title='2015')
plotImg(scale_percentile(im2017_0_39[:,:,:3]), title='2017')
plotImg(imcada_0_39, title='cada', cmap=cm.bwr)
plotImg(imsamp_0_39, title='sample', cmap=cm.bwr)
