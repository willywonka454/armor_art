waiting_for_sample = False
waiting_for_color = False

def reset():
    global waiting_for_sample
    global waiting_for_color
    waiting_for_sample = False
    waiting_for_color = False