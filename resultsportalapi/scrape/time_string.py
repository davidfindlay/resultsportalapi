# Convert time string into seconds
def convert_time(time_str):
    sec, ms = time_str.split('.')
    min_sec = 0

    if ':' in sec:
        min, sec = sec.split(':')

        min_sec = int(min) * 60

    sec = min_sec + int(sec) + (int(ms) / 100)

    return sec

def display_time(time_number):

    min = time_number // 60
    secs = time_number % 60

    return "%i:%05.2f" % (min, secs)