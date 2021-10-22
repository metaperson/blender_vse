import bpy

strip1 = bpy.data.scenes["Scene"].sequence_editor.sequences_all["Strip1"]
strip2 = bpy.data.scenes["Scene"].sequence_editor.sequences_all["Strip2"]
strip3 = bpy.data.scenes["Scene"].sequence_editor.sequences_all["Strip3"]

# coordinate of strip
#format_str = '{:>8} | {:>12} {:>20} {:>20} {:>20}'
#print()
#print(format_str.format('name', 'frame_start', 'frame_final_start', 'frame_offset_start', 'frame_still_start'))
#print('-' * 90)
#print(format_str.format(strip1.name, strip1.frame_start, strip1.frame_final_start, strip1.frame_offset_start, strip1.frame_still_start))
#print(format_str.format(strip2.name, strip2.frame_start, strip2.frame_final_start, strip2.frame_offset_start, strip2.frame_still_start))
#print(format_str.format(strip3.name, strip3.frame_start, strip3.frame_final_start, strip3.frame_offset_start, strip3.frame_still_start))

# experiment #1
#strip3.frame_final_start = 60

# experiment #2
#strip3.frame_start = 60

# experiment #3
#strip3.frame_start += (60 - strip3.frame_final_start)

# experiment #4
#strip3.channel = 4
#strip3.frame_start += (93 - strip3.frame_final_start)

# experiment #5
#strip3.frame_start += (93 - strip3.frame_final_start)
#strip3.channel = 4

# experiment #6
#(strip3.channel, strip3.frame_start) = (4, strip3.frame_start + 93 - strip3.frame_final_start)

# experiment #7
#(strip3.frame_start, strip3.channel) = (strip3.frame_start + 93 - strip3.frame_final_start, 4)

# experiment #8
#frame_movement = 93 - strip3.frame_final_start
#channel_movement = 4 - strip3.channel
#strip3.select = True
#bpy.ops.transform.seq_slide(value=(frame_movement, channel_movement))

# experiment #9
#frame_movement = 93 - strip3.frame_final_start
#channel_movement = 4 - strip3.channel
#save_type = bpy.context.area.type           # store the current window state
#bpy.context.area.type = 'SEQUENCE_EDITOR'   # set into the sequencer window
#strip3.select = True
#bpy.ops.transform.seq_slide(value=(frame_movement, channel_movement))
#bpy.context.area.type = save_type           # restore the original state
