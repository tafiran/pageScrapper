import requests
from bs4 import BeautifulSoup as bS
from os.path import exists
from os import mkdir, rmdir

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

    def __init__(self, ):

        self.config = {
            'folder': 'upload',
            'styles': 'css',
            'scripts': 'scripts',
            'media': 'images',
            'start': 'index.html'
        }

    def checkAllFolders(self):

        # ignoring parameters
        iList = ['folder', 'start']

        # creating main page folder
        mainFolder = self.config['folder']
        self.createDirectory(mainFolder)

        for fold in self.config:
            if fold not in iList:
                self.createDirectory(fold)




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




url('https://vk.com/id176216539')