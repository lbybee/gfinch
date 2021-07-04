from .utilities import git_status_check, git_commit, relabel_rs, add_rs_msg
import shutil
import click
import os


@click.command("gmuta")
@click.argument("label")
@click.argument("mlabel")
@click.option("-m", "--msg", required=True,
              help="msg explaining mutation")
@click.option("-b", "--bud", is_flag=True,
              help="whether to bud the mutation")
def cli(label, mlabel, msg, bud):
    """creates a new mutation from existing experiment

    Parameters
    ----------
    label : str
        label for new experiment
    mlabel : str
        new label for experiment
    msg : str
        msg explain mutation
    bud : bool
        whether to bud the mutation
    """

    # git check
    cwd = os.getcwd()
    if git_status_check(cwd):
        return None

    # form new label
    if bud:
        nlabel = mlabel
    else:
        nlabel = "_".join([label, mlabel])
    git_msg = "mutate experiment %s to %s\n\n%s" % (label, nlabel, msg)

    # copy files (ignoring cache)
    oexp_dir = os.path.join(cwd, label)
    nexp_dir = os.path.join(cwd, nlabel)
    shutil.copytree(oexp_dir, nexp_dir,
                    ignore=shutil.ignore_patterns(".cache",
                                                  ".dataloc",
                                                  "joblib",
                                                  "__pycache__"))

    # update label in runscript
    relabel_rs(nexp_dir, label, nlabel)

    # add message
    add_rs_msg(nexp_dir, msg)

    # git commit
    git_commit(cwd, git_msg)


if __name__ == "__main__":

    cli()
