import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells.copy():
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells.copy():
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """        
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        cells_to_add = set()
        cells_to_add.add((cell[0]+1, cell[1]+1))
        cells_to_add.add((cell[0]+1, cell[1]+0))
        cells_to_add.add((cell[0]+1, cell[1]-1))
        cells_to_add.add((cell[0]+0, cell[1]-1))
        cells_to_add.add((cell[0]-1, cell[1]-1))
        cells_to_add.add((cell[0]-1, cell[1]+0))
        cells_to_add.add((cell[0]-1, cell[1]+1))
        cells_to_add.add((cell[0]+0, cell[1]+1))
        for cell_check in cells_to_add.copy():
            if cell_check[0] < 0 or cell_check[0] >= self.height or cell_check[1] < 0 or cell_check[1] >= self.width:
                cells_to_add.remove(cell_check)
        
        for cell_check in cells_to_add.copy():
            if cell_check in self.mines or cell_check in self.safes:
                cells_to_add.remove(cell_check)
            if cell_check in self.mines:
                count -= 1
                
        
        
        new_sentence = Sentence(cells_to_add, count)
        self.knowledge.append(new_sentence)
        
        #now, check each sentence to see if it is a subset of another sentence. If so remove the subset from the superset, and reduce the superset count by the subset count
        for sentence1 in self.knowledge.copy():
            for sentence2 in self.knowledge.copy():
                if not sentence1 == sentence2:
                    if sentence1.cells.issubset(sentence2.cells) and not len(sentence1.cells) == 0:
                        add_sentence_cells = sentence2.cells - sentence1.cells
                        add_sentence_count = abs(sentence2.count - sentence1.count)
                        add_sentence = Sentence(add_sentence_cells, add_sentence_count)
                        if not len(add_sentence.cells) == 0:
                            self.knowledge.append(add_sentence)
                        self.knowledge.remove(sentence2)
                        # print(f"Reformed Sentence: {add_sentence}")
                        # if len(add_sentence_cells) == 0 and add_sentence_count > 0:
                        #     print(f"Sentence cells empty\n Source Sentences->\nSentence 1: {sentence1}\nSentence 2: {sentence2}")
                        
                        
        #check whole knowledge to see if there are any safes or mines that we can a to self.mine/safes
        for sentence in self.knowledge:
            if sentence.known_mines():
                for mine in sentence.known_mines().copy():
                    # self.mines.add(mine)
                    self.mark_mine(mine)
            if sentence.known_safes():
                # print(f"Adding safes: {sentence}")
                for safe in sentence.known_safes().copy():
                    # self.safes.add(safe)
                    self.mark_safe(safe)
                    
        
        # print(f"Selected Cell: {cell},  New Sentence: {new_sentence}")
        # for i in cells_to_add:
        #     print(i)
        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_move in self.safes:
            if not safe_move in self.moves_made:
                return safe_move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                random_moves.add((i,j))
        
        for move in self.moves_made:
            if move in random_moves.copy():
                random_moves.remove(move)
        for mine in self.mines:
            if mine in random_moves.copy():
                random_moves.remove(mine)
                
        if len(random_moves) == 0:
            return None
        random_list = list(random_moves)
        max_rand = len(random_list)
        index = random.randint(0, max_rand)
        return random_list[index]
        
        
