# Using best-first search to generate an optimal tab configuration from a sequence of chords
# Chords are represented as sorted tuples of notes, and notes are represented as integers
#  measured from the low E string and counted along the chromatic scale.
# Tabs are tuples of 6 elements, either None or a nonnegative number measured wrt the corresponding string.

import heapq as hp

strings = (0, 5, 10, 15, 19, 24) # E, A, D, G, B, E
spread  = 5 # maximum distance between fingers
maxfret = 19

# may also return list of configurations, sorted by optimality and cut off after a certain number
def config(chords, ignoreoctaves = False):
    'Traverse tab configurations starting from the first chord, returning the optimal one.'
    # The neighbors of an incomplete configuration are configurations with the next chord complete 
    openset = [(0, ())]
    dists   = {() : 0}
    length  = len(chords)
    
    while openset:
        current = hp.heappop(openset)[1]
        i = len(current)
        if i == length: # found first complete configuration
            return list(current)
        for tab in tabs(chords[i], ignoreoctaves):
            # is it necessary to calculate the new distance, as the new item will never be traversed before?
            newdist = dists[current] + (distance(current[-1], tab) if current else sum(filter(None, tab))) # hack
            newitem = current + (tab,)
            if newitem not in dists or newdist < dists[newitem]:
                dists[newitem] = newdist
                hp.heappush(openset, (newdist, newitem))
    return None

# TODO make this iterative
def tabs(chord, ignoreoctaves = False):
    'Generate all possible tabs of a given chord.'
    # For each note in chord, try each string with value less than the note
    if len(chord) == 0:
        yield (None,) * 6
    else:
        for i in xrange(6):
            if strings[i] <= chord[0] < strings[i] + maxfret: # TODO modify for ignoreoctaves, perhaps by adding 12 iteratively
                for tab in tabs(chord[1:]):
                    if tab[i] is None: # ith string previously unoccupied
                        tab = tab[:i] + (chord[0] - strings[i],) + tab[i+1:]
                        if viable(tab):
                            yield tab

def distance(tab1, tab2):
    'Measure the effort spent in moving from tab1 to tab2 using an edit distance.'
    # The following should count as unit moves:
    # - Holding or releasing a string (conversion from or to 0/None)
    # - Moving a string one semitone up or down
    # - Transposing two adjacent strings
    # Perhaps measure edit distance on the True elements of the tabs, something like Damerau-Levenshtein distance
    # Memoize starting from the 0th index and up to the ith, considering the distance swapping the ith and (i+1)th strings
    pass

def viable(tab):
    'Check the spread and number of fingers of tab and return if they are viable.'
    frets = filter(None, tab) # extract fingers not None or 0
    return not frets or max(frets) - min(frets) <= spread and (len(frets) <= 4 or len(frets) == 5 and tab[0])