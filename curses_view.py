import curses
from bear import Bear
from lumberjack import Lumberjack

class CursesView(object):
    """A three-pane view displaying a map, recent logs, and the current state."""
    def __init__(self, forest, statistics_batch, record):
        self.forest = forest
        self.statistics_batch = statistics_batch
        self.record = record
        self.width, self.height = -1, -1
        self.bottom_pane_height = 20
        self.right_pane_width = 35

    def initialize(self):
        self.terrain = TerrainPane(self.forest)
        self.state_shower = StateShowerPane(self.forest, self.statistics_batch)
        self.state_shower.width = self.right_pane_width
        self.log_shower = LogShowerPane(self.forest.record)
        self.log_shower.height = self.bottom_pane_height

    def display(self, screen):
        screen.erase()
        if curses.LINES != self.height or curses.COLS != self.width:
            self.width, self.height = curses.COLS, curses.LINES
            curses.curs_set(0)
            self.terrain.height = self.height - self.log_shower.height
            self.terrain.width = self.width - self.state_shower.width
            self.state_shower.height = self.terrain.height
            self.state_shower.left = self.terrain.width
            self.log_shower.width = self.terrain.width
            self.log_shower.top = self.terrain.height

        for pane in [self.terrain, self.state_shower, self.log_shower]:
            pane.draw(screen)
        screen.refresh()

class Pane(object):
    """A section of the screen to divide data into."""
    def __init__(self, height=0, width=0, top=0, left=0):
        # Using height, width instead of width, height for consistency with curses
        self.height = height
        self.width = width
        self.top = top
        self.left = left

    def draw(self, screen):
        pass

class TerrainPane(Pane):
    def __init__(self, forest, height=0, width=0, top=0, left=0, x_offset=0, y_offset=0):
        Pane.__init__(self, height, width, top, left)
        self.forest = forest
        self.x_offset = x_offset
        self.y_offset = y_offset

    def draw(self, screen):
        screen_x = self.left
        for x in xrange(self.x_offset, min(self.x_offset + self.width, len(self.forest.layout))):
            screen_y = 0
            for y in xrange(self.y_offset, min(self.y_offset + self.height, len(self.forest.layout[x]))):
                screen.addstr(screen_y, screen_x, self.forest.layout[x][y].short())
                screen_y += 1
            screen_x += 1

class StateShowerPane(Pane):
    def __init__(self, forest, statistics, height=0, width=0, top=0, left=0, x_offset=0, y_offset=0):
        Pane.__init__(self, height, width, top, left)
        self.forest = forest
        self.statistics = statistics

    def draw(self, screen):
        screen_y, screen_x = self.top, self.left
        digits = 4
        screen_x_num = screen_x + self.width - digits # where to start writing numbers
        for entity_type in self.forest.population:
            screen.addnstr(screen_y, screen_x, str(entity_type.__name__), self.width)
            screen.addnstr(screen_y, screen_x_num, str(self.forest.get_total_of_entity(entity_type)), digits)
            screen_y += 1
        screen_y += 1
        for key in self.statistics.keys():
            screen.addnstr(screen_y, screen_x, 'Lumberjacks Mawed ({0})'.format(key), self.width)
            screen.addnstr(screen_y, screen_x_num, str(self.statistics[key]['lumberjacks mawed']), digits)
            screen_y += 1
            screen.addnstr(screen_y, screen_x, 'Lumber Collected ({0})'.format(key), self.width)
            screen.addnstr(screen_y, screen_x_num, str(self.statistics[key]['lumber collected']), digits)
            screen_y += 2

        screen.addnstr(screen_y, screen_x, 'Month {0}'.format(self.forest.current_tick), self.width)

class LogShowerPane(Pane):
    def __init__(self, record, height=0, width=0, top=0, left=0):
        Pane.__init__(self, height, width, top, left)
        self.record = record

    def draw(self, screen):
        for screen_y in xrange(0, min(self.height, len(self.record.records))):
            screen.addnstr(self.top + self.height - screen_y - 1, self.left, self.record.records[-(screen_y + 1)], self.width)
