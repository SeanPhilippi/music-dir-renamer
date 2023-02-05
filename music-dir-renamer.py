# this script's purpose is to rename my music directories according to a preferred schema
# and to have a script I can run with a simple alias
import os
import eyed3
from path import Path
import argparse

MUSIC_PATH = os.environ["MUSIC_PATH"]
music_dir = Path(MUSIC_PATH)

def music_dir_renamer():
    for dirpath, dirnames, files in os.walk(music_dir):
        for filename in files:
            # print("==filename", filename)
            if filename.endswith(".mp3"):
                filepath = os.path.join(dirpath, filename)
                # print("filepath", filepath)
                audiofile = eyed3.load(filepath)
                # print("audiofile", audiofile)
                try:
                    artist = audiofile.tag.artist
                    # print("artist", artist)
                except:
                    # pass here because we don't want to rename if this is missing
                    # will probably make the folder name even worse
                    pass
                try:
                    album = audiofile.tag.album
                    # print("album", album)
                except:
                    # pass here because we don't want to rename if this is missing
                    # will probably make the folder name even worse
                    pass
                try:
                    year = f" ({audiofile.tag.getBestDate().year})"
                    # print("year", year)
                except:
                    year = ""
                new_dirname = f"{artist} - {album}{year}"
                print("--new_dirname", new_dirname)
                new_dirpath = os.path.join(os.path.dirname(dirpath), new_dirname)
                # print("--new_dirpath", new_dirpath)
                break
                # if not os.path.exists(new_dirpath):
                      # os.rename(dirpath, new_dirpath)

music_dir_renamer()                    
