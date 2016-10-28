# Using A* search to generate an optimal tab configuration from a sequence of chords
# Chords are represented as sorted tuples of notes, and notes are represented as integers
#  measured from the low E string and counted along the chromatic scale.
# Tabs are tuples of 6 elements, either None or a nonnegative number measured wrt the corresponding string.

strings = (0, 5, 10, 15, 19, 24) # E, A, D, G, B, E
spread  = 5 # maximum distance between fingers
maxfret = 19

# may also return list of configurations, sorted by optimality and cut off after a certain number
def config(chords):
    'Traverse tab configurations starting from the first chord, returning the optimal one.'
    # The neighbors of an incomplete configuration are configurations with the next chord complete 
    pass

# TODO make this iterative
def tabs(chord, ignoreoctaves = False):
    'Generate all possible tabs of a given chord.'
    # For each note in chord, try each string with value less than the note
    if len(chord) == 0:
        yield (None,) * 6
    else:
        for i in xrange(6):
            if strings[i] < chord[0] < strings[i] + maxfret: # TODO modify for ignoreoctaves
                for tab in tabs(chord[1:]):
                    if tab[i] is None: # ith string previously unoccupied
                        tab = tab[:i] + (chord[0] - strings[i],) + tab[i+1:]
                        if viable(tab):
                            yield tab

def distance(tab1, tab2):
    'Measure the effort spent in moving from tab1 to tab2.'
    pass

def viable(tab):
    'Check the spread and number of fingers of tab and return if they are viable.'
    frets = filter(None, tab) # extract fingers not None or 0
    return max(frets) - min(frets) <= spread and (len(frets) <= 4 or len(frets) == 5 and tab[0])