"""
The archive method here is based on the dataloc system.
This is a system where when code is run a json file with the output directory
path is written in the repo.

- Pros
  - Can handle general paths

- Cons
  - requires a link to files
  - Has trouble if experiments mix their output folders
"""
from .utilities import git_status_check, git_commit
from datetime import datetime
from jinja2 import Template
import textwrap
import shutil
import click
import json
import re
import os


@click.command("gprune")
@click.argument("label")
@click.option("-m", "--msg", required=True,
              help="msg for first mutation")
@click.option("-b", "--branch", is_flag=True,
              help="whether to bud all sub-branches along with main")
@click.option("-a", "--archive_root",
              help="root directory where we should locate archive")
def cli(label, msg, branch, archive_root):
    """archives code and data files for a mutation and leaf-mutas

    Parameters
    ----------
    label : str
        label for current mutation
    msg : str
        msg to explain pruning/archiving
    branch : bool
        whether to prune all sub-branches as well
    """

    # specify potential archive roots
    base_dirs = ["raw", "intermediate", "cache", "summaries", "results"]
    if archive_root:
        base_dirs.append(archive_root)

    # git check
    cwd = os.getcwd()
    if git_status_check(cwd):
        return None

    # get list of all directories which have label as parent
    if branch:
        exp_dir_l = [os.path.join(cwd, d) for d in os.listdir(cwd)
                     if re.match("^%s" % label, d)]
    else:
        exp_dir_l = [os.path.join(cwd, label)]

    # apply budding/relabeling to all resulting mutations
    for ed in exp_dir_l:
        prune_mutation(ed, label, msg, base_dirs)
        git_msg = "prune experiment %s\n\n%s" % (label, msg)
        git_commit(cwd, git_msg)


def prune_mutation(exp_dir, label, msg, base_dirs):
    """archives the code and data files for a mutation

    Parameters
    ----------
    exp_dir : str
        location for current mutation
    label : str
        current label for parent/root mutation
    msg : str
        message to explain the pruning
    base_dirs : list
        list of potential root locations
    """

    # archive dataloc and get common root
    dataloc_dir = os.path.join(exp_dir, ".dataloc")
    if os.path.exists(dataloc_dir):
        dataloc_paths = [os.path.join(r, f)
                         for r, i, f_l in os.walk(dataloc_dir)
                         for f in f_l if ".json" in f]
    else:
        dataloc_paths = []

    # build paths containing output
    path_l = []
    for cf in dataloc_paths:
        with open(cf, "r") as fd:
            outdirs = json.load(fd)
            for d in outdirs:
                path = outdirs[d]
                path_l.append(path)

    # determine archive root directory
    potential_archive_roots = []
    for p in path_l:
        for d in base_dirs:
            if ("/%s/" % d) in p:
                potential_archive_roots.append(d)

    potential_archive_roots = list(set(potential_archive_roots))

    if len(potential_archive_roots) > 1:
        raise ValueError("Multiple potential archive roots detected")
    elif len(potential_archive_roots) == 1:
        archive_root = potential_archive_roots[0]
    else:
        archive_root = None

    if archive_root:
        dt = datetime.now().strftime("%Y%m%d")
        archive_dir = os.path.join(archive_root, "archive_%s" % dt, label)
        os.makedirs(archive_dir, exist_ok=True)

        # get top lvl dirs for tree move
        rel_path_l = [os.path.relpath(p, archive_root) for p in path_l]
        rel_path_l = list(set(rel_path_l))

        # add deprecated paths
        nrel_path_l = []
        for p in rel_path_l:
            re_pattern = "%s__dep[0-9][0-9]" % p
            dep_paths = [f for f in os.listdir(archive_root)
                         if re.search(re_pattern, f)]
            nrel_path_l.append(p)
            nrel_path_l.extend(dep_paths)

        # move all paths
        for p in nrel_path_l:
            if os.path.exists(os.path.join(archive_root, p)):
                shutil.copytree(os.path.join(archive_root, p),
                                os.path.join(archive_dir, p))
                shutil.rmtree(os.path.join(archive_root, p))

        # move code
        code_dir = os.path.join(archive_dir, "code")
        shutil.copytree(exp_dir, code_dir)

        # write README explaining archive
        with open(os.path.join(archive_dir, "README.txt"), "w") as fd:
            fd.write(msg)

    # remove existing code
    shutil.rmtree(exp_dir)




if __name__ == "__main__":

    cli()
