# gfinch

A set of tools for evolving experiments in git.

## ggen

Generates a new folder containing a runscript to run the corresponding `module` code.  For example calling:

`ggen calc_model_est -m "Calculate model estimates"`

will generate a folder called `calc_model_est` containing the corresponding runscript along with notes for the creation date with the message "Calculate model estimates" in the runscript.

Additionally, this will make a git commit noting that the experiment `calc_model_est` was generated.

## gmuta

Generates a new version of a corresponding project/folder from an existing project/folder.  For instance, if called in ranger on the `calc_model_est` folder from the previous example:

`gmuta std -m "Generate new model estimates using standardized data"`

Will generate a new folder called `calc_model_est_std` with an additional note in the runscript "Generate new model estimates using standardized data".

If a new version is desired that isn't attached to the previous the `-b` flag can be used -- again calling `gmuta` on the above created folder:

`gmuta fit_std_model -b -m "Fit a new standardized model"`

Will generate a new folder copying the contents of `calc_model_est` labeled `fit_std_model` with the corresponding runscript note, "Fit a new stadardized model".

Additionally, regardless of the flags, this will make a git commit noting that the experiment `calc_model_est` was mutated to either `calc_model_est_std` or `fit_std_model` depending on the example used.
