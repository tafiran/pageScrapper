import requests
from bs4 import BeautifulSoup as bS
from os.path import exists, isfile, join
from os import mkdir, rmdir, listdir
from shutil import rmtree
from pageEditor import pageEditor

# GETTING URL WORKING WITH IT
class url():

    def __init__(self, url, config):

        # input url of page to copy
        self.url = url
        self.config = config

        app = config['files']

        self.mainFolder, self.assetFolder = app['folder'], app['assets']
        self.style, self.script, self.media = app['styles'], app['scripts'], app['media']
        self.start = app['start']

        # getting html code from response
        self.soup = bS(self.html().text, 'lxml')

        self.page = pageEditor(self.soup)
        self.soup = self.page.get_result()

        self.save()

    # getting response and setting encoding utf-8
    def html(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        return response

    def save(self):
        with open(f'{self.mainFolder}/{self.start}', "wb") as file:
            file.write(self.soup.prettify('utf-8'))

# CLASS FOR CREATING FOLDER STRUCTURE
class Structure():

    def __init__(self, config):

        self.config = config

        self.mainFolder = self.config['folder']
        self.assetFolder = self.config['assets']

        self.list = {
            'ignore': ['.git', '.idea', 'plugins'],
            'main': ['folder', 'start', 'assets'],
            'asset': [self.config[i] for i in ['styles', 'scripts', 'media']]
        }

        self.checkAllFolders()

    # creating and checking all folders
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
            if fold not in self.list['asset'] and fold not in self.list['ignore']:
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

    def __init__(self, link):

        self.appStruct = Structure({'folder': 'upload', 'assets': 'assets',
                                 'styles': 'css', 'scripts': 'scripts', 'media': 'images', 'start': 'index.html'})

        config = {
            'url': {},
            'files': self.appStruct.config
        }

        url(link, config)

test_url = f'https://ru.stackoverflow.com/' \
           f'questions/1130349/%D0%9F%D0%BE%D0' \
           f'%BB%D0%BE%D1%81%D0%B0-%D0%B7%D0%B0%D0' \
           f'%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8-%D0%BD%D0' \
           f'%B0-python-3-x'


App(test_url)