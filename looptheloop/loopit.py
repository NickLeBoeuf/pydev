#!/usr/bin/env python

import random 

################## Grid Class #######################
class Grid:
    '''The Grid Class, containing user and cpu info '''
    
    def __init__(self,width, height):
        '''Initialize a Grid of widthXheight'''
        self.height = height
        self.width  = width
        self.size   = height*width
        self.makeitempty()
    
    def makeitempty(self):
        '''Fill the Grid with empty stuff everywhere'''
        self.rows = [['-' for x in range(self.width)] for x in range(self.height+1)]
        self.cols = [['|' for x in range(self.height)] for x in range(self.width+1)]
        self.cells = [[' ' for x in range(self.height)] for x in range(self.width)]
        self.corners = [['.' for x in range(self.width+1)] for x in range(self.height+1)]

    def __str__(self):
        ''' Method to print the contents of the class'''
        returnstring = self.__class__.__name__+':\n'
        returnstring = returnstring +'Size: {0}x{1} = {2} cells'.format(self.width,self.height,self.size)
        returnstring = returnstring + \
        '\nRows: {0}'.format(self.rows) + \
        '\nCols: {0}'.format(self.cols)+ \
        '\nCells: {0}'.format(self.cells)
        return returnstring
        
    def display(self):
        '''Display the Grid contents using Text '''
        for r in range(0,self.height):
            line1 = ''
            line2 = ''
            for c in range(0, self.width):
                line1 = line1+' '+format(self.rows[r][c])
            for c in range(0, self.width):
                line2 = line2+format(self.cols[c][r])+format(self.cells[c][r])
            line2 = line2+format(self.cols[self.width][r])
            printd(line1+'\n'+line2)
        # Final Line
        fline = ''
        for c in range(0, self.width):
            fline = fline+' '+format(self.rows[self.height][c])
        printd(fline+'\n')    

    def generateloop(self, minlength):
        '''Generate a Loop in the Grid of a given minimum length'''
        start = (random.randint(0,self.width),random.randint(0,self.height))
        start = (1,1)
        self.length = 0 # This is the current length of the loop
        print 'Generating a {0}-length loop starting at '.format(minlength)+format(start)
        print self.build('r',start[0],start[1],minlength)
        print 'Length is {0:2d}'.format(self.length)


    ## TODO: If needed, implement a counter/watchdog that will interrupt the trial after a given recurrence number.
    ## If the loop is started like a snail, the algorithm will search for a very long time before coming back to the start.
    
    def build(self, direction, stx,sty, minlength):
        ''' Method that is called recursively to build the loop \
        parameters are the direction, the location of the start point stx,sty \
        and the awaited minimum length of the final loop\
        return is DONE, CANT'''
        printd('build: Length is {0:2d}'.format(self.length))
        printd("build({0},{1},{2},{3})".format(direction, stx,sty, minlength))
        
        ## Determine the cell coords where to go (and stop method if we are out of the boundaries)
        scoord = (stx, sty)
        ecoord = self.gotocoord(stx,sty,direction)
        printd("gotocoord({0},{1},{2})={3},{4}".format(stx,sty,direction, ecoord[0],ecoord[1]))
        if ecoord == (-1,-1) :
            return 'CANT'
            
        ## Test if we can draw to the chosen direction (ie.there could be already some loop present)
        drawtest=self.drawto(ecoord[0],ecoord[1],direction)
        printd("drawto({0},{1},{2})={3}".format(ecoord[0],ecoord[1],direction,drawtest))
        if drawtest == 'OK' :
            # We can draw (and it is not the end of the loop), so fill the grid and continue to build
            self.fillgrid(scoord[0],scoord[1],ecoord[0],ecoord[1])
            self.length+=1
            printd('Length is {0:2d}'.format(self.length))
            # Using a table with 4 elements that will be emptied progressively 
            # to memorize the directions that have been explored
            dirtable = ['u','d','l','r']
            # Remove firstly the direction in dirtable where we come from. This will optimize the search.
            dirtable.pop(self.in_integer(self.oppositedir(direction)))

            buildloop = 1 # Let's build a loop
            while buildloop:
                # choose a direction to try 
                chosen_direction = self.choose_direction(dirtable, ecoord[0], ecoord[1], scoord[0], scoord[1], 'random')
                # Remove it from the allowed possibilities before testing it.
                drawdir = dirtable.pop(chosen_direction) 
                # Build in that direction, using this build method recursively.
                buildtest=self.build(drawdir,ecoord[0],ecoord[1],minlength)
                # Test the return value - If it's done, the loop is looped !
                if buildtest == 'DONE':
                    return 'DONE'
                # if not, that mean CANT, try another direction
                if len(dirtable) == 0 :  # and stop if the 4 directions have been tried
                    buildloop = 0   # Exit the while loop
                # end while buildloop

            # if we arrive here, that means that all 4 directions have failed
            # so the segment we have just filled must be erased.
            self.length -= 1           
            printd('Length is {0:2d}'.format(self.length))
            self.unfillgrid(scoord[0],scoord[1],ecoord[0],ecoord[1])
            return 'CANT'
        elif drawtest == 'CANT':
            return 'CANT'
        elif drawtest == 'STOP':
            # The loop is looped !
            if self.length < minlength: # The line that looped is not long enough
                print "Too Short"
                return 'CANT' 
            else:           # We are done. Draw the line and Finish all methods
                self.fillgrid(scoord[0],scoord[1],ecoord[0],ecoord[1])
                self.length+=1    
                print 'Length is {0:2d}'.format(self.length)
                return 'DONE'
                
    def choose_direction(self, dirtable, x, y, comefromx, comefromy, algo):
       ''' This method returns a direction (using an offset in dirtable input) using an \
       chosen algorithm, that can be pure random, or smarter, using some weighting for ex.\
       Inputs are the position to draw from, the previous position of the line, and the table\
       containing the available allowed directions. Last parameter is the algorithm used.'''
       # First algo is pure random
       if algo == 'random':
           return (random.randint(0,len(dirtable)-1)) 
       # Default algo is weighting one
       else:
           return (random.randint(0,len(dirtable)-1)) 

       
       
       
                
    def fillgrid(self,sx,sy,ex,ey):
        ''' This method fills one element of rows[][] or cols[][] \
        inputs are 2 corners: start(x,y) and end(x,y). A line is drawn between \
        the two corners. The two corners must be adjacent.'''
        printd("fillgrid {0} {1} {2} {3}".format(sx,sy,ex,ey))
        if sx == ex :   # Fill a Cols
            if sy > ey :
                self.cols[sx][ey]='#'
            else:
                self.cols[sx][sy]='#'
        elif sy==ey :    # Fill a Rows
            if sx > ex :
                self.rows[sy][ex]='#'
            else:
                self.rows[sy][sx]='#'
        else:
            print "Error in fillgrid method - bad arguments."
        self.display()
                              
    def unfillgrid(self,sx,sy,ex,ey):
        ''' This method deletes one element of rows[][] or cols[][] \
        inputs are 2 corners: start(x,y) and end(x,y). The grid is filled with empty value. \
        The two corners must be adjacent.'''
        printd("unfillgrid {0} {1} {2} {3}".format(sx,sy,ex,ey))
        if sx == ex :   # Fill a Cols
            if sy > ey :
                self.cols[sx][ey]='|'
            else:
                self.cols[sx][sy]='|'
        elif sy==ey :    # Fill a Rows
            if sx > ex :
                self.rows[sy][ex]='-'
            else:
                self.rows[sy][sx]='-'
        else:
            print "Error in unfillgrid method - bad arguments."
        self.display()
                                    
                
    def drawto(self, x , y, fromdir)   : 
        '''Method to test if drawing to x,y (in a line in fromdir direction)\
        will end up in a OK, CANT or STOP status'''
        #printd("drawto({0},{1},{2})".format(x,y,fromdir))
        # test first if we dont try to draw to an existing line
        if (x>0):
            if (self.rows[y][x-1] == '#') and fromdir == 'r':
                return 'CANT'
        if (x < self.width):
            if (self.rows[y][x] == "#") and fromdir == 'l':
                return 'CANT'
        if (y>0):
            if (self.cols[x][y-1] == '#') and fromdir == 'd':
                return 'CANT'
        if (y < self.height):
            if (self.cols[x][y] == '#') and fromdir == 'u':
                return 'CANT'
                          
        # if not, test if it is possible to draw:
        # end point should only be surrounded by 1 line at most
        surroundlines = 0
        # check the surrounding lines in 4 directions
        if (x>0) and (fromdir != 'r') :
            if self.rows[y][x-1] == '#' :
                surroundlines += 1
        if (x < self.width) and (fromdir != 'l') :
            if self.rows[y][x] == "#":
                surroundlines += 1
        if (y > 0) and (fromdir != 'd'):
            if self.cols[x][y-1] == "#":
                surroundlines += 1
        if (y < self.height) and (fromdir != 'u'):
            if self.cols[x][y] == "#":
                surroundlines += 1
        
        # Verify how many surrounding lines have been counted.
        if surroundlines == 0:
            return 'OK'
        elif surroundlines == 1:
            return 'STOP'
        elif surroundlines == 2:
            return 'CANT'
        else:
            print "Error: drawto zarbi"
       
            
               
 
    def gotocoord(self,x,y,direction):
        '''Method to indicate the next coords, \
        starting on a couple of coords and going to a direction\
        output is a pair of coords'''
        if (direction == 'u') and (y>0):
            y = y -1
        elif (direction == 'r') and (x<self.width):
            x = x + 1
        elif (direction == 'd') and (y<self.height):
            y = y + 1
        elif (direction == 'l') and (x>0):
            x = x - 1    
        else:
            return(-1,-1)
        return(x,y)

    def oppositedir(self, direction) :
        ''' Method to give the opposite direction of the input direction '''
        if (direction == 'u') :
            return 'd'
        if (direction == 'd') :
            return 'u'
        if (direction == 'l') :
            return 'r'
        if (direction == 'r') :
            return 'l'                       
        print "Error: malformed input direction".format(direction)

    def in_integer(self, direction):
        ''' Method to convert a string direction into integer value '''
         # dirtable = ['u','d','l','r'] => 0,1,2,3
        if (direction == 'u') :
            return 0
        if (direction == 'd') :
            return 1
        if (direction == 'l') :
            return 2
        if (direction == 'r') :
            return 3                       
        print "Error: malformed input direction".format(direction)



    def fillcellswithnumbers(self):
        '''Method to fill all cells with NUMBERS according to the loop in place\
        To be used on a grid where the loop is present and complete.'''
        for y in range(self.height):
            for x in range(self.width):
                self.cells[x][y]=0 
                if self.rows[y][x]=='#':
                   self.cells[x][y]+=1 
                if self.rows[y+1][x]=='#':
                   self.cells[x][y]+=1 
                if self.cols[x][y]=='#':
                   self.cells[x][y]+=1 
                if self.cols[x+1][y]=='#':
                   self.cells[x][y]+=1 


## 
class Direction:
    ''' Basic class to define directions'''
    def __init__(self,direction):
        self.dir=direction

    def next(self):
        if (self.dir=='u') :
            self.dir = 'r'
        elif self.dir == 'r':
            self.dir = 'd'
        elif self.dir == 'd':
            self.dir = 'l'
        elif self.dir == 'l':
            self.dir = 'u'
        else:
            print('Error in dir definition'.format(self))

      
def printd(string):
    ''' Main printd Method - Print only if Debug parameter is ON'''
    if debugON == 1 :
        print string
        


#######################################################


debugON = 1

random.seed(3)

gr = Grid(6,4)
gr = Grid(5,5)
gr = Grid(4,2)
#gr = Grid(5,5)


#gr.rows[0][0]='-'
#gr.rows[0][1]='-'
#gr.rows[0][2]='-'
#gr.rows[2][3]='-'
#
#gr.cells[3][1]=2

#print(gr)

print "#######################################################"
gr.display()
gr.generateloop(8)
gr.display()

gr.fillcellswithnumbers()
gr.display()

