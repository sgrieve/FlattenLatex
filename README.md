# FlattenLatex

Python script to flatten an Edinburgh University thesis made using the LaTeX template into a single tex file suitable for running latexdiff on. Really useful for doing corrections.

## Usage

Grab this repo, or download the `FlattenLatex.py` file, and run it from the command line, just like you would with latexdiff. For example:

```
$> python FlattenLatex.py /path/to/thesis ed_thesis.tex Output.tex
```

The first argument should be the path to the thesis file, typically called `ed_thesis.tex`. The second argument should be the name of the file that is used to build the thesis, usually called `ed_thesis.tex`. The third argument is optional and is the name of the file the flattened thesis should be written to. If this is ommited the thesis file is written to the terminal. It can be redirected to a file in the same manner as latexdiff:

```
$> python FlattenLatex.py /path/to/thesis ed_thesis.tex > Output.tex
```

Call the script with the switch `--help` to display the help file.

This has all been desgined to run using python 2.7 and latexdiff 1.2.0 alpha on Ubuntu 14.04, it may well work with other environments, if you epericence trouble running it on other environments try with the output filename specified as this was added to deal with some compatibility issues I had.

SWDG -- July 2016
