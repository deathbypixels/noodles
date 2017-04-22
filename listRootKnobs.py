r = nuke.Root()
for i in range (r.getNumKnobs()):
    print r.knob (i).name()