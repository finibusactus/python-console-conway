from threading import Timer

class Game:
    'This program assumes the top left corner is (0,0) and the program is written to ALWAYS ASSUME this'
    'Program internals such as self.squares_alive and self.top_left and self.cursor_position, etc uses 0 based indexing'
    '[-Infinity, -Infinity]  < self.squares_alive[x,y] < [Infinity, Infinity]'
    '[-Infinity, -Infinity]  < self.top_left[x,y] < [Infinity, Infinity]'
    '[0,0] >= self.cursor_position[x,y] < [TERMINAL_WIDTH, TERMINAL_HEIGHT]'
    'TERMINAL_WIDTH and TERMINAL_HEIGHT >= 1'

    def __init__(self, TERMINAL_WIDTH, TERMINAL_HEIGHT):
        self.TERMINAL_WIDTH = TERMINAL_WIDTH
        self.TERMINAL_HEIGHT = TERMINAL_HEIGHT
        self.squares_alive = set()
        self.cursor_position = [0,0]
        self.top_left = [0,0]
        self.character_scale_factor = 1
        self.game_loop_callback = None
        self.game_loop_speed = 1
        self.game_loop_paused = False
        self.previous_screen_state = ''

    def quit(self):
        'we have to close the threads before leaving'
        self.game_loop_callback.cancel()
        return

    def _redraw(self):
        'quite unoptimised, TODO fix'
        OUTPUT_MAP = {False:".", True: "\x1b[1;93m#\x1b[0m"}
        text = ''
        tmp_array = []
        i = self.top_left[1]
        while i < (self.TERMINAL_HEIGHT + self.top_left[1]) * self.character_scale_factor:
            j = self.top_left[0]
            while j < (self.TERMINAL_WIDTH + self.top_left[0]) * self.character_scale_factor:
                num =  0
                for x in range(j, j + self.character_scale_factor):
                    for y in range(i, i + self.character_scale_factor):
                        num += 1 if (x,y) in self.squares_alive else 0
                text += OUTPUT_MAP[True] if num > 0 else OUTPUT_MAP[False]
                j += self.character_scale_factor
            i += self.character_scale_factor
        full_text = '\r' + text + f'\x1b[{self.cursor_position[1]+1};{self.cursor_position[0]+1}H'
        'only draw if neccessary'
        if full_text == self.previous_screen_state:
            return
        self.previous_screen_state = full_text
        print()
        print('\r' + text + f'\x1b[{self.cursor_position[1]+1};{self.cursor_position[0]+1}H', end='', flush=True)

    def _yield_coordinates_of_neighbours(self, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i == x and j == y:
                    continue
                yield (i, j)

    def _get_neighbours_count_of_cell(self, x, y):
        num = 0
        for x1, x2 in self._yield_coordinates_of_neighbours(x, y):
            if (x1, x2) in self.squares_alive:
                num += 1
        return num
    

    def _update_cells(self):
        new_set = self.squares_alive.copy()
        for x, y in self.squares_alive:
            neighbours = self._get_neighbours_count_of_cell(x, y)
            if neighbours < 2:
                new_set.remove((x, y))
            elif neighbours > 3:
                new_set.remove((x, y))
            for x2, y2 in self._yield_coordinates_of_neighbours(x, y):
                if self._get_neighbours_count_of_cell(x2, y2) == 3:
                    new_set.add((x2, y2))
        if self.squares_alive == new_set:
            return
        self.squares_alive = new_set
        self._redraw()


    def _handle_screen_movement(self, x_offset, y_offset):
        'updates the current cursor position if able to, if at the edge of a line, translate the screen.'
        if x_offset == 0 and y_offset == 0:return
        assert self.cursor_position[0] <= self.TERMINAL_WIDTH - 1
        assert self.cursor_position[1] <= self.TERMINAL_HEIGHT - 1

        self.cursor_position[0] += x_offset
        x_translation = 0
        if self.cursor_position[0] < 0:
            x_translation = self.cursor_position[0]
            self.cursor_position[0] = 0
        elif self.cursor_position[0] >= self.TERMINAL_WIDTH:
            x_translation = self.cursor_position[0] - (self.TERMINAL_WIDTH-1)
            self.cursor_position[0] = self.TERMINAL_WIDTH - 1
        self.top_left[0] += x_translation

        self.cursor_position[1] += y_offset
        y_translation = 0
        if self.cursor_position[1] < 0:
            y_translation = self.cursor_position[1]
            self.cursor_position[1] = 0
        elif self.cursor_position[1] >= self.TERMINAL_HEIGHT:
            y_translation = self.cursor_position[1] - (self.TERMINAL_HEIGHT-1)
            self.cursor_position[1] = self.TERMINAL_HEIGHT - 1
        self.top_left[1] += y_translation
        self._redraw()

    def handle_key_press(self, key: bytearray):
        if key in [b'UP', b'W', b'w']:
            self._handle_screen_movement(0,-1*self.character_scale_factor)
        elif key in [b'RIGHT', b'D', b'd']:
            self._handle_screen_movement(1*self.character_scale_factor,0)
        elif key in [b'DOWN', b's', b'S']:
            self._handle_screen_movement(0,1*self.character_scale_factor)
        elif key in [b'LEFT', b'A', b'a']:
            self._handle_screen_movement(-1*self.character_scale_factor,0)
        elif key in [b'T', b't']:
            # because coordinates are relative and the reference frame of the top left corner changes based on the mouse position AND the screen translation i.e. self.top_left
            x, y = self.cursor_position
            x += self.top_left[0]
            y += self.top_left[1]
            if (x,y) in self.squares_alive:
                self.squares_alive.remove((x,y))
            else:
                self.squares_alive.add((x,y))
            self._redraw()
        elif key == b'-':
            self.game_loop_callback.cancel()
            self.start_game_loop(self.game_loop_speed*1.5)
        elif key == b'+':
            self.game_loop_callback.cancel()
            self.start_game_loop(self.game_loop_speed*0.75)
        elif key == b' ':
            self.pause()
            '''
            # unimplemented zoom functions
        elif key == b'z':
            self.character_scale_factor += 1
        elif key == b'x':
            self.character_scale_factor = max(1, self.character_scale_factor-1)
            '''
        elif key in [b'f', b'F']:
            self._update_cells()

    
    def pause(self):
        if self.game_loop_callback == None:
            print('ERROR, function self.start_game_loop must first be called')
            exit()
        if self.game_loop_paused == False:
            self.game_loop_callback.cancel()
            self.game_loop_paused = True
        else:
            self.start_game_loop(self.game_loop_speed)


    def start_game_loop(self, secs=1):
        def wrapper():
            self.start_game_loop(secs)
            self._update_cells()
        t = Timer(secs, wrapper)
        t.start()
        self.game_loop_callback = t
        self.game_loop_speed = secs
        self.game_loop_paused = False
    
    def load_cell_data(self, data: set, pause_after_load = True):
        self.squares_alive = data