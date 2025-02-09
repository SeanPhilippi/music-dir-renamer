# this script's purpose is to rename my music directories according to a preferred schema
# and to have a script I can run with a simple alias
import os
import eyed3
from path import Path

MUSIC_PATH = os.environ["MUSIC_PATH"]
# music_dir = Path(MUSIC_PATH)
music_dir = Path("/home/kesto/Test")
# music_dir = Path("/media/kesto/My Passport/MUSIC")

problematic_dirs = []

def rename_using_schema(audiofile, dir_path):
    try:
        if audiofile.tag.artist is not None:
            artist = audiofile.tag.artist
        else:
            print("!!! Skipped because artist was None")
            problematic_dirs.append(dir_path)
            return
    except Exception as e:
        print(f"!!! error when trying to get artist: {e}")
        # pass here because we don't want to rename if this is missing
        # will probably make the folder name even worse
        problematic_dirs.append(dir_path)
        return
    try:
        if audiofile.tag.album is not None:
            album = audiofile.tag.album
        else:
            print("!!! Skipped because album was None")
            problematic_dirs.append(dir_path)
            return
    except Exception as e:
        print(f"!!! error when trying to get album: {e}")
        # pass here because we don't want to rename if this is missing
        # will probably make the folder name even worse
        problematic_dirs.append(dir_path)
        return
    try:
        year = f" ({audiofile.tag.getBestDate().year})"
    except Exception as e:
        print(f"!!! error trying to extract the year: {e}")
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
        if path != music_dir:
            for filename in files:
                if filename.endswith(".mp3") and "INCOMPLETE" not in filename:
                    filepath = path / filename
                    print(f"==filepath: {filepath}")
                    audiofile = eyed3.load(filepath)
                    new_dirname = rename_using_schema(audiofile, filename)
                    if new_dirname is not None:
                        # start renaming using new directory path
                        new_dirpath = Path(Path(dirpath).parent) / new_dirname
                        try:
                            if not Path(new_dirpath).exists():
                                os.rename(dirpath, new_dirpath)
                        except Exception as e:
                            print("==dirpath", repr(dirpath))
                            print("==new_dirpath", repr(new_dirpath))
                            print(f"!!! Error when trying to find path or rename: {e}")
                            continue
                    else:
                        print("!!! Skipped because could not create new directory name with metadata")
                    break

                elif "INCOMPLETE" in filename:
                    print(f"!!! Skipped {filename} because incomplete file")

        else: # if it's a file within top most directory (usually Music)
            for filename in files:
                if filename.endswith(".mp3") and "INCOMPLETE" not in filename:
                    filepath = path / filename
                    print(f"==filepath: {filepath}")
                    audiofile = eyed3.load(filepath)
                    new_dirname = rename_using_schema(audiofile, filename)
                    if new_dirname is not None:
                        new_dirpath = music_dir / new_dirname
                        if new_dirpath in dir_files_dict:
                            dir_files_dict[new_dirpath].append(filepath)
                        else:
                            dir_files_dict[new_dirpath] = [filepath]
                    else:
                        print("!!! Skipped because could not create new directory name with metadata")

                elif "INCOMPLETE" in filename:
                    print("!!! Skipped because incomplete file")

    # loop through the dictionary made for stand-alone files at the top level of music_dir
    for new_dirpath, filepaths in dir_files_dict.items():
        try:
            # create a new directory for the files
            if not new_dirpath.exists():
                os.makedirs(new_dirpath, exist_ok=True)
            for filepath in filepaths:
                # move the files to the new directory
                filepath.rename(new_dirpath / filepath.name)
        except Exception as e:
            print(f"!!! Error when trying to create directory or move file for {new_dirpath}: {e}")

    if problematic_dirs:
        print("problematic files and folders:")
        for dir_path in problematic_dirs:
            print(dir_path)
    else:
        print("No problematic folders!")

music_dir_renamer()
