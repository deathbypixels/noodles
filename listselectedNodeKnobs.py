n = nuke.selectedNode()
for i in range (n.getNumKnobs()):
    print n.knob (i).name()