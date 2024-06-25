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

        ok because in our process we must ask our self when and how i can return the known mines of cells ??? of course if the number of cells 
        are same number of count which indicate to the number of mines so:-
        """
        if len(self.cells)==self.count:
            return set(self.cells)
        return set()
       

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        the same process when we ask our self , of course the awnser is when the count equal zero that mean there is no mine cell so we return the safe cells so:-
        """
        if self.count==0:
            return set(self.cells)
        return set()
      

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine. so in this process we will remove any cell that known is a mine and reduce the number of count by one 
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe. and if we know that this cell is safe then we remove it from our cells but of course withought reduce any counting because it is already
        save that mean no effect on the number of cells
    
        """
        if cell in self.cells:
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
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # add a new sentence to the AI's knowledge bas  based on the value of `cell` and `count`
        i, j = cell
        neighbors = set()
        # so first of all we need to defined the cell if it is unkown or not by make a coordinate for cell and move to neighbors ones
        for di in [-1, 0, 1]:  
        #represents the possible moves in rows under ,above and no move 
          for dj in [-1, 0, 1]:  
          #represents the possiple moves in column left ,right and no move 
           
            if (di, dj) != (0, 0):
            # ensure that we are not in the same cell
              ni, nj = i + di, j + dj 
              # move depend on the for loop and ensure that not a safe or not a mine 
              if 0 <= ni < self.height and 0 <= nj < self.width: 
              # ensure that we move inside game not out of the game 
                 if (ni, nj) not in self.safes and (ni, nj) not in self.mines: 
                 # ensure that the neighbor cell we move to it , is nither safe nore mane 
                    neighbors.add((ni, nj)) 
                    # add to neighbors group

        if neighbors:
            self.knowledge.append(Sentence(neighbors, count)) 
        
        # to defined new safes and mines        
        new_safes = set()
        new_mines = set()

        for sentence in self.knowledge:
            new_safes.update(sentence.known_safes())
            new_mines.update(sentence.known_mines())

        for safe in new_safes:
            self.mark_safe(safe)

        for mine in new_mines:
            self.mark_mine(mine)

        # add new knowladge
        new_knowledge = []

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells < sentence2.cells:
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    
                    if Sentence(new_cells, new_count) not in self.knowledge and new_cells:
                        new_knowledge.append(Sentence(new_cells, new_count))
        
        self.knowledge.extend(new_knowledge)

       

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None
    
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        choices = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        if choices:
            return random.choice(choices)
        return None
       