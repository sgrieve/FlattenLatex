#!/usr/bin/python
import os
import sys
import re


def Flatten(BasePath, Filename, Outfile=None, Output=[]):
    '''
    Code to flatten a University of Edinburgh LaTeX thesis into a single file
    to enable latexdiff to be run on it.

    Should be run from the command line. If no output filename is given the full
    thesis will be written to screen. If an output filename is given it will
    write the full thesis to that file.

    Pass in:
    - path to the thesis file (the one you compile to build the whole thesis)
    - name of the file that is used to build the thesis eg ed_thesis.tex
    - filename of an output file to be created (optional)
    - an empty list used to store data if being written to file (ignore this)
    '''

    os.chdir(BasePath)

    DirPattern = re.compile('newcommand{(.*)}{(.*)}')
    TexPattern = re.compile('\\input{(.*\.tex)}')

    DirValue = ''

    with open(Filename, 'r') as texfile:
        for line in texfile.readlines():
            # ignore comments
            if line.strip().startswith('%'):
                pass
            else:
                # get the current value of the dir variable
                DirSearch = DirPattern.search(line)
                if DirSearch and DirSearch.group(1) == '\dir':
                    DirValue = DirSearch.group(2)
                else:
                    # find where tex files are input and recursively open them
                    InputSearch = TexPattern.search(line)
                    if InputSearch:
                        # build the relative path to the next file
                        NextFile = DirValue + InputSearch.group(1).strip('\dir')
                        Flatten(BasePath, NextFile, Outfile, Output)
                    else:
                        # once all that is done write lines to screen or file
                        if Outfile:
                            Output.append(line)
                        else:
                            sys.stdout.write(line)

    # write the data to file if requested
    if Outfile:
        with open(Outfile, 'w') as OutWriter:
            for line in Output:
                OutWriter.write(line)


def SanitizeInputs(path, filename, outname):
    '''
    Check the input arguments to ensure the path is valid, the input file
    exists, the output file does not exist, and the input and output files have
    the .tex extension.
    '''
    if not os.path.exists(path):
        sys.exit('\n{} is not a valid path.\n'.format(path))

    if outname:
        if not outname.lower().endswith('.tex'):
            outname = outname + '.tex'
    if not filename.lower().endswith('.tex'):
        filename = filename + '.tex'

    if not os.path.isfile(path + filename):
        sys.exit('\nInput file, {}, does not exist.\n'.format(filename))
    if outname:
        if os.path.isfile(path + outname):
            sys.exit('\nOutput file, {}, is an existing file.\n'
                     .format(outname))

    return path, filename, outname


def Run(path, filename, outname=None):
    """
    Simple wrapper that calls the SanitizeInputs() method then the Flatten()
    method.
    """
    CleanPath, CleanName, CleanOut = SanitizeInputs(path, filename, outname)
    Flatten(CleanPath, CleanName, CleanOut)


if __name__ == "__main__":
    if (len(sys.argv) == 1) or (sys.argv[1] == '--help'):
        sys.exit('\nCode to flatten a University of Edinburgh LaTeX thesis\n'
                 'into a single file to enable latexdiff to be run on it.\n\n'
                 'Works best with latexdiff version 1.2.0\n\n'
                 'SWD Grieve July 2016\n'
                 '\n{} needs at least 2 arguments:\n\n'
                 '[1] The path to the main thesis file\n'
                 '[2] The name of the main thesis file, usually ed_thesis.tex\n'
                 '[3] (Optional) An output filename\n\n'
                 'Run {} with the command --help for help\n'
                 .format(sys.argv[0], sys.argv[0]))
    else:
        if len(sys.argv) == 3:
            Run(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 4:
            Run(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            sys.exit('\n{} needs at least 2 arguments:\n\n'
                     '[1] The path to the main thesis file\n'
                     '[2] The name of the main thesis file, usually '
                     'ed_thesis.tex\n'
                     '[3] (Optional) An output filename\n\n'
                     'Run {} with the command --help for help\n'
                     .format(sys.argv[0], sys.argv[0]))
