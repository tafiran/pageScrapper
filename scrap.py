import requests
from bs4 import BeautifulSoup as bS
from os.path import exists, isfile, join
from os import mkdir, rmdir, listdir
from progress.bar import Bar
from shutil import rmtree

# getting url html class
class url():

    def __init__(self, url):

        # input url of page to copy
        self.url = url

        # getting response and setting encoding utf-8
        response = requests.get(self.url)
        response.encoding = 'utf-8'

        # getting html code from response
        self.soup = bS(response.text, 'lxml')
        self.prettySoup = self.soup.prettify('utf-8')

    def save(self):
        with open("file.html", "wb") as file:
            file.write(self.prettySoup)

# CLASS FOR CREATING FOLDER STRUCTURE
class Structure():

    def __init__(self, config):

        self.config = config

        self.mainFolder = self.config['folder']
        self.assetFolder = self.config['assets']

        self.list = {
            'ignore': ['.git', '.idea'],
            'main': ['folder', 'start', 'assets']
        }

        self.checkAllFolders()

    def checkAllFolders(self):

        self.createMainFolder()
        self.createAssetsFolder()
        self.createAssetInnerFolders()
        self.deleteOtherExcessFolders()

    # creating main page folder
    def createMainFolder(self):
        self.createDirectory(self.mainFolder)

    # creating asset folder
    def createAssetsFolder(self):
        self.createDirectory(f'./{self.mainFolder}/{self.assetFolder}')

    # full asset folder the structure of page
    def createAssetInnerFolders(self):
        for fold in self.config:
            if fold not in self.list['main']:
                self.createDirectory(f'./{self.mainFolder}/{self.assetFolder}/{self.config[fold]}')

    # delete excess folders
    def deleteOtherExcessFolders(self):

        # getting list of folders in pack
        def packs(path):
            return [f for f in listdir(path) if not isfile(join(path, f))]

        # clear folders in root folder
        for fold in packs('.'):
            if fold != self.mainFolder and fold not in self.list['ignore']:
                rmtree(fold)

        # clear folders in main page folder
        for fold in packs(f'./{self.mainFolder}'):
            if fold != self.assetFolder and fold not in self.list['ignore']:
                rmtree(f'./{self.mainFolder}/{fold}')

        # clear folders in asset folder
        for fold in packs(f'./{self.mainFolder}/{self.assetFolder}'):
            if fold not in self.asset and fold not in self.list['ignore']:
                rmtree(f'./{self.mainFolder}/{self.assetFolder}/{fold}')

    # creating folder if not exists
    def createDirectory(self, folder):

        # true if folder not exists
        # creating folder
        if not exists(folder):
            mkdir(folder)
            return True

        # false if folder exists
        # passing folder
        else:
            return False

class App():

    def __init__(self):

        self.appStruct = Structure({'folder': 'upload', 'assets': 'assets',
                                 'styles': 'css', 'scripts': 'scripts', 'media': 'images', 'start': 'index.html'})

        app = self.appStruct.config

        self.mainFolder, self.assetFolder = app['folder'], app['assets']
        self.style, self.script, self.media = app['styles'], app['scripts'], app['media']
        self.start = app['start']




App()