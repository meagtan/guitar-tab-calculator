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
    # The items traversed are pairs (i, t) where t is a tab of chords[i]
    openset = []
    dists   = {}
    preds   = {}
    length  = len(chords)
    
    for tab in tabs(chords[0], ignoreoctaves):
        hp.heappush(openset, (heur(tab), (0, tab)))
        dists[0, tab] = 0
    
    while openset:
        i, t = hp.heappop(openset)[1]
        
        # found first complete configuration
        if i == length - 1: 
            res = []
            while (i, t) in preds:
                res.append(t)
                i, t = preds[i, t]
            res.append(t)
            res.reverse()
            return res
        
        for tab in tabs(chords[i+1], ignoreoctaves):
            # is it necessary to calculate the new distance, as the new item will never be traversed before?
            newdist = dists[i, t] + distance(t, tab)
            newitem = (i + 1, tab)
            if newitem not in dists or newdist < dists[newitem]:
                dists[newitem] = newdist
                preds[newitem] = i, t
                hp.heappush(openset, (newdist + heur(tab), newitem))
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
    # TODO change this and heur later to suit this measure
    return sum(map(lambda i, j: abs((i if i else 0) - (j if j else 0)), tab1, tab2))

def heur(tab):
    'Estimate the cost of tab.'
    return sum(filter(None, tab))

def viable(tab):
    'Check the spread and number of fingers of tab and return if they are viable.'
    frets = filter(None, tab) # extract fingers not None or 0
    return not frets or max(frets) - min(frets) <= spread and (len(frets) <= 4 or len(frets) == 5 and tab[0])
