from .utilities import git_status_check, git_commit, relabel_rs, add_rs_msg
import shutil
import click
import os


@click.command("gnote")
@click.argument("label")
@click.option("-m", "--msg", required=True,
              help="msg to add to exp")
def cli(label, msg):
    """creates a new mutation from existing experiment

    Parameters
    ----------
    label : str
        label for experiment
    msg : str
        msg added to exp
    """

    cwd = os.getcwd()
    git_msg = "comment experiment %s\n\n%s" % (label, msg)

    # add message
    exp_dir = os.path.join(cwd, label)
    add_rs_msg(exp_dir, msg)

    # git commit
    git_commit(cwd, git_msg)


if __name__ == "__main__":

    cli()
