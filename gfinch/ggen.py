from .utilities import git_status_check, git_commit, prep_msg
from pkg_resources import resource_string
from jinja2 import Template
import click
import os


@click.command("ggen")
@click.argument("label")
@click.option("-m", "--msg", required=True,
              help="msg for first mutation")
@click.option("-b", "--base_dir", default="/home/lbybee/globalfs",
              help="base directory which all ops are relative to")
def cli(label, msg, base_dir):
    """create a new experiment

    Parameters
    ----------
    label : str
        label for new experiment/scratch
    msg : str
        msg for first mutation
    base_dir : str
        base directory which all ops are relative to
    """

    # git check
    cwd = os.getcwd()
    if git_status_check(cwd):
        return None
    git_msg = "generate experiment %s\n\n%s" % (label, msg)

    # prep message
    msg = prep_msg(msg)

    # build initial content
    template = resource_string("templates", "experiment.py")
    template = template.decode("utf-8")
    template = Template(template)
    content = template.render(msg=msg, base_dir=base_dir, label=label)

    # create experiment dir and runscript
    exp_dir = os.path.join(os.getcwd(), label)
    os.makedirs(exp_dir, exist_ok=True)
    with open(os.path.join(exp_dir, "runscript.py"), "w") as fd:
       fd.write(content)

    # commit new experiment
    git_commit(cwd, git_msg)


if __name__ == "__main__":

    cli()
