from glob import glob
from os import makedirs
from shutil import move

from bs4 import BeautifulSoup
from github_release import gh_release_create
from requests import get

url = 'https://www.torproject.org/download/download.html'
response = get(url)
data = BeautifulSoup(response.content, 'html.parser')
version = str(data.find_all('span', class_='hidden')).split('"')[7]
print("latest version is: " + version)
win = "https://www.torproject.org/dist/torbrowser/" + version + "/torbrowser-install-" + version + "_en-US.exe"
win64 = "https://www.torproject.org/dist/torbrowser/" + version + "/torbrowser-install-win64-" + version + "_en-US.exe"
osx = "https://www.torproject.org/dist/torbrowser/" + version + "/TorBrowser-" + version + "-osx64_en-US.dmg"
linux = "https://www.torproject.org/dist/torbrowser/" + version + "/tor-browser-linux32-" + version + "_en-US.tar.xz"
linux64 = "https://www.torproject.org/dist/torbrowser/" + version + "/tor-browser-linux64-" + version + "_en-US.tar.xz"

print("Starting download")
platforms = [win, win64, osx, linux, linux64]
for platform in platforms:
    url = platform
    name = platform.split('/')[6]
    print("Downloading: " + name)
    r = get(url)
    with open(name, 'wb') as f:
        f.write(r.content)

print("Moving files")
makedirs("out", exist_ok=True)
for file in glob(version):
    move(file, 'out/')

print("Uploading files")
gh_release_create("yshalsager/TorAutoMirror", version, publish=True, name=version, asset_pattern="out/*")
