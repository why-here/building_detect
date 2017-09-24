import tifffile as tiff
import matplotlib.pyplot as plt
import shutil
import numpy as np
import os

IM2015_PATH = '../preliminary/quickbird2015.tif'
IM2017_PATH = '../preliminary/quickbird2017.tif'
SAMPLE_PATH = '../tinysample.tif'

x_start = 0; x_end = 256
y_start = 39*256; y_end = 40*256

im2015_0_39_name = 'im2015_0_39.csv'
im2017_0_39_name = 'im2017_0_39.csv'
csvPath = './csvData/'

def plotImg(imMat, title=None):
    plt.imshow(imMat)
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

print('loading data...')
havecsvData = check_csvdata()
if havecsvData:
    im2015_0_39 = np.loadtxt(csvPath+im2015_0_39_name, dtype=int)
    im2017_0_39 = np.loadtxt(csvPath+im2017_0_39_name, dtype=int)
    im2015_0_39 = im2015_0_39.reshape((256,256,4))
    im2017_0_39 = im2017_0_39.reshape((256,256,4))
else:
    create_clean_dir()
    im2015 = tiff.imread(IM2015_PATH).transpose([1,2,0])
    im2017 = tiff.imread(IM2017_PATH).transpose([1,2,0])
    np.savetxt(csvPath+im2015_0_39_name, im2015_0_39.astype(int).reshape(-1), delimiter=',', fmt='%d')
    np.savetxt(csvPath+im2017_0_39_name, im2017_0_39.astype(int).reshape(-1), delimiter=',', fmt='%d')
print('data loaded.')

plotImg(im2015_0_39[:,:,:3], title='2015')
plotImg(im2017_0_39[:,:,:3], title='2017')
