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

class Struct():

    def __init__(self):

        self.config = {
            'folder': 'upload',
            'assets': 'assets',
            'styles': 'css',
            'scripts': 'scripts',
            'media': 'images',
            'start': 'index.html'
        }

        self.mainFolder = self.config['folder']
        self.fullIgnore = ['.git', '.idea']
        self.iList = ['folder', 'start', 'assets']
        self.ignore = [self.config[self.iList[i]] for i in range(len(self.iList))]
        self.assets = ['styles', 'scripts', 'media']
        self.asset = [self.config[self.assets[i]] for i in range(len(self.assets))]

        self.checkAllFolders()

    def checkAllFolders(self):

        bar = Bar('Creating structure', max=4)

        self.mFolder()
        bar.next()

        self.assetsFolder()
        bar.next()

        self.assetInnerFolders()
        bar.next()

        self.deleteMoreFolders()
        bar.next()
        bar.finish()




    def mFolder(self):

        bar = Bar('Creating main folder', max=1)

        # creating main page folder
        mainFolder = self.config['folder']
        self.createDirectory(mainFolder)

        bar.next()
        bar.finish()

    def assetsFolder(self):

        bar = Bar('Creating asset folder', max=1)

        # creating assets folder
        assetFolder = self.config['assets']
        self.createDirectory(f'./{self.mainFolder}/{assetFolder}')

        bar.next()
        bar.finish()

    def assetInnerFolders(self):

        assetFolder = self.config['assets']

        progress = Bar('Creating folders in assets pack', max=3)

        for fold in self.config:

            if fold not in self.iList:
                self.createDirectory(f'./{self.mainFolder}/{assetFolder}/{self.config[fold]}')

            progress.next()

        progress.finish()

    def packs(self, path):
        return [f for f in listdir(path) if not isfile(join(path, f))]

    def deleteMoreFolders(self):

        assetFolder = self.config['assets']

        for fold in self.packs('.'):
            if fold != self.mainFolder and fold not in self.fullIgnore:
                rmtree(fold)

        for fold in self.packs(f'./{self.mainFolder}'):
            if fold != assetFolder and fold not in self.fullIgnore:
                rmtree(f'./{self.mainFolder}/{fold}')

        for fold in self.packs(f'./{self.mainFolder}/{assetFolder}'):
            if fold not in self.asset and fold not in self.fullIgnore:
                rmtree(f'./{self.mainFolder}/{assetFolder}/{fold}')

    # CREATING FOLDER
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
        self.appStruct = Struct()

App()