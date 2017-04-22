r = nuke.Root()
f = r.knob('first_frame').value()
n = nuke.selectedNode()

n['frame'].setValue(str(f))
n['frame_mode'].setValue('start_at')