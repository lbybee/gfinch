from .utilities import git_status_check, git_commit, relabel_dataloc, \
                       relabel_rs, add_rs_msg
from datetime import datetime
from jinja2 import Template
import textwrap
import click
import re
import os


@click.command("gbud")
@click.argument("label")
@click.argument("nlabel")
@click.option("-m", "--msg", required=True,
              help="msg for budding mutation")
@click.option("-b", "--branch", is_flag=True,
              help="whether to bud all sub-branches along with main")
def cli(label, nlabel, msg, branch):
    """takes mutation and all leaf-mutas and buds into separate experiment

    Parameters
    ----------
    label : str
        label for current mutation
    nlabel : str
        new label for experiment
    msg : str
        msg to explain budding
    branch : bool
        whether to prune all sub-branches as well
    """

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
        bud_mutation(ed, label, nlabel, msg)
        git_msg = "bud experiment %s to %s\n\n%s" % (label, nlabel, msg)
        git_commit(cwd, git_msg)


def bud_mutation(exp_dir, label, nlabel, msg):
    """updates a mutation to reflect a new parent/root (label->nlabel)

    Parameters
    ----------
    exp_dir : str
        location for current mutation
    label : str
        current label for parent/root mutation
    nlabel : str
        new label for parent/root
    msg : str
        message to explain the budding

    Notes
    -----
    This is useful when label may itself be a mutation, e.g.

    exp1__expmuta

    with a leaf mutation:

    exp1__expmuta__leafmuta

    and expmuta is budded into its own experiment:

    exp2

    and

    exp2__leafmuta
    """

    # rename exp_dir
    nexp_dir = exp_dir.replace(label, nlabel)
    os.rename(exp_dir, nexp_dir)

    # handle dataloc
    relabel_dataloc(nexp_dir, label, nlabel)

    # update label in runscript
    relabel_rs(nexp_dir, label, nlabel)

    # add message
    add_rs_msg(nexp_dir, msg)


if __name__ == "__main__":

    cli()
