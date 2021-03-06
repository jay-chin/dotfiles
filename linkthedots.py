import os
import sys
import shutil
import argparse

HOMEDIR='/tmp/test' # Toggle this for testing purposes

def query_yes_no(question, default="yes", cowboy_mode=False):
    """Ask a yes/no question via raw_input() and return their answer.

    " from http://code.activestate.com/recipes/577058/
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
    It must be "yes" (the default), "no" or None (meaning
    an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    if cowboy_mode:
        return True
    valid = {"yes": True, "y": True, "ye": True,
            "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                    "(or 'y' or 'n').\n")

def backup(source, suffix="bkp"):
    """ backup by renaming file or directory with a suffix
    """
    dst = "%s_%s" % (source, suffix)
    print("backing up %s" % dst)
    if os.path.isfile(source):
        os.renames(source, dst)
    if os.path.isdir(source):
        shutil.move(source, dst)
    return dst

def create_link(target, cowboy_mode=False):
    """ Creates a logical link from user's homedir to target 
    """
    linkname = os.path.expanduser(os.path.join(HOMEDIR, os.path.basename(target)))
    print("Creating link from %s to %s" % (linkname, target))
    if os.path.exists(linkname):
        if query_yes_no("%s exists ! Overwrite ?" % linkname, 'yes', cowboy_mode):
            if os.path.isfile(linkname) or os.path.isdir(linkname):
                bkp = backup(linkname)
                print("Backing up %s to %s" % (linkname, bkp))
            if os.path.islink(linkname):
                os.remove(linkname)
        else:
            return

    os.symlink(target, linkname) 

def main():
    parser = argparse.ArgumentParser(description='Link dotfiles to repo')
    parser.add_argument('-c', action="store_true", dest='cowboy',
            help='Cowboy mode. No prompting just clobber everything',
            default=False)
    cmd = parser.parse_args()

    cwd = os.path.dirname(os.path.realpath(__file__))
    ignore = [__file__, ".git", ".gitignore"]
    targets = [f for f in os.listdir(cwd) if f not in ignore]
    for t in targets:
        if query_yes_no("Link %s" % t, 'yes', cowboy_mode=cmd.cowboy):
            create_link(os.path.join(cwd, t), cowboy_mode=cmd.cowboy)

if __name__ == "__main__":
    main()
