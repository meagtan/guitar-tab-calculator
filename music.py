# Process music files to be converted into a sequence of chords
# Requires music21: http://web.mit.edu/music21/

from music21 import *

def musictochords(path):
    'Open music file at given directory and convert it into a sequence of chords.'
    try:
        scor = converter.parse(path).chordify()
        res = []
        e, b = pitch.Pitch('E2'), pitch.Pitch('B6')
        for chor in scor.recurse().getElementsByClass('Chord'):
            # TODO differentiate tied notes from others so they can be omitted if the search fails otherwise
            # and include other features such as shifting notes if out of range
            res.append(tuple(int(p.ps - e.ps) for p in chor.pitches if e <= p <= b)) # only include if within range
        return res
    except:
        pass

