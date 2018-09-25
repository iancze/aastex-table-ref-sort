from astropy.table import Table,Column
from astropy.io import ascii
from collections import OrderedDict

# This function could be helpful to include in a larger routine used for writing your table.

def reformat_column(refcolumn):
    '''
    Takes in a column of citation keys, reformats them as numbers and a lookup list in the comments.
    '''

    index = 1
    refdict = OrderedDict()

    # go through each row and create a set of all the keys as they appear
    for row in refcolumn:
        # most columns will a list of more than one key, separated by a comma
        for citekey in row.split(","):
            if citekey not in refdict.keys():
                # add the reference to the list
                refdict[citekey] = index
                # update the current number
                index += 1

    # cycle through the rows and replace the references list with a list of numbers
    newcolumn = Column(name=refcolumn.name, length=len(refcolumn), dtype="S64")

    for i in range(len(refcolumn)):
        citekeys = refcolumn[i].split(",")
        newcolumn[i] = ",".join(["{:d}".format(refdict[key]) for key in citekeys])

    # Assemble all numbers with their ref keys as a string, and return this too.
    citestring = ", ".join(["{:d}) ".format(val) + "\citet{" + key +  "}" for key,val in refdict.items()])

    return newcolumn, citestring
