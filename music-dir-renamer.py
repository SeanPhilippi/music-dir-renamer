# this script's purpose is to rename my music directories according to a preferred schema
# and to have a script I can run with a simple alias
import os
import eyed3
from path import Path

MUSIC_PATH = os.environ["MUSIC_PATH"]
music_dir = Path(MUSIC_PATH)
# music_dir = Path("/home/kesto/Test")
# music_dir = Path("/media/kesto/My Passport/MUSIC")

def music_dir_renamer():
    for dirpath, dirnames, files in os.walk(music_dir):
        for filename in files:
            if filename.endswith(".mp3") and "INCOMPLETE" not in filename:
                filepath = Path(dirpath) / filename
                print(f"==filepath {filepath}")
                audiofile = eyed3.load(filepath)
                try:
                    if audiofile.tag.artist is not None:
                        artist = audiofile.tag.artist
                    else:
                        print("!!! Skipped because artist was None")
                        continue
                except:
                    print("!!! error when trying to get artist")
                    # pass here because we don't want to rename if this is missing
                    # will probably make the folder name even worse
                    continue
                try:
                    if audiofile.tag.album is not None:
                        album = audiofile.tag.album
                    else:
                        print("!!! Skipped because album was None")
                        continue
                except:
                    print("!!! error when trying to get album")
                    # pass here because we don't want to rename if this is missing
                    # will probably make the folder name even worse
                    continue
                try:
                    year = f" ({audiofile.tag.getBestDate().year})"
                except:
                    year = ""
                # replace all invalid characters in filenames with '-'
                invalid_chars = "/|:\""
                replace_chars = "-"

                translator = str.maketrans(invalid_chars, replace_chars * len(invalid_chars))

                new_dirname = f"{artist} - {album}{year}".translate(translator)
                new_dirpath = Path(Path(dirpath).parent) / new_dirname

                try:
                    if not Path(new_dirpath).exists():
                          os.rename(dirpath, new_dirpath)
                except:
                    print("==dirpath", dirpath)
                    print("==new_dirpath", new_dirpath)
                    print("!!! Error when trying to find path or rename")
                    continue
                break
            elif "INCOMPLETE" in filename:
                print("!!! Skipped because incomplete file")

music_dir_renamer()                    
