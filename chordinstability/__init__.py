# I want this to expose the functions via
# chordinstability.instability
# not
# chordinstability.instability.instability
# So I moved everything into lib, and import the functions here. I think there
# would be a name-clash between module and function otherwise

from .lib.dissonance import dissonance
from .lib.tension import tension
from .lib.instability import instability
