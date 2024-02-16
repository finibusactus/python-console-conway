def _windows_getkp() -> bytearray:
    from msvcrt import getch, kbhit
    buffer = []
    buffer_bytes = b''
    LEADING_CONTROL_BYTE = [b'\x00', b'\xe0']
    LAST_BYTE_TO_KEY = {b'H':b'UP', b'M':b'RIGHT', b'P':b'DOWN', b'K':b'LEFT', b'I':b'PAGEUP', b'Q':b'PAGEDOWN'}
    SINGLE_BYTE_COMMANDS = {b'\x03':b'CONTROL+C', b'\x04':b'CONTROL+D', b'\x1a':b'CONTROL+Z'}
    has_more = True 
    while has_more:
        ch = getch()
        buffer.append(ch)
        buffer_bytes += ch
        has_more = kbhit()
    if len(buffer) == 2:
        if buffer[0] in LEADING_CONTROL_BYTE and buffer[1] in LAST_BYTE_TO_KEY:
            return LAST_BYTE_TO_KEY[buffer[1]]
        else:
            return buffer_bytes
    elif len(buffer) == 1:
        if buffer[0] in SINGLE_BYTE_COMMANDS:
            return SINGLE_BYTE_COMMANDS[buffer[0]]
        else:
            return buffer_bytes
    return buffer_bytes

def _unix_getch():
    import tty
    import termios
    from sys import stdin
    file_descriptor = stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(stdin.fileno())
        character = stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
    return character

def _unix_getkp():
    ESCAPE = chr(27)
    CONTROL = ESCAPE + '['
    SPECIAL = {CONTROL+'A':'UP', CONTROL+'B':'DOWN', CONTROL+'C':'RIGHT', CONTROL+'D':'LEFT', CONTROL+'5~':'PAGEUP', CONTROL+'6~':'PAGEDOWN'}
    buffer = _unix_getch()
    while any(i.startswith(buffer) for i in SPECIAL.keys()):
        if buffer in SPECIAL:
            return SPECIAL[buffer]
        buffer += _unix_getch
    return buffer.decode()

def getkp() -> bytearray:
    try:
        return _windows_getkp()
    except ImportError:
        return _unix_getkp()

def csv_data_to_set(file_name):
    import csv
    data = set()
    with open(file_name) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.add((int(row['x']), int(row['y'])))
    return data

def set_to_csv_data(file_name, set_data):
    import csv
    fieldnames = ['x', 'y']
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in set_data:
            x, y = data
            writer.writerow({'x':x, 'y':y})






'currently unused function'
def clear_screen():
    for i in range(200):
        print('\n')



