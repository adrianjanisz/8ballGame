import phylib;
import os;
import sqlite3;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;

HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;

DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;

MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

FRAME_INTERVAL = 0.01;

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg(self):
        # Simplified variables for formatting 
        x = self.obj.still_ball.pos.x
        y = self.obj.still_ball.pos.y
        radius = BALL_RADIUS
        ball_number = self.obj.still_ball.number
        ball_color = BALL_COLOURS[ball_number]
        
        # Full colored circle as the base
        ball_svg = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (x, y, radius, ball_color)

        # Only balls 9 to 15 (inclusive)
        if 9 <= ball_number <= 15:
            # Clip paths 
            clipPathTop = 'top-clip-%d' % ball_number
            clipPathBottom = 'bottom-clip-%d' % ball_number

            # Format top third of ball 
            ball_svg += '<clipPath id="%s">\n' % clipPathTop
            ball_svg += '  <rect x="%d" y="%d" width="%d" height="%d" />\n' % (x - radius, y - radius, radius * 2, radius * (2/3))
            ball_svg += '</clipPath>\n'

            # Format bottom third of ball 
            ball_svg += '<clipPath id="%s">\n' % clipPathBottom
            ball_svg += '  <rect x="%d" y="%d" width="%d" height="%d" />\n' % (x - radius, y + (radius / 3), radius * 2, radius * (2/3))
            ball_svg += '</clipPath>\n'

            # # Apply clip paths to the ball 
            ball_svg += '<circle cx="%d" cy="%d" r="%d" fill="white" clip-path="url(#%s)" />\n' % (x, y, radius, clipPathTop)
            ball_svg += '<circle cx="%d" cy="%d" r="%d" fill="white" clip-path="url(#%s)" />\n' % (x, y, radius, clipPathBottom)
        
        return ball_svg

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity and acceleration as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg(self):
        # Simplified variables for formatting 
        x = self.obj.still_ball.pos.x
        y = self.obj.still_ball.pos.y
        radius = BALL_RADIUS
        ball_number = self.obj.still_ball.number
        ball_color = BALL_COLOURS[ball_number]
        
        # Full colored circle as the base
        ball_svg = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (x, y, radius, ball_color)

        # Only balls 9 to 15 (inclusive)
        if 9 <= ball_number <= 15:
            # Clip paths 
            clipPathTop = 'top-clip-%d' % ball_number
            clipPathBottom = 'bottom-clip-%d' % ball_number

            # Format top third of ball 
            ball_svg += '<clipPath id="%s">\n' % clipPathTop
            ball_svg += '  <rect x="%d" y="%d" width="%d" height="%d" />\n' % (x - radius, y - radius, radius * 2, radius * (2/3))
            ball_svg += '</clipPath>\n'

            # Format bottom third of ball 
            ball_svg += '<clipPath id="%s">\n' % clipPathBottom
            ball_svg += '  <rect x="%d" y="%d" width="%d" height="%d" />\n' % (x - radius, y + (radius / 3), radius * 2, radius * (2/3))
            ball_svg += '</clipPath>\n'

            # # Apply clip paths to the ball 
            ball_svg += '<circle cx="%d" cy="%d" r="%d" fill="white" clip-path="url(#%s)" />\n' % (x, y, radius, clipPathTop)
            ball_svg += '<circle cx="%d" cy="%d" r="%d" fill="white" clip-path="url(#%s)" />\n' % (x, y, radius, clipPathBottom)
        
        return ball_svg

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires position (x,y) 
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;

    def svg(self):
        """cx: position of hole (x), cy: position of hole (y), r: hole radius."""
        return """<circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """
    
    def __init__( self, y ):
        """
        Constructor function. Requires position (y) 
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;
    
    def svg(self):
        """y is -25 (top cushion) or 2700 (bottom cushion)."""
        if self.obj.hcushion.y == 0:
            return """<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        return """<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (self.obj.hcushion.y)

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires position (x) 
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;

    def svg(self):
        """x is -25 (left cushion) or 1350 (right cushion)."""
        if self.obj.vcushion.x == 0:
            return """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        return """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (self.obj.vcushion.x)

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg( self ):
        svgString = HEADER 
        for obj in self:
            if obj is not None:
                svgString += obj.svg()
        svgString += FOOTER 
        return svgString 

    def roll( self, t ):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                # Create a new ball with the same number as the old ball 
                new_ball = RollingBall(ball.obj.rolling_ball.number, Coordinate(0, 0), Coordinate(0, 0), Coordinate(0, 0))

                # Compute where it rolls to 
                phylib.phylib_roll(new_ball, ball, t)

                # Add ball to table 
                new += new_ball 

            if isinstance(ball, StillBall):
                # Create a new ball with the same number and pos as the old ball 
                new_ball = StillBall(ball.obj.still_ball.number, Coordinate(ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)) 

                # Add ball to table 
                new += new_ball 

        # Return table 
        return new
    
    def cueBall( self, table, xVel, yVel ):
        for ball in self:
            # Find cue ball 
            if isinstance(ball, StillBall):
                if ball.obj.still_ball.number == 0:

                    # Convert cue ball into rolling ball 
                    tempPosX = ball.obj.still_ball.pos.x
                    tempPosY = ball.obj.still_ball.pos.y
                    
                    # Change cue ball type 
                    ball.type = phylib.PHYLIB_ROLLING_BALL

                    # Assign new values to cue ball 
                    ball.obj.rolling_ball.number = 0
                    ball.obj.rolling_ball.pos.x = tempPosX
                    ball.obj.rolling_ball.pos.y = tempPosY
                    ball.obj.rolling_ball.vel.x = xVel
                    ball.obj.rolling_ball.vel.y = yVel

                    # Calculate acceleration 
                    PHYLIB_DRAG = 150.0
                    VEL_EPSILON = 0.01

                    lengthOfVel = (xVel * xVel + yVel * yVel)
                    ballSpeed = math.sqrt(lengthOfVel)

                    if ballSpeed > VEL_EPSILON:
                        xAcc = (-xVel / ballSpeed * PHYLIB_DRAG)
                        yAcc = (-yVel / ballSpeed * PHYLIB_DRAG)

                    # Assign remaining values to cue ball 
                    ball.obj.rolling_ball.acc.x = xAcc
                    ball.obj.rolling_ball.acc.y = yAcc
        

################################################################################
class Database:
    """
    Database class.
    """

    def __init__( self, reset=False ):
        # Check if reset value is True 
        if reset == True:
            if os.path.exists( 'phylib.db' ):
                os.remove( 'phylib.db' )

        self.conn = sqlite3.connect( 'phylib.db' )

    def createDB( self ):
        self.cur = self.conn.cursor()

        # Create all tables 
        # Ball table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Ball (
                        BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                        BALLNO INTEGER NOT NULL, 
                        XPOS FLOAT NOT NULL, 
                        YPOS FLOAT NOT NULL, 
                        XVEL FLOAT, 
                        YVEL FLOAT
                        );""")

        # TTable table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TTable (
                        TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                        TIME FLOAT NOT NULL
                        );""")

        # BallTable table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS BallTable (
                        BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
                        );""")

        # Game table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Game (
                        GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMENAME VARCHAR(64) NOT NULL
                        );""")

        # Player table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Player (
                        PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                        );""")

        # Shot table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Shot (
                        SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID INTEGER NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                        );""")

        # TableShot table 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TableShot (
                        TABLEID INTEGER NOT NULL,
                        SHOTID INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                        FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
                        );""")

        self.cur.close()
        self.conn.commit()

    def readTable( self, tableID ):
        self.cur = self.conn.cursor()

        table = Table()
        adjustedTableID = tableID + 1

        # Find all details of a ball 
        self.cur.execute("""SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME FROM Ball 
                            JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                            JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                            WHERE TTable.TABLEID = ?"""
                            ,
                            (adjustedTableID,))

        # Get tuple of details of the ball 
        results = self.cur.fetchall()

        # Null check 
        if not results:
            return None

        # Convert all balls to StillBalls and RollingBalls 
        for ballNum, xPos, yPos, xVel, yVel, time in results:
            table.time = time
            
            # StillBall 
            if xVel == 0 and yVel == 0:
                ball = StillBall(ballNum, Coordinate(xPos, yPos))
            # RollingBall 
            else:
                # Calculate acceleration 
                PHYLIB_DRAG = 150.0
                VEL_EPSILON = 0.01

                lengthOfVel = (xVel * xVel + yVel * yVel)
                ballSpeed = math.sqrt(lengthOfVel)

                if ballSpeed > VEL_EPSILON:
                    xAcc = (-xVel / ballSpeed * PHYLIB_DRAG)
                    yAcc = (-yVel / ballSpeed * PHYLIB_DRAG)

                ball = RollingBall(ballNum, Coordinate(xPos, yPos), Coordinate(xVel, yVel), Coordinate(xAcc, yAcc))

            # Add ball to table 
            table += ball

        self.cur.close()
        self.conn.commit()

        return table

    def writeTable( self, table ):
        self.cur = self.conn.cursor()

        # Insert table time into TTable 
        self.cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))

        # Get tableID 
        tableID = self.cur.lastrowid

        # Record all balls on the table 
        for ball in table:
            if isinstance(ball, (StillBall, RollingBall)):
                # RollingBall 
                if isinstance(ball, RollingBall):
                    self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                    (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                # StillBall 
                else:
                    self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                    (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y, 0, 0))
                # Get ballID 
                ballID = self.cur.lastrowid
                # Insert BALLID and TABLEID into BallTable 
                self.cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballID, tableID))

        self.cur.close()
        self.conn.commit()

        return tableID - 1

    def getGame( self, gameID ):
        self.cur = self.conn.cursor()
        
        # Find gameName, player1Name and player2Name that match the gameID 
        self.cur.execute("""SELECT Game.GAMEID, Game.GAMENAME, p1.PLAYERNAME AS Player1, p2.PLAYERNAME AS Player2
                           FROM Game 
                           JOIN Player p1 ON Game.GAMEID = p1.GAMEID
                           JOIN Player p2 ON Game.GAMEID = p2.GAMEID
                           WHERE Game.GAMEID = ? AND p1.PLAYERID < p2.PLAYERID
                           LIMIT 1""", (gameID,))

        # Get tuple of gameName, player1Name and player2Name 
        result = self.cur.fetchone()
        
        self.conn.commit()
        self.cur.close()
        
        if result:
            # Return gameName, player1Name and player2Name to Game class 
            return result
        else:
            return None

    def setGame( self, gameName, player1Name, player2Name ):
        self.cur = self.conn.cursor()

        # Insert gameName into Game table 
        self.cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        # Get gameID 
        gameID = self.cur.lastrowid

        # Insert GAMEID and PLAYERNAME into Player table for both players 1 and 2 
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))
        
        self.conn.commit()
        self.cur.close()

        # Return gameID to the Game class
        return gameID
    
    def newShot( self, playerName, gameID ):
        self.cur = self.conn.cursor()
        
        # Find a playerID that matches with the playerName and gameID 
        self.cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?", (playerName, gameID))
        playerID = self.cur.fetchone()

        # Insert PLAYERID and GAMEID into Shot table 
        self.cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID[0], gameID))
        shotID = self.cur.lastrowid
        
        self.conn.commit()
        self.cur.close()

        # Return shotID to shoot() 
        return shotID

    def recordTableShot( self, tableID, shotID ):
        self.cur = self.conn.cursor()

        # Insert TABLEID and SHOTID into TableShot table 
        self.cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableID, shotID))

        self.conn.commit()
        self.cur.close()

    def close( self ):
        # Commit and close connection 
        self.conn.commit()
        self.conn.close()

################################################################################
class Game:
    """
    Game class.
    """

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        self.db = Database()
        # Case where only gameID is provided 
        if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            self.gameID = gameID + 1
            gameInfo = self.db.getGame(gameID) # Retrieve values gameName, player1Name and player2Name from Game and Player tables 
            self.gameName = gameInfo[1]
            self.player1Name = gameInfo[2]
            self.player2Name = gameInfo[3]

        # Case where gameName, player1Name and player2Name are provided 
        elif gameID is None and isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str):
            self.gameID = self.db.setGame(gameName, player1Name, player2Name) # Add row to the Game table and two rows to the Player table 
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

        else:
            raise TypeError("Invalid combination of arguments passed to constructor.")

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        # New entry to shot table 
        shotID = self.db.newShot(playerName, self.gameID)

        # Find the cue ball 
        table.cueBall(table, xvel, yvel)
        
        # Create copy of table to track time between segments 
        copyTable = table
        copyTable = copyTable.segment()

        # Start time 
        segmentStart = table.time  
        
        # Repeated call on segment 
        while copyTable:
            segmentLength = copyTable.time - segmentStart
            totalFrames = int(segmentLength / FRAME_INTERVAL)

            # Loop over number of frames 
            for i in range(totalFrames):
                # Integer multiplied by FRAME_INTERVAL 
                frameTime = i * FRAME_INTERVAL
                
                # Roll to create next table 
                nextTable = table.roll(frameTime) 

                # Update time 
                nextTable.time = segmentStart + frameTime
                
                # Save to database 
                tableID = self.db.writeTable(nextTable)
                self.db.recordTableShot(tableID, shotID)

            # Segment tables and save time 
            table = table.segment()
            segmentStart = table.time
            copyTable = copyTable.segment()

        tableID = self.db.writeTable(table)

        return table, tableID

    def initializeGame( self, db ):
        # Initialize a table 
        table = Table()
        table_id = 0
        
        # Initialize all balls onto the table 
        # 0 ball (Cue ball)
        pos = Coordinate(675, 2100)
        sb  = StillBall(0, pos)
        table += sb

        # 1st ball position
        pos = Coordinate(674, 800)
        sb = StillBall(1, pos)
        table += sb

        # 2nd ball position
        pos = Coordinate(710, 744)
        sb = StillBall(2, pos)
        table += sb

        # 3rd ball position
        pos = Coordinate(640, 745)
        sb = StillBall(15, pos)
        table += sb

        # 4th ball position
        pos = Coordinate(740, 688)
        sb = StillBall(14, pos)
        table += sb

        # 5th ball position
        pos = Coordinate(675, 689)
        sb = StillBall(8, pos)
        table += sb

        # 6th ball position
        pos = Coordinate(610, 690)
        sb = StillBall(3, pos)
        table += sb

        # 7th ball position
        pos = Coordinate(775, 632)
        sb = StillBall(4, pos)
        table += sb

        # 8th ball position
        pos = Coordinate(710, 633)
        sb = StillBall(13, pos)
        table += sb

        # 9th ball position
        pos = Coordinate(640, 634)
        sb = StillBall(5, pos)
        table += sb

        # 10th ball position
        pos = Coordinate(575, 635)
        sb = StillBall(12, pos)
        table += sb

        # 11th ball position
        pos = Coordinate(805, 576)
        sb = StillBall(11, pos)
        table += sb

        # 12th ball position
        pos = Coordinate(740, 577)
        sb = StillBall(6, pos)
        table += sb

        # 13th ball position
        pos = Coordinate(675, 578)
        sb = StillBall(10, pos)
        table += sb

        # 14th ball position
        pos = Coordinate(610, 579)
        sb = StillBall(7, pos)
        table += sb

        # 15th ball position
        pos = Coordinate(545, 580)
        sb = StillBall(9, pos)
        table += sb

        # Write to database 
        db.writeTable(table)

        # Create a starter svg file 
        with open("table%02d.svg" % table_id, "w") as fp:
            fp.write(table.svg());

        # Return starting table 
        return table

    def gameRules( self, table, prevTable, currentPlayer, currentTurn, didBallSink, lowPlayer, highPlayer ):
        firstSunkBallNumber = 0
        gameStatus = 1
        lowBalls = [11, 12, 16, 17, 19, 22, 24]
        highBalls = [13, 14, 18, 20, 21, 23, 25]
        
        # If cue ball is hit into a hole 
        if table[10] == None:
            pos = Coordinate(675, 2100)
            sb  = StillBall(0, pos)
            table += sb
        
        if table != prevTable:
            for i in range(11, 26):
                if table[i] == None:
                    if prevTable[i] != None:
                        # Assign high/low balls to players 
                        if didBallSink == 0:
                            firstSunkBallNumber = prevTable[i].obj.still_ball.number
                            return table, gameStatus, firstSunkBallNumber, currentTurn
                        # Give another turn 
                        else:
                            if currentTurn == 0 and (i in lowBalls) and currentPlayer == lowPlayer:
                                currentTurn = 1
                            elif currentTurn == 1 and (i in lowBalls) and currentPlayer == lowPlayer:
                                currentTurn = 0
                            elif currentTurn == 0 and (i in highBalls) and currentPlayer == highPlayer:
                                currentTurn = 1
                            elif currentTurn == 1 and (i in highBalls) and currentPlayer == highPlayer:
                                currentTurn = 0
                            else:
                                # If 8 ball is hit into a hole 
                                if i == 15:
                                    if all(table[j] is None for j in [11, 12, 16, 17, 19, 22, 24]) and (lowPlayer == currentPlayer):
                                        gameStatus = 0
                                        return table, gameStatus, firstSunkBallNumber, currentTurn
                                    elif all(table[j] is None for j in [13, 14, 18, 20, 21, 23, 25]) and (highPlayer == currentPlayer):
                                        gameStatus = 0
                                        return table, gameStatus, firstSunkBallNumber, currentTurn
                                    else:
                                        gameStatus = 2
                                        return table, gameStatus, firstSunkBallNumber, currentTurn
                                else:
                                    gameStatus = 1

        if currentTurn == 0:
            currentTurn = 1
        else:
            currentTurn = 0

        return table, gameStatus, firstSunkBallNumber, currentTurn
