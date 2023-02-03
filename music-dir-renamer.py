# this script's purpose is to rename my music directories according to a preferred schema
# and to have a script I can run with a simple alias
import os
import eyed3

for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        if filename.endswith(".mp3"):
            filepath = os.path.join(dirpath, filename)
            audiofile = eyed3.load(filepath)
            artist = audiofile.tag.artist
            album = audiofile.tag.album
            year = audiofile.tag.getBestDate().year
            new_dirname = "{} - {} ({})".format(artist, album, year)
            new_dirpath = os.path.join(os.path.dirname(dirpath), new_dirname)
            if not os.path.exists(new_dirpath):
                os.rename(dirpath, new_dirpath)
