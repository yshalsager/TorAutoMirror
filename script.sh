echo Fetching versions:
curl -s https://www.torproject.org/projects/torbrowser.html | grep en | grep -Eo "/dist/[a-zA-Z0-9./?=_-]*" | grep -i -E "exe|tar|dmg" | grep -v "asc" > download
echo Downloading:
links=$(cat download)
for link in $links; do
echo Download $link
wget -qq https://www.torproject.org/$link
done
mkdir files && mv *.tar.xz *.exe *.dmg files/
