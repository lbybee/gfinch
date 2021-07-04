"""
utitlies called by multiple muta methods
"""
from datetime import datetime
from jinja2 import Template
import subprocess
import textwrap
import click
import json
import os


def git_status_check(cwd):
    """check whether there are uncommited changes in current dir

    Parameters
    ----------
    cwd : str
        current working directory to check git status

    Returns
    -------
    bool
        indicating whether there are uncommited changes
    """

    pipe = subprocess.Popen(["git status --porcelain"],
                            stdout=subprocess.PIPE, shell=True, cwd=cwd)
    stdout, stderr = pipe.communicate()
    stdout = stdout.decode()

    if stdout != "":
        click.echo("Uncommited changes exist on branch")
        return True

    else:
        return False


def git_commit(cwd, msg):
    """commit the changes on the current branch

    Parameters
    ----------
    cwd : str
        current working directory to make commit
    msg : str
        message for git commit
    """

    subprocess.call(["git add -A"], shell=True, cwd=cwd)
    subprocess.call(["git commit --quiet -m '%s'" % msg], shell=True, cwd=cwd)


def relabel_dataloc(exp_dir, olabel, nlabel):
    """replace all references in dataloc and file system of olabel with nlabel

    Parameters
    ----------
    exp_dir : str
        directory for experiment
    olabel : str
        old label for experiment
    nlabel : str
        new label for experiment

    Notes
    -----
    dataloc establishes a link between the scripts and output directories
    """

    dataloc_dir = os.path.join(exp_dir, ".dataloc")

    if os.path.exists(dataloc_dir):
        dataloc_paths = [os.path.join(r, f)
                         for r, i, f_l in os.walk(dataloc_dir)
                         for f in f_l if ".json" in f]
    else:
        dataloc_paths = []

    # replace dataloc references
    for cf in dataloc_paths:
        with open(cf, "r") as fd:
            outdirs = json.load(fd)

        for d in outdirs:
            outdirs[d] = outdirs[d].replace(olabel, nlabel)

        with open(cf, "w") as fd:
            json.dump(outdirs, fd)


def relabel_rs(exp_dir, olabel, nlabel):
    """replace references to olabel with nlabel in the exp_dir runscript"""

    runscript = os.path.join(exp_dir, "runscript.py")

    with open(runscript, "r") as fd:
        content = fd.read()

    content = content.replace(olabel, nlabel)

    with open(runscript, "w") as fd:
        fd.write(content)


def add_rs_msg(exp_dir, msg):
    """adds the specified message to the runscript

    Parameters
    ----------
    exp_dir : str
        directory in which all files are located
    msg : str
        message added to runscript to explain the update
    """

    runscript = os.path.join(exp_dir, "runscript.py")

    msg = prep_msg(msg)

    with open(runscript, "r") as fd:
        content = fd.read()
    content_l = content.split('"""')
    notes = content_l[1]
    notes += ("\n" + msg + "\n")
    content_l = content_l[0:1] + [notes] + content_l[2:]
    content = '"""'.join(content_l)
    with open(runscript, "w") as fd:
        fd.write(content)


def prep_msg(msg):
    """formats a message to insert into docstring"""

    dt_base = datetime.now()
    dt = dt_base.strftime("%Y-%m-%d %H:%M:%S")
    dt_date = dt_base.strftime("%Y%m%d")
    template = Template("- {{ dt }} {{ msg }}")
    msg = template.render(dt=dt, msg=msg)
    msg = "\n  ".join(textwrap.wrap(msg, width=77))

    return msg
