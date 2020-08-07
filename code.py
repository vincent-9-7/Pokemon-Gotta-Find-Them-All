import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import time
from time import strftime, localtime
import math
import random
import re

from PIL import Image, ImageTk

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"
TASK_ONE = 'Run Task One'
TASK_TWO = 'Run Task Two'




class BoardView(tk.Canvas): 
    """
    The view of the game board.
    """
    
    def __init__(self, master,grid_size,board_width=600,*args,**kwargs) : 
        """
        Parameters:
        master:The game window
        grid size: Size of game
        Board_width: size of window
        """

        super().__init__(master, width=board_width, height=board_width)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._width = int(board_width/grid_size)

    def draw_board(self,board,bd_position):
        """
        Draw the board of task1.
        """

        self.clear_canvas() 
        position_x = 0
        position_y = 0
            
        for i in range(len(board)): #get the each cell in the game string

            x1 = position_x * self._width
            y1 = position_y * self._width
            x2 = x1 + self._width
            y2 = y1 + self._width
            
            if board[i] == '~': 
                
                self._canvas.create_rectangle(x1,y1,x2,y2,fill='darkgreen') #Use the x,y location to draw

                if position_x < self._grid_size - 1: #If the (x) is not out of the ground, then +1
                    
                    position_x += 1
                else:#If the (x) is  out of the ground, then change to 0, and y+1
                    position_y += 1
                    position_x = 0
                    
            elif board[i] == '♥':

                self._canvas.create_rectangle(x1,y1,x2,y2,fill='red') #same as above

                if position_x < self._grid_size - 1:
                    
                    position_x += 1
                else:
                    position_y += 1
                    position_x = 0

            elif board[i] == '☺': 
                    
                self._canvas.create_rectangle(x1,y1,x2,y2,fill='yellow') #same as above
                
                if position_x < self._grid_size - 1:
                    
                    position_x += 1
                else:
                    position_y += 1
                    position_x = 0

            else: #If the string is number
                
                word_x = x1 + (self._board_width/self._grid_size)/2 #get the middle position of the click position
                word_y = y1 + (self._board_width/self._grid_size)/2
                word_pixel = [word_x,word_y]
                
                self._canvas.create_rectangle(x1,y1,x2,y2,fill='lightgreen')
                self._canvas.create_text(word_pixel[0],word_pixel[1],text=board[i]) #Change the inside words to the number of pokemon near this cell

                if position_x < self._grid_size - 1:
                    
                    position_x += 1

                else:

                    position_y += 1
                    position_x = 0
         

            
        if bd_position != 0:   #Run this, means in Task2 add the shadow of each cells
            
            x1 = bd_position[0]
            y1 = bd_position[1]
            x2 = bd_position[2]
            y2 = bd_position[3]

            self._canvas.create_rectangle(x1,y1,x2,y2,outline='peach puff',width=3) #Add the outline of cells
        
        else:
            pass

    def clear_canvas(self):
        """
        Delete all of Drawing
        """
        self._canvas.delete(tk.ALL) 

        
    def get_bbox(self,pixel): 
        """
        Get the position of the Left Top, Left Bottom, Right Top, Right Bottom
        Parameters:
        pixel:The mouse location
        """
        
        if pixel.x % self._width == 0 and pixel.y % self._width != 0: #If the x not large than a cell's width
                                                                     #and y is larger,means in the left column
            x = (pixel.x // self._width) - 1
            y = (pixel.y // self._width)
                
        elif pixel.x % self._width != 0 and pixel.y % self._width == 0:#If the y not large than a cell's width
                                                                     #and x is larger,means in the Top row
            x = pixel.x // self._width
            y = (pixel.y // self._width) - 1

        elif pixel.x % self._width == 0 and pixel.y % self._width == 0:#In the left top corner
            x = (pixel.x // self._width) - 1
            y = (pixel.y // self._width) - 1
            if y < 0:
                y += 1

        else: 
            x = pixel.x // self._width
            y = pixel.y // self._width
                
        x1 = x * self._width #x1,y1,x2,y2 is four sides loaction of the cell, then multi the width of cell can get the real position
        y1 = y * self._width
        x2 = (x+1) * self._width
        y2 = (y+1) * self._width

        return(x1,y1,x2,y2)

    def pixel_to_position(self,pixel): 
        
        """
        Change the pixel to the sample location such as E2
        """
        
        if pixel.x % self._width == 0 and pixel.y % self._width != 0: #In the Left column
            x = (pixel.x // self._width) - 1
            y = pixel.y // self._width
                
        elif pixel.x % self._width != 0 and pixel.y % self._width == 0: #In the Top row
            x = (pixel.x // self._width)
            y = (pixel.y // self._width) - 1

        elif pixel.x % self._width == 0 and pixel.y % self._width == 0: #in the Left Top corner
            x = (pixel.x // self._width) - 1
            y = (pixel.y // self._width) - 1
        
        else:
            x = pixel.x // self._width
            y = pixel.y // self._width

        row = ALPHA[y]
        col = x
        self._row = row
        self._col = col
        return row,col                 

    def position_to_pixel(self,position): 
        """
        Use the positon like "E2" return the middle position of each cell, it can be used to show the number of pokemon in the cell.
        """

        position = self.pixel_to_position(position)
        x,y = position
        x_positon = 0
        
        for i in ALPHA: #get the input position's number

            if i != x:

                x_positon += 1
            else:

                break
                
        x = self._board_width/2 * ((x_positon)*2+1) #Change the position like "E" to a real pixel number
        y = self._board_width/2 * ((int(y))*2+1) #Change the position like "2" to a real pixel number
        pixel = (y,x)

        return pixel    


class ImageBoardView(BoardView):
    """
    In task2, the image of the board.
    """

    def __init__(self,master,grid_zize,board_width=600):
        """
        set the master window.
        Parameters:
        grid size: size of grid
        Board width: size of game
        """

        self._master = master
        self._grid_size = grid_zize
        self._board_width = board_width
        self._width = int(board_width/self._grid_size)
   
        unrevealed = Image.open('images/unrevealed.png')
        self._unrevealed = ImageTk.PhotoImage(image=unrevealed)
        
        unrevealed_moved = Image.open('images/unrevealed_moved.png')
        self._unrevealed_moved = ImageTk.PhotoImage(image=unrevealed_moved)

        pokeball = Image.open('images/pokeball.png')
        self._pokeball = ImageTk.PhotoImage(image=pokeball)

        pikachu = Image.open('images/pokemon_sprites/pikachu.png')
        self._pikachu = ImageTk.PhotoImage(image=pikachu)

        charizard = Image.open('images/pokemon_sprites/charizard.png')
        self._charizard = ImageTk.PhotoImage(image=charizard)

        cyndaquil = Image.open('images/pokemon_sprites/cyndaquil.png')
        self._cyndaquil = ImageTk.PhotoImage(image=cyndaquil)

        psyduck = Image.open('images/pokemon_sprites/psyduck.png')
        self._psyduck = ImageTk.PhotoImage(image=psyduck)

        togepi = Image.open('images/pokemon_sprites/togepi.png')
        self._togepi = ImageTk.PhotoImage(image=togepi)

        umbreon = Image.open('images/pokemon_sprites/umbreon.png')
        self._umbreon = ImageTk.PhotoImage(image=umbreon)

        zero_adjacent = Image.open('images/zero_adjacent.png')
        self._zero_adjacent = ImageTk.PhotoImage(image=zero_adjacent)

        one_adjacent = Image.open('images/one_adjacent.png') 
        self._one_adjacent = ImageTk.PhotoImage(image=one_adjacent)
        
        two_adjacent = Image.open('images/two_adjacent.png')
        self._two_adjacent = ImageTk.PhotoImage(image=two_adjacent)

        three_adjacent = Image.open('images/three_adjacent.png')
        self._three_adjacent = ImageTk.PhotoImage(image=three_adjacent)

        four_adjacent = Image.open('images/four_adjacent.png')
        self._four_adjacent = ImageTk.PhotoImage(image=four_adjacent)

        five_adjacent = Image.open('images/five_adjacent.png')
        self._five_adjacent = ImageTk.PhotoImage(image=five_adjacent)

        six_adjacent = Image.open('images/clock.png')
        self._six_adjacent = ImageTk.PhotoImage(image=six_adjacent)

        seven_adjacent = Image.open('images/seven_adjacent.png')
        self._seven_adjacent = ImageTk.PhotoImage(image=seven_adjacent)

        eight_adjacent = Image.open('images/eight_adjacent.png')
        self._eight_adjacent = ImageTk.PhotoImage(image=eight_adjacent)

    def draw_board_2(self,board,bd_position):
        """
        Draw the task2 board.
        Parameters:
        board:game string
        bd_position: At first it is 0, no motion image, when motion it will change to 1, and run below function
        """
        self.clear_canvas()
        position_x = 0
        position_y = 0
    
        for i in range(len(board)): #Same as the draw board in BoardView class

            x1 = position_x * self._width
            y1 = position_y * self._width

            x = x1 + self._width/2
            y = y1 + self._width/2
            
            if board[i] == '~': 
                
                self._canvas.create_image(x,y,image = self._unrevealed) #Use the position to create image

                if position_x < self._grid_size - 1:
                    position_x += 1

                else:
                    position_y += 1
                    position_x = 0
            
            
            elif board[i] == '♥':

                self._canvas.create_image(x,y,image = self._pokeball)

                if position_x < self._grid_size - 1:
                    position_x += 1

                else:
                    position_y += 1
                    position_x = 0

            elif board[i] == '☺': 
                
                image = self.random_pokemon_image()
                self._canvas.create_image(x,y,image = image)

                if position_x < self._grid_size - 1:
                    position_x += 1

                else:
                    position_y += 1
                    position_x = 0

            else:
                
                if int(board[i]) == 0: #If the number of this cell is 0, the above is same
                    self._canvas.create_image(x,y,image = self._zero_adjacent)

                elif int(board[i]) == 1:
                    self._canvas.create_image(x,y,image = self._one_adjacent)

                elif int(board[i]) == 2:
                    self._canvas.create_image(x,y,image = self._two_adjacent)
                
                elif int(board[i]) == 3:
                    self._canvas.create_image(x,y,image = self._three_adjacent)
                
                elif int(board[i]) == 4:
                    self._canvas.create_image(x,y,image = self._four_adjacent)
                
                elif int(board[i]) == 5:
                    self._canvas.create_image(x,y,image = self._five_adjacent)
                
                elif int(board[i]) == 6:
                    self._canvas.create_image(x,y,image = self._six_adjacent)
                
                elif int(board[i]) == 7:
                    self._canvas.create_image(x,y,image = self._seven_adjacent)
                
                elif int(board[i]) == 8:
                    self._canvas.create_image(x,y,image = self._eight_adjacent)

                elif int(board[i]) == 9:
                    self._canvas.create_image(x,y,image = self._night_adjacent)
                
                else:
                    pass

                if position_x < self._grid_size - 1: #If the x is not larger than the outside of the grid, then +1 and draw next one
                    position_x += 1

                else: #If x is > grid, means need a new line.
                    position_y += 1
                    position_x = 0
        


        if bd_position != 0: #If is motion, change the grass image

            x = bd_position[0]
            y = bd_position[1]

            index_x = x/self._width
            index_y = y/self._width
            index = int(index_y*self._grid_size + index_x)
            
            if board[index] == '~':  #Just can change the image when the grid is grass
                x = bd_position[0] + self._width/2
                y = bd_position[1] + self._width/2
                self._canvas.create_image(x,y,image = self._unrevealed_moved)
            
            else:
                pass

        else:
            pass

    def random_pokemon_image(self): 
        """
        Get the random image of pokemon.
        """

        pokemon_type = random.randint(1,6) #Get the random number from 1~6
        if pokemon_type == 1: #If the random number is 1, then use this image, the below function is the same
            return self._charizard

        elif pokemon_type == 2:
            return self._cyndaquil

        elif pokemon_type == 3:
            return self._pikachu
        
        elif pokemon_type == 4:
            return self._psyduck
        
        elif pokemon_type == 5:
            return self._togepi
        
        elif pokemon_type == 6:
            return self._umbreon

        else:
            return self._charizard
        

class BoardModel(): 
    """
    The core of the Game.
    """ 
    
    def __init__(self,grid_size,num_pokemon):
        """
        Parameters:
        master: the window of game
        grid_size:size of grid
        num_pokemon: Number of pokemon
        """
            
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._game = UNEXPOSED * self._grid_size ** 2 #At the first time, the game string

        self._left_number = self._num_pokemon
        self._catch_number = 0

        self._new_position = ''
        self._index = ''

    def display_game(self,game, grid_size):
        """ Print the game (i.e. string) with the given size of the game

        Parameters:
            game (str): The string representation of the game
            grid_size (int): The grid size of the game.
        """

        row_separator = '\n' + WALL_HORIZONTAL * (grid_size + 1) * 4
        
        first_row = f"  {WALL_VERTICAL}"

        for i in range(1, grid_size + 1):
            first_row += f" {i:<2}{WALL_VERTICAL}"

        game_board = first_row + row_separator
        
        for i in range(grid_size):
            row = f"{ALPHA[i]} "

            for j in range(grid_size):
                char = game[self.position_to_index((i, j), grid_size)]
                row += f"{WALL_VERTICAL} {char} "

            game_board += "\n" + row + WALL_VERTICAL
            game_board += row_separator
        
        return game_board
      
    def parse_position(self,action, grid_size): 
        """resolve the action into its corresponding position.

        This function should return None if the action is not the correct format.
        i.e it's not a capital letter followed by a number (e.g. A1).

        Parameters:
            action (str): The string containing the row (Cap) and column.
            grid_size (int): Size of game.

        Returns:
            (tuple<int, int>) : The row, column position of a cell in the game.

            None if the action is invalid.

        """

        row = action[0]
        column = action[1:]
        x = ALPHA.find(row)
        y = int(column)-1

        return x, y

    def position_to_index(self,position, grid_size): 
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """

        x=position[0]
        y=position[1]
        
        return x * grid_size + y
      
    def replace_character_at_index(self,game, index, character): 
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """

        return game[:index] + character + game[index + 1:]

    def flag_cell(self,game,index):
        """Toggle Flag on or off at selected index. If the selected index is already
        revealed, the game would return with no changes.

        Parameters:
            game (str): The game string.
            index (int): The index in the game string where a flag is placed.
        Returns
            (str): The updated game string.
         """
   
        if game[index] == FLAG:
            game = self.replace_character_at_index(game, index, UNEXPOSED)
            self._left_number += 1

        elif game[index] == UNEXPOSED:

            if self._left_number == 0: #if no ball,number didn't change,game string didn't change
                game = game
                self._left_number = 0

            else:
                game = self.replace_character_at_index(game, index, FLAG)
                self._left_number -= 1
        
        else: #If there is a number,cannot flag
            pass

        return game
    
    def index_in_direction(self,index, grid_size, direction): 
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
    
        col = index % grid_size
        row = index // grid_size
        
        if RIGHT in direction:
            col += 1

        elif LEFT in direction:
            col -= 1

        if UP in direction:
            row -= 1

        elif DOWN in direction:
            row += 1

        if not (0 <= col < grid_size and 0 <= row < grid_size):
            return None

        return self.position_to_index((row, col), grid_size)
      
    def neighbour_directions(self,index,grid_size): 
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """

        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, grid_size, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def number_at_cell(self,game,pokemon_locations,grid_size,index): 
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
         
        if game[index] != UNEXPOSED:
            return int(game[index])

        number = 0
        for neighbour in self.neighbour_directions(index, grid_size):
            if neighbour in pokemon_locations:
                number += 1
    
        return number
         
    def reveal_cells(self,game, grid_size, pokemon_locations, index): 
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
    
        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        game = self.replace_character_at_index(game, index, str(number))
        clear = self.big_fun_search(game, grid_size, pokemon_locations, index)
        for i in clear:
            if game[i] != FLAG:
                number = self.number_at_cell(game, pokemon_locations, grid_size, i)
                game = self.replace_character_at_index(game, i, str(number))
       
        return game
      
    def big_fun_search(self,game, grid_size, pokemon_locations, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if game[index] == FLAG:
            return queue

        number = self.number_at_cell(game, pokemon_locations, grid_size, index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, grid_size):
                if neighbour in discovered:
                    continue
    
                discovered.append(neighbour)
                if game[neighbour] != FLAG:
                    number = self.number_at_cell(game, pokemon_locations, grid_size, neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def get_pokemon_locations(self,grid_size, number_of_pokemons): 
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.
            number_of_pokemons (int): The number of pokemons that the game will have.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        
        cell_count = grid_size ** 2
        pokemon_locations = ()

        for _ in range(number_of_pokemons):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count-1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count-1)

            pokemon_locations += (index,)

        return pokemon_locations
      
    def index_to_position(self,index): 
        """
        From the index to return the position.
        """
          
        x = index // self._grid_size
        y = index % self._grid_size
            
        position = (x,y)                
        return position
       
    def get_left_ball(self): 
        """
        Get the left ball of game.
        """

        return self._left_number
    
    def get_left_pokemon(self): 
        """
        Get the number of Flag set in the board
        """
        
        return self._catch_number

    def get_game(self,action,game,pokemon_locations):
        """
        It is the main function.
        Parameters:
        action:Click position
        game:Game string
        pokemon_locations: Location of pokemon
        """
        
        self._game = game
        grid_size = self._grid_size
        new_position = self.parse_position(action, grid_size)
        index = self.position_to_index(new_position, grid_size)
        self._index = index
        self._new_position = new_position


        if index in pokemon_locations:
            if self._game[index] == FLAG:  #If there is a flag, it not fail
                
                self._game = self._game
            
            else:
                for i in pokemon_locations: #show all of pokemon
                    self._game = self.replace_character_at_index(self._game, i, POKEMON)
                
                print("You have scared away all the pokemons.")

        else: 
            if self._game[index] == FLAG: #If there is a flag, it not change
                
                self._game = self._game
            
            else: #Change the ceels
                self._game = self.reveal_cells(self._game, grid_size, pokemon_locations, index)

        return self._game
 
    def get_game_right(self,action,game,pokemon_locations):
        """
        Whenclick right mouse, run this.
        Parameters:
        action:Click position
        game:Game string
        pokemon_locations: Location of pokemon
        """
        
        self._game = game
        grid_size = self._grid_size
        new_position = self.parse_position(action, grid_size)
        index = self.position_to_index(new_position, grid_size)

        self._index = index
        self._new_position = new_position
        self._game = self.flag_cell(self._game, index) #Change the ceel to the flag
        
        return self._game


class StatusBar(tk.Frame):
    """
    The button under the game board.
    """

    def __init__(self,master,*change):
        """
        Set the frame and the button in the bottom of window in task2.
        """

        super().__init__(master)
        full_pokeball = Image.open('images/full_pokeball.png') 
        self._full_pokeball = ImageTk.PhotoImage(image=full_pokeball)
        clock = Image.open('images/clock.png')
        self._clock = ImageTk.PhotoImage(image=clock)

        self._master = master
        self._new = False
        self._restart = False
        self._clicktime = 0

        self._frame1 = tk.Frame(self._master,relief='solid')
        self._ball_label = tk.Label(self._frame1,image=self._full_pokeball)
        self._catch_label = tk.Label(self._frame1, text=" attemped catches"  )
        self._left_label = tk.Label(self._frame1, text=" pokeballs left"  )

        self._frame2 = tk.Frame(self._master,relief='solid')
        self._clock_label = tk.Label(self._frame2,image=self._clock)
        self._time_label = tk.Label(self._frame2, text="Time elapsed" )
        self._playtime_label = tk.Label(self._frame2, text="0m  0s" )

        self._frame3 = tk.Frame(self._master,relief='solid')
        self._new_game = tk.Button(self._frame3, text="New game")
        self._restart_game = tk.Button(self._frame3, text="Restart game")


class PokemonGame(ImageBoardView,BoardView,BoardModel,StatusBar): 
    """
    The main function to run the game.
    """

    def __init__(self,master,grid_size,num_pokemon,task): 
        """
        You can also change grid_size,numPokmon andtask at the bottom of the code
        app=PokemonGame(root) function
        """
        
        self._statusbar = StatusBar(master) #Use this class to show the bottom button
        self._task = task #Get the task input
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._pokemon_locations = ''

        self._new_game = UNEXPOSED * self._grid_size ** 2
        self._pokemon_locations = ''

        self._left_number = self._num_pokemon #The first time of ball number is equal to pokemon number
        super().__init__(master,self._grid_size) #Call the ImageBoard class,then it will call BoardView class， can self._board_width

        if task == TASK_ONE: #Use the task 1 board and setting
            self._task = 1
        elif task == TASK_TWO:#Use the task 2 board and setting
            self._task = 2
        else:
            pass
       
        self._master = master
        self._master.title("Pokemon: Got 2 Find Them All!")
        self._lbl = tk.Label(master, text="Pokemon: Got 2 Find Them All!",font=('Arial','35'),bg='IndianRed3',fg='white',bd=3,relief=tk.RAISED) 
        self._lbl.pack(side=tk.TOP,fill=tk.X)

        if self._task == 1:

            self._task = 1 
            self._canvas = tk.Canvas(self._master,width = self._board_width,height = self._board_width,bg='white')
            self._canvas.pack()
            self.draw_board(self._new_game,0)

        elif self._task == 2:

            self._task = 2 
            self._canvas = tk.Canvas(self._master,width = self._board_width,height = self._board_width,bg='white')
            self._canvas.pack()

            self.draw_board_2(self._new_game,0) 
            self.pack_bottom() #Pack the bottom button

        else:
            pass

 
        self._canvas.bind("<Button-1>",self.click)
        self._canvas.bind("<Button-2>",self.click_right)
        self._canvas.bind("<Button-3>",self.click_right)
        self._canvas.bind('<Motion>', self.evt_motion) #Add the motion outside of the cell

        self._statusbar._new_game.bind("<Button-1>",self.new_game)
        self._statusbar._restart_game.bind("<Button-1>",self.restart_game)

        self._checktime = 0
        self._catch_number = 0 #At fitst, the number of catch is 0
        self.catches()#Then show in the button
        self.ball_left() #Show the first time's ball number

      
        menubar = tk.Menu(self._master) #Set the menubar
        self._master.config(menu=menubar) 

        filemenu1 = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = filemenu1)
        filemenu2 = tk.Menu(menubar)
        menubar.add_cascade(label = "Game", menu = filemenu2)

        filemenu1.add_command(label="Open Game File", command=self.open_file)
        filemenu1.add_command(label="Save Game", command=self.save_file)

        filemenu2.add_command(label="New Game", command=self.new)
        filemenu2.add_command(label="Restart Game", command=self.restart)
        filemenu2.add_command(label="High Scores", command=self.show_high_score)
        filemenu2.add_command(label="Quit", command=self.quitgame)
        self._filename = None
    
        self._seconds = 0
        self._minutes = 0
        self._time_check = 0

        self._win = False #If it change to True, stop timing
        self.play_time() #Show the playing time

        self._write_high_score = 0 #  1:No file。  2: Has file, less than 3people。 3：Has file, equal 3 people
    
        self._name1_first = '' #The three people's name and timein High score menu
        self._name1_last = ''
        self._name2_first = ''
        self._name2_last = ''
        self._name3_first = ''
        self._name3_last = ''
        self._name1_time = ''
        self._name2_time = ''
        self._name3_time = ''

        self.read_highscore() #Get the High score at first
        self._creat_high_score = 0  #When create new score, it will change to 1
        
    def show_high_score(self):
        """
        Set and pack the High score window.
        """

        if self._task == 1: 
            tk.messagebox.showerror('Error','Please change to TASK 2!')

        else:

            self._top_window=tk.Toplevel(bg='white') #Set a new window
            self._top_window.geometry("200x120")
            self._top_window.title("Top 3")

            self._top_frame = tk.Frame(self._top_window) #set the new windows' a frame, put the player score on it
            self._top_frame.pack(side=tk.TOP,pady=5,fill=tk.X)

            self._title = tk.Label(self._top_frame, text="High Scores",bg='IndianRed3',fg='white',bd=3,relief=tk.RAISED)
            self._text1 = tk.Label(self._top_frame, text="",bg='white',fg='black')
            self._text2 = tk.Label(self._top_frame, text="",bg='white',fg='black')
            self._text3 = tk.Label(self._top_frame, text="",bg='white',fg='black')
            self._enterbuttton = tk.Button(self._top_frame,text='Done',command = self.done) 
            
            self._title.pack(side = tk.TOP,fill=tk.X)
            self._text1.pack(side = tk.TOP)
            self._text2.pack(side = tk.TOP)
            self._text3.pack(side = tk.TOP)
            self._enterbuttton.pack(side=tk.TOP)
    def done(self):
        """
        Click, then close the top window.
        """
        self._top_window.destroy()
        

    def input_high_score(self):
        """
        Ask to input the High score window.
        """

        if self._task == 1: 
            tk.messagebox.showerror('Error','Please change to TASK 2!')

        else:

            self._top_window=tk.Toplevel(height=100,width=300,bg='white') #Set a new window
            self._top_window.geometry("270x80")

            self._top_frame = tk.Frame(self._top_window)
            self._top_frame.pack(side=tk.TOP,pady=5,fill=tk.X)
            self._text = tk.Label(self._top_frame, text=f'You win in {self._new_time}! Enter your name:')
            self._entry = tk.Entry(self._top_frame)
            self._enterbuttton = tk.Button(self._top_frame,text='Enter',command=self.create_high_score) 
            
            self._text.pack(side = tk.TOP)
            self._entry.pack(side=tk.TOP)
            self._enterbuttton.pack(side=tk.TOP)
            

    def open_file(self):
        """
        The open file menu
        """
        
        if self._task == 1:
            tk.messagebox.showerror('Error','Please change to TASK 2!')
        else:
            
            filename = filedialog.askopenfilename()

            if filename: #if has a file name
                self._filename = filename
                self._master.title(self._filename)
                fd = open(filename, 'r')
                
                text = fd.read() #Get the text in the open file
                fd.close()

                time = 0
                time2 = 0
                for i in range(1,len(text)):
                    if text[i] != 's':
                        time += 1
                    if text[i] == 's': #Find the position of task
                        break
                for i in range(1,len(text)):
                    if text[i] != 'n':
                        time2 += 1
                    if text[i] == 'n': #Find the number of pokemon
                        break
                
                self._minutes = int(f'{text[0]}{text[1]}') #Get the running time
                self._seconds = int(f'{text[2]}{text[3]}') #Get the running time
                self._checktime = int(text[4]) #Get is it the first time to click game, if yes, creat a new pokemon location
                
                self._new_game = str(text [5:time+1]) #Get the game string of game
                all_pokemon_locations = text[time+5:]  #Get the string of pokemon location + number of pokemon

                new = ''
                new = re.split(r'(\W+)',f'{all_pokemon_locations}') #Splite all pokemon string to pieces
                pokemon_locations = []

                for i in range(len(new)): #Use 're' to spilte the string to pices

                    try: #Try if the string has the location
                        if new[i].isdigit(): #If it is number, not '(' or ')' or alpha

                            pokemon_locations.append(int(new[i])) #then get it
                
                    except:
                        pass

                self._pokemon_locations = tuple(pokemon_locations) #Get the real location of pokemon
                self._catch_number = 0 

                for i in range(len(text)): #Check how many balls in the game

                    if str(text[i]) == FLAG: 

                        self._catch_number+=1  #Get how many ball has left


                for i in range(len(text)):
                    if text[i] == '(': #Means it already has pokemonlocation
                        self._has_location = 1
                    else:
                        self._has_location = 0
                #try: #If it has location, then get the ball left and how many balls in the grid

                    if self._has_location == 1: #If it has location
                        self._left_number = len(self._pokemon_locations)-self._catch_number
                        self.ball_left() 
                        self.catches() 
                    
                #except: #If not have the pokemon location, creat a new the location

                    elif self._has_location == 0: #If it did't has location, need to create
                        self._grid_size = int(round(math.sqrt(len(self._new_game)))) #use math sqrt to get the grid_size
                        num_pokemon = time2+2 #(time2+1 is 'n', then time2+2 is the first number of number )
                        self._num_pokemon = int(text[num_pokemon:])
                        self._pokemon_locations = self.get_pokemon_locations(self._grid_size,self._num_pokemon)

                        self._left_number = self._num_pokemon-self._catch_number
                        self._checktime = 1 #has already create the location of pokemon,then it change to 1
                        self._task = 2
                        self.ball_left() 
                        self.catches() 

                    else:
                        pass
                
                self.draw_board_2(self._new_game,0) #Draw the load file size
                

            else: #If cannot open the file

                tk.messagebox.showerror('Error','Can not find the file,please run program again!')
                self._master.destroy() #Quit the windows

        
    def save_file(self):
        """
        Save the game file
        """

        if self._task == 1:
            tk.messagebox.showerror('Error','Please change to TASK 2!')
        else:
            print('Save correct')

            if self._filename is None: #Ask a filename
                
                filename = filedialog.asksaveasfilename()
                
                if filename: 
                    self._filename = f'{filename}.txt' #Save as txt file
                    
                else: #If not save, keep playing
                    pass

            if self._filename: 
                self._master.title(self._filename)
                fd = open(self._filename, 'w')

                if len(str(self._minutes)) == 1: #If minutes is one digite, then add '0' before it
                    if len(str(self._seconds)) == 1:
                        text = f'0{self._minutes}0{self._seconds}{self._checktime}{self._new_game}s{self._task}b{self._pokemon_locations}n{self._num_pokemon}'
                    else:
                        text = f'0{self._minutes}{self._seconds}{self._checktime}{self._new_game}s{self._task}b{self._pokemon_locations}n{self._num_pokemon}'
                       
                else: #If minute is two digit
                    if len(str(self._seconds)) == 1:
                        text = f'{self._minutes}0{self._seconds}{self._checktime}{self._new_game}s{self._task}b{self._pokemon_locations}n{self._num_pokemon}'
                    else: #Minute and seconds all is two digit
                        text = f'{self._minutes}{self._seconds}{self._checktime}{self._new_game}s{self._task}b{self._pokemon_locations}n{self._num_pokemon}'                        
                fd.write(text)
                fd.close()

        self._name = None
        

    def new(self):
        """
        Get the new game
        """
    
        if self._task == 1:

            self.clear_canvas()
            self._new_game = UNEXPOSED * self._grid_size ** 2
            self.draw_board(self._new_game,0)
            self._checktime = 0
        else:
            self.clear_canvas()
            self._new_game = UNEXPOSED * self._grid_size ** 2
            self.draw_board_2(self._new_game,0)
            self._checktime = 0
            self._time_check = 1 #Clear the timing

            self._left_number = self._num_pokemon #Clear the ball and catching
            self._catch_number = 0
            self.ball_left()
            self.catches()


    def restart(self):
        """
        Restart the game, the location of pokemon will not change
        """
        
        if self._task == 1:
            self.clear_canvas()
            self._new_game = UNEXPOSED * self._grid_size ** 2
            self.draw_board(self._new_game,0)
            self._checktime = 1

        else:
            self.clear_canvas()
            self._new_game = UNEXPOSED * self._grid_size ** 2
            self.draw_board_2(self._new_game,0)
            self._checktime = 1

            self._left_number = self._num_pokemon 
            self._catch_number = 0
            self.ball_left()
            self.catches()
 

    def quitgame(self):
        """
        Ask people if they want to quit.
        """
        
        ans = tk.messagebox.askokcancel('Warning!','Do you want to quit?')
                
        if ans is False:
            pass
        
        elif ans is True:
            self._master.destroy() #Quit the windows
        
        else:
            pass
           
    def pack_bottom(self):
        """
        Pack the buttom botton
        """
        
        #Left sides
        self._statusbar._frame1.pack(side=tk.LEFT,padx=35)
        self._statusbar._ball_label.pack(side=tk.LEFT)
        self._statusbar._catch_label.pack(side=tk.TOP,anchor='w',pady=1)
        self._statusbar._left_label.pack(side=tk.TOP,anchor='w')
        #Middle
        self._statusbar._frame2.pack(side=tk.LEFT,padx=10)
        self._statusbar._clock_label.pack(side=tk.LEFT)
        self._statusbar._time_label.pack(side=tk.TOP,pady=0.5)
        self._statusbar._playtime_label.pack(side=tk.TOP )
        #Right
        self._statusbar._frame3.pack(side=tk.LEFT,padx=35)
        self._statusbar._new_game.pack(side=tk.TOP)
        self._statusbar._restart_game.pack(side=tk.BOTTOM)
    
    def new_game(self,event):
        """
        Same as the new function
        """
        self.clear_canvas()
        self._new_game = UNEXPOSED * self._grid_size ** 2
        self.draw_board_2(self._new_game,0)
        self._checktime = 0
        self._time_check = 1  

        self._left_number = self._num_pokemon 
        self._catch_number = 0
        self.ball_left()
        self.catches()

    def restart_game(self,event):
        """
        Same as the restart function
        """
        self.clear_canvas()
        self._new_game = UNEXPOSED * self._grid_size ** 2
        self.draw_board_2(self._new_game,0)
        self._checktime = 1

        self._left_number = self._num_pokemon 
        self._catch_number = 0
        self.ball_left()
        self.catches()
        
    def click(self,event):
        """
        Click the left mouse
        """
        self.clear_canvas()
        point = event.x, event.y
        
        print(f'Left click position is {point}')
        click_position = self.pixel_to_position(event) #Get Like "A4"

        x=click_position[0]
        y=click_position[1]
        position = f'{x}{y+1}'

        if self._task == 1: #Test Task1

            if event.x > self._board_width or event.y > self._board_width: #If click out side of grid
                print('Outside of grid')
                self.draw_board(self._new_game,0)

            else: #If didn't click outside
                
                if self._checktime ==0: #The first time to click game board

                    pokemon_locations = self.get_pokemon_locations(self._grid_size,self._num_pokemon)
                    new_game = self.get_game(position,self._new_game,pokemon_locations) 

                    if POKEMON in new_game:
                
                        self._new_game = new_game
                        self.draw_board(self._new_game,0)
                        self._master.update() 
                        tk.messagebox.showerror('Error','You Lose!')
                        self._master.destroy() #Quit the windows
         
                    else: #Draw the new board
                        self._new_game = str(new_game)
                        self._pokemon_locations = pokemon_locations
                        self.draw_board(self._new_game,0)
                        self._checktime += 1

                        self.check_loss(self._task)

                elif self._checktime == 1: #The second time to click game board
                    
                    new_game = self.get_game(position,self._new_game,self._pokemon_locations)
                    
                    if POKEMON in new_game:
                        self.draw_board(new_game,0)
                        self._master.update() 

                        tk.messagebox.showerror('Error','You Lose!')
                        self._master.destroy() 

                    else:
                        self._new_game = new_game
                        self.draw_board(self._new_game,0)
                        self.check_loss(self._task)

                else: 

                    pass

                   
        if self._task == 2:            

            if event.x > self._board_width or event.y > self._board_width: #Click out of grid
                print('Outside of grid')
                self.draw_board_2(self._new_game,0)

            else: #Playing in the grid
                
                if self._checktime ==0: #The first time to click game board
                    pokemon_locations = self.get_pokemon_locations(self._grid_size,self._num_pokemon)
                    self._pokemon_locations = pokemon_locations
                    
                    new_game = self.get_game(position,self._new_game,pokemon_locations) 

                    if POKEMON in new_game: #Click on a pokemon , lose
                        
                        self._new_game = new_game
                        self.draw_board_2(self._new_game,0)
                        self._master.update() 
                        ans = tk.messagebox.askokcancel('Game Over','You lose! Would you like to play again?')
                        
                        if ans is True:
                            
                            self.clear_canvas()
                            self._catch_number = 0 
                            self._left_number = self._num_pokemon 
                            self.ball_left()
                            self.catches()

                            self._new_game = UNEXPOSED * self._grid_size ** 2
                            self.draw_board_2(self._new_game,0)
                            self._checktime = 0 #Change to the first time click
                            self._time_check = 1 #Change the time to 0
                
                        
                        if ans is False:
                            self._master.destroy()                      
                        
                    else: #Not pokemon, draw board
                        self._new_game = str(new_game)
                        self._pokemon_locations = pokemon_locations
                        self.draw_board_2(self._new_game,0)
                        self._checktime += 1
                        self.check_loss(self._task)

                elif self._checktime == 1: #The second time to click game board
                    new_game = self.get_game(position,self._new_game,self._pokemon_locations)
                    
                    if POKEMON in new_game: #Same as above

                        self.draw_board_2(new_game,0)
                        self._master.update() 
                        ans = tk.messagebox.askokcancel('Game Over','You lose! Would you like to play again?')
                        
                        if ans is True:
                            
                            self.clear_canvas()
                            self._catch_number = 0 
                            self._left_number = self._num_pokemon
                            self.ball_left()
                            self.catches()

                            self._new_game = UNEXPOSED * self._grid_size ** 2
                            self.draw_board_2(self._new_game,0)
                            self._checktime = 0
                            self._time_check = 1
                
                        
                        if ans is False:

                            self._master.destroy() 

                    else: #If the click position is not pokemon, then update the board
                        self._new_game = new_game
                        self.draw_board_2(self._new_game,0)
                        self.check_loss(self._task)

                else: 
                    pass
        
            

    def click_right(self,event):
        """
        Click the right mouse
        """
        self.clear_canvas()     
        click_position = self.pixel_to_position(event)
        x=click_position[0]
        y=click_position[1]
        position = f'{x}{y+1}'
        print(f'Right click position is {position}')
        
        game = self._new_game
        
        if self._task == 1:

            if event.x > self._board_width or event.y > self._board_width: #Outside of grid
                print('Outside of grid')
                self.draw_board(self._new_game,0)

            else:
                
                if self._checktime == 1 or self._checktime == 0:

                    self._new_game = self.get_game_right(position,game,self._pokemon_locations) 
                    self.draw_board(self._new_game,0)

                    self.ball_left()
                    self.catches()
                    self.check_loss(self._task)
                else:
                    pass
        
        elif self._task == 2:

            if event.x > self._board_width or event.y > self._board_width:  #Same as above
                print('Outside of grid')
                self.draw_board_2(self._new_game,0)
            
            else: #playing in the grid

                if self._checktime == 1 or self._checktime == 0:

                    self._new_game = self.get_game_right(position,game,self._pokemon_locations) 
                    self.draw_board_2(self._new_game,0)

                    self.ball_left()
                    self.catches()
                    self.check_loss(self._task)
                
                else:
                    pass

        else:
            pass
    
        
    def evt_motion(self,event):
        """
        Set the motion of the mouse
        """
        motion = self.get_bbox(event) #The position of the motion cell
        
        if self._task == 1:

            if event.x > self._board_width or event.y > self._board_width: 
                print('Outside of grid')
                self.draw_board(self._new_game,0)

            else:
                self.draw_board(self._new_game,motion)
        
        else: 

            if event.x > self._board_width or event.y > self._board_width: 
                print('Outside of grid')
                self.draw_board_2(self._new_game,0)

            else:
                self.draw_board_2(self._new_game,motion)
    

    def ball_left(self):
        """
        Get the left ball
        """

        BoardModel(self._grid_size,self._num_pokemon).get_left_ball()

        new_text=f'{self._left_number}   pokeballs left'
        self._statusbar._left_label.config(text=new_text)

        if self._left_number == 0: #If no ball, change the image to empty

            empty_pokeball = Image.open('images/empty_pokeball.png')
            self._empty_pokeball = ImageTk.PhotoImage(image=empty_pokeball)

            self._statusbar._ball_label.config(image = self._empty_pokeball)
        
        else:
            
            full_pokeball = Image.open('images/full_pokeball.png')
            self._full_pokeball = ImageTk.PhotoImage(image=full_pokeball)

            self._statusbar._ball_label.config(image = self._full_pokeball)
        
        return self._left_number


    def catches(self): 
        """
        Get the number of set ball
        """
    
        BoardModel(self._grid_size,self._num_pokemon).get_left_pokemon() #Get the left pokemon ball
        self._catch_number = self._num_pokemon - self._left_number
        new_text=f'{self._catch_number}   attemped catches'
        self._statusbar._catch_label.config(text=new_text)
        return self._catch_number

    def play_time(self): 
        """
        Get the playing time.
        """

        if self._time_check == 1:
            self._seconds = 0
            self._minutes = 0
            self._time_check = 0
        else:
            pass

        self._seconds += 1
        if self._seconds == 60: #If 60 seconds, then change to 1 minute
            self._minutes += 1
            self._seconds = 0
        else:
            pass
        self._new_time = f'{self._minutes}m {self._seconds}s'


        if self._win is False: #If not win, still counting

            self._statusbar._playtime_label.config(text=self._new_time)
            self._master.after(1000,self.play_time)

        elif self._win is True: #If win the game, stop timeing
            self._statusbar._playtime_label.config(text=self._new_time)
    
        else:
            pass
    
    def check_win(self,game, pokemon_locations):
        """
        Check is there winning in the game
        """
    
        return UNEXPOSED not in game and game.count(FLAG) == len(pokemon_locations)
    
    def check_loss(self,task):
        """
        Show the message box when win the game
        """
        
        if task == 1:
            if self.check_win(self._new_game,self._pokemon_locations):

                self._master.update() 
                tk.messagebox.showerror('','You Win!')
                self._master.destroy() 
            else:
                pass

        elif task == 2:

            if self.check_win(self._new_game,self._pokemon_locations):
                self._master.update() 
                self._win = True #Stop timing

                ans = tk.messagebox.askokcancel('You win!','Good job! Would you like to play again?')
                
                if ans is True: #If choose start new game
                    
                    self.clear_canvas()
                    self._catch_number = 0 
                    self._left_number = self._num_pokemon 
                    self.ball_left()
                    self.catches()

                    self._new_game = UNEXPOSED * self._grid_size ** 2
                    self.draw_board_2(self._new_game,0)
                    self._checktime = 0
                    self._time_check = 1 
        
                elif ans is False:

                    self._master.destroy() #Quit the windows
            else:
                pass
        else:
            pass
        
    def create_high_score(self): 
        """
        When the game stop,create high score file.
        """
        
        if self._task == 1:
            tk.messagebox.showerror('Error','Please change to TASK 2!')

        else:

            if self._write_high_score == 1:

                self.high_score()

                self._name = self._entry.get()

                self._high_name = "HighScoreData.txt" #Set a file with this name
                self._master.title(self._high_name)

                fd = open(self._high_name, 'w')
                time = self._new_time 
                newtime = ''

                for i in range(len(time)):
                    if time[i] == 'm':
                        newtime_min = time[:i] #Get the minute

                        if len(time[i:]) == 5: #  if is two digits secods " 12s"
                            newtime_sec = f'{time[i+2]}{time[i+3]}'

                        elif len(time[i:]) == 4: #  ' 9s'
                            newtime_sec = f'{time[i+2]}'

                text = f'({self._name}*{newtime_min}m{newtime_sec})' 
                self._creat_high_score = 1 #Create window to get name, if 0, not new score
                fd.write(text)
                fd.close()

                self._master.destroy() 
            
            elif self._write_high_score == 2:# Has the file and less than 3 peop;e

                self.high_score() 
                self._name = self._entry.get()
                self._high_name = "HighScoreData.txt" 
                self._master.title(self._high_name)
                fd = open(self._high_name, 'w')

                time = self._new_time 
                newtime = ''
                for i in range(len(time)):
                    if time[i] == 'm':
                        newtime_min = time[:i] 

                        if len(time[i:]) == 5: #  " 12s"
                            newtime_sec = f'{time[i+2]}{time[i+3]}'

                        elif len(time[i:]) == 4: #  ' 9s'
                            newtime_sec = f'{time[i+2]}'
                
                #1.If just one people in the file
                if self._name2_first == '': #If not has second people 
                    if self._name1_last != '': #If first people is two names
                        
                        text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self._name[0]}{self._name[2]}*{newtime_min}m{newtime_sec})' #(aaa0m21)
                        
        
                    else:#If first people just one name 

                        text = f'({self._name1_first}*{self._name1_time[0]}m{self._name1_time[2]})({self._name[0]}{self._name[2]}*{newtime_min}m{newtime_sec})' #(aaa0m21)
                                            
                
                elif self._name2_first != '': #2. If already two people
                    
                    if self._name1_last != '': 
                        
                        if self._name2_last != '':
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self.__name2_first}{self.__name2_last}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'

                        else:
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self.__name2_first}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'

                    else:#If first people have only one name

                        if self._name2_last != '':
                            text = f'({self._name1_first}*{self._name1_time[0]}m{self._name1_time[2]})({self.__name2_first}{self.__name2_last}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'

                        else:
                            text = f'({self._name1_first}*{self._name1_time[0]}m{self._name1_time[2]})({self.__name2_first}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'
                else:
                    pass
                self._creat_high_score = 1 
                fd.write(text)
                fd.close()
                self._master.destroy() 

            elif self._write_high_score == 3:#  3：Has file , 3 people in it

                self._name = self._entry.get()
                self._high_name = "HighScoreData.txt" 
                self._master.title(self._high_name)
                fd = open(self._high_name, 'w')

                time = self._new_time 
                newtime = ''
                for i in range(len(time)):
                    if time[i] == 'm':
                        newtime_min = time[:i] 

                        if len(time[i:]) == 5: 
                            newtime_sec = f'{time[i+2]}{time[i+3]}'

                        elif len(time[i:]) == 4: 
                            newtime_sec = f'{time[i+2]}'
                
                time1 = self._name1_time[0]*60 + self._name1_time[2]
                time2 = self._name2_time[0]*60 + self._name2_time[2]
                time3 = self._name3_time[0]*60 + self._name3_time[2]
                time4 = self._new_time[0]*60 + self._new_time[2] #This game's time

                time_sort = [time1,time2,time3]
                time_sort = time_sort.sort() #Make in order, the last is the slowest

                if time_sort[2] == time1 and time1>time4: #If time is slow
                    self.high_score() 
                    if self._name2_last != '': 

                        if self._name3_last != '': #Same as above
                            text = f'({self._name}*{newtime_min}m{newtime_sec})({self._name2_first}{self._name2_last}*{self._name2_time[0]}m{self._name2_time[2]})({self._name3_first}{self._name3_last}*{self._name3_time[0]}m{self._name3_time[2]})'
                        
                        else:
                            text = f'({self._name}*{newtime_min}m{newtime_sec})({self._name2_first}{self._name2_last}*{self._name2_time[0]}m{self._name2_time[2]})({self._name3_first}*{self._name3_time[0]}m{self._name3_time[2]})'

                    else: 

                        if self._name3_last != '': 
                            text = f'({self._name}*{newtime_min}m{newtime_sec})({self._name2_first}*{self._name2_time[0]}m{self._name2_time[2]})({self._name3_first}{self._name3_last}*{self._name3_time[0]}m{self._name3_time[2]})'
                        
                        else:
                            text = f'({self._name}*{newtime_min}m{newtime_sec})({self._name2_first}*{self._name2_time[0]}m{self._name2_time[2]})({self._name3_first}*{self._name3_time[0]}m{self._name3_time[2]})'
                    
                    self._creat_high_score = 1 
                    fd.write(text)
                    fd.close()
                    self._master.destroy() 

                elif time_sort[2] == time2 and time2>time4: #Same as above

                    self.high_score() 

                    if self._name1_last != '': 

                        if self._name3_last != '': 
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self._name}*{newtime_min}m{newtime_sec})({self._name3_first}{self._name3_last}*{self._name3_time[0]}m{self._name3_time[2]})'
                        
                        else:
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self._name}*{newtime_min}m{newtime_sec})({self._name3_first}*{self._name3_time[0]}m{self._name3_time[2]})'
                        
                    else: 

                        if self._name3_last != '': 
                            text = f'({self._name1_first}*{self._name1_time[0]}m{self._name1_time[2]})({self._name}*{newtime_min}m{newtime_sec})({self._name3_first}{self._name3_last}*{self._name3_time[0]}m{self._name3_time[2]})'
                        
                        
                        else:
                           text = f'({self._name1_first}*{self._name1_time[0]}m{self._name1_time[2]})({self._name}*{newtime_min}m{newtime_sec})({self._name3_first}*{self._name3_time[0]}m{self._name3_time[2]})'
                    
                    self._creat_high_score = 1 
                    fd.write(text)
                    fd.close()
                    self._master.destroy() 

                elif time_sort[2] == time3 and time3>time4: #Same as above
                    self.high_score() 

                    if self._name1_last != '': 

                        if self._name2_last != '': 
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self._name2_first}{self._name2_last}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'
                        

                        else:
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self._name2_first}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'
                           
                    else: 

                        if self._name2_last != '': 
                            text = f'({self._name1_first}*{self._name1_time[0]}m{self._name1_time[2]})({self._name2_first}{self._name2_last}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'
                           
                        else:
                            text = f'({self._name1_first}{self._name1_last}*{self._name1_time[0]}m{self._name1_time[2]})({self._name2_first}*{self._name2_time[0]}m{self._name2_time[2]})({self._name}*{newtime_min}m{newtime_sec})'
                    
                    self._creat_high_score = 1 
                    fd.write(text)
                    fd.close()
                    self._master.destroy() 

            else:
                pass


    def read_highscore(self): 
        """
        Read the high score file
        """

        score_name = "HighScoreData.txt"

        try: #If has the file, read it
            fd = open(score_name, 'r')
            text = fd.read()
            fd.close()

            new = ''
            new = re.split(r'(\W+)',f'{text}')

            count = 0
            for i in range(len(new)): #Check is there 3 people in file
                if new[i] == "*":
                    count += 1
            
            if count == 3: #If 3 people ,need compare
                self._write_high_score = 3  
                if name[4] != '*': #First people has two name "Vincent Jack"
                    self._name1_first = name[2]
                    self._name1_last = name[4]
                    self._name1_time = name[6]

                    
                    if name[10] != '*': #Second is either two name
                        self._name2_first = name[8] 
                        self._name2_last = name[10]
                        self._name2_time = name[12]

                        if name[16] != '*': #The third is two name
                            self._name3_first = name[14] 
                            self._name3_last = name[16]
                            self._name3_time = name[18]

                        else:
                            self._name3_first = name[14] 
                            self._name3_time = name[16]

                    else:#The second only have one name "Jack"
                        self._name2_first = name[8]
                        self._name2_time = name[10] 

                        if name[14] != '*': 
                            self._name3_first = name[12] 
                            self._name3_last = name[14]
                            self._name3_time = name[16]

                        else:
                            self._name3_first = name[12]
                            self._name3_time = name[14]


                else:#The first only have one name "Jack"

                    self._name1_first = name[2] 

                    if name[6] != '*':
                        self._name2_first = name[4] 
                        self._name2_last = name[6]

                        if name[12] != '*': 
                            self._name3_first = name[10] 
                            self._name3_last = name[12]

                        else:
                            self._name3_first = name[10]

                    else:
                        self._name2_first = name[8]

                        if name[12] != '*': 
                            self._name3_first = name[10] 
                            self._name3_last = name[12]

                        else:
                            self._name3_first = name[10] 

            elif count ==1 or count ==2: #Less than 3 people, write in file directly
                self._write_high_score = 2

                if name[4] != '*': 
                    self._name1_first = name[2]
                    self._name1_last = name[4]
                    self._name1_time = name[6]

                    try: #Try is there the second people?

                        if name[10] != '*': #Same as above
                            self._name2_first = name[8] 
                            self._name2_last = name[10]
                            self._name2_time = name[12]

                        else:
                            self._name2_first = name[8] 
                            self._name2_time = name[10]

                    except: 
                        pass

                else: #The first people only have one name
                    self._name1_first = name[2] 
                    self._name1_time = name[4]

                    try: #Try is there second people?
                        if name[10] != '*': #The second is two name
                            self._name2_first = name[8] 
                            self._name2_last = name[10]
                            self._name2_time = name[10]

                        else:#The second is one name
                            self._name2_first = name[8] 
                            self._name2_time = name[8]

                    except: #No second people
                        pass
        
        except:#No High score file
            pass    

                    




def main():
    """
    You can change Grid_size and Num_poke and Task One/Two at here
    """

    root = tk.Tk()

    #PokemonGame(root,10,15,TASK_ONE)
    PokemonGame(root,10,15,TASK_TWO)
    #PokemonGame(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
    