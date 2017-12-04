# Get frame_range values from selected Viewer
value = nuke.selectedNode().knob('frame_range').getValue()
print value
firstlast = value.split("-")
print firstlast


", ".join(firstlast)

# What is a dict isnt that what I need to make ? or do I need to rejoin firstlast at pos '0' & '1' seperated by "-"