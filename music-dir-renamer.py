# this script's purpose is to rename my music directories according to a preferred schema
# and to have a script I can run with a simple alias
import os
import eyed3
from path import Path

MUSIC_PATH = os.environ["MUSIC_PATH"]
music_dir = Path(MUSIC_PATH)
# music_dir = Path("/home/kesto/Test")
# music_dir = Path("/media/kesto/My Passport/MUSIC")

def rename_using_schema(audiofile, top_level=False):
    try:
        if audiofile.tag.artist is not None:
            artist = audiofile.tag.artist
        else:
            print("!!! Skipped because artist was None")
            return
    except:
        print("!!! error when trying to get artist")
        # pass here because we don't want to rename if this is missing
        # will probably make the folder name even worse
        return
    try:
        if audiofile.tag.album is not None:
            album = audiofile.tag.album
        else:
            print("!!! Skipped because album was None")
            return
    except:
        print("!!! error when trying to get album")
        # pass here because we don't want to rename if this is missing
        # will probably make the folder name even worse
        return
    try:
        year = f" ({audiofile.tag.getBestDate().year})"
    except:
        year = ""
    # replace all invalid characters in filenames with '-'
    invalid_chars = "/|:\""
    replace_chars = "-"

    translator = str.maketrans(invalid_chars, replace_chars * len(invalid_chars))

    new_dirname = f"{artist} - {album}{year}".translate(translator)
    return new_dirname


def music_dir_renamer():
    dir_files_dict = {}
    for dirpath, dirnames, files in os.walk(music_dir):
        path = Path(dirpath)
        new_dirpath = None
        if path != music_dir:
            for filename in files:
                if filename.endswith(".mp3") and "INCOMPLETE" not in filename:
                    filepath = path / filename
                    print(f"==filepath: {filepath}")
                    audiofile = eyed3.load(filepath)
                    new_dirname = rename_using_schema(audiofile)
                    if new_dirname is not None:
                        new_dirpath = Path(Path(dirpath).parent) / new_dirname
                        try:
                            if not Path(new_dirpath).exists():
                                os.rename(dirpath, new_dirpath)
                        except:
                            print("==dirpath", dirpath)
                            print("==new_dirpath", new_dirpath)
                            print("!!! Error when trying to find path or rename")
                            continue
                    else:
                        print("!!! Skipped because could not create new directory name with metadata")
                    break

                elif "INCOMPLETE" in filename:
                    print("!!! Skipped because incomplete file")

        else: # if it's a file within top most directory (usually Music)
            for filename in files:
                if filename.endswith(".mp3") and "INCOMPLETE" not in filename:
                    filepath = path / filename
                    print(f"==filepath for top level: {filepath}")
                    audiofile = eyed3.load(filepath)
                    new_dirname = rename_using_schema(audiofile)
                    if new_dirname is not None:
                        new_dirpath = music_dir / new_dirname
                        if new_dirpath in dir_files_dict:
                            dir_files_dict[new_dirpath].append(filepath)
                            print(f'--after append {dir_files_dict}')
                        else:
                            dir_files_dict[new_dirpath] = [filepath]
                            print(f'--after add key {dir_files_dict}')
                    else:
                        print("!!! Skipped because could not create new directory name with metadata")

                elif "INCOMPLETE" in filename:
                    print("!!! Skipped because incomplete file")

        if new_dirpath is None:
            print("!!! Skipped because new_dirpath was None")
            continue
        # start renaming using new directory path

    print(f'REEEEEE {dir_files_dict}')
    # loop through the dictionary made for stand-alone files at the top level of music_dir
    for new_dirpath, filepaths in dir_files_dict.items():
        print("==in top level loop")
        try:
            # create a new directory for the files
            if not new_dirpath.exists():
                os.makedirs(new_dirpath, exist_ok=True)
            for filepath in filepaths:
                # move the files to the new directory
                filepath.rename(new_dirpath / filepath.name)
        except OSError as e:
            print(f"OSError {e}")
            print(f"!!! Error when trying to create directory or move file for {new_dirpath}")

music_dir_renamer()
