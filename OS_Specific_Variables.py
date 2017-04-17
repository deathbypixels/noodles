import sys

# Create OS specific variables (no Linux support)
volProjects = ''
volAssets = ''
if sys.platform == 'win32':
    volProjects = 'X:'
    volAssets = 'Y:'
    volShows = 'Z:'
elif (sys.platform == 'darwin'):
    volProjects = '/Volumes/Projects'
    volAssets = '/Volumes/Assets'
