import sys
import os
import Physics
import math
import json
import gzip
from io import BytesIO

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl;

class DoGetAndDoPost(BaseHTTPRequestHandler):
    # Global variables 
    db = None
    gameInstance = None
    currentTable = None
    previousTable = None
    currentTableID = None
    previousTableID = 0
    gameStatus = 1 # 0: Stop game, 1: Continue game, 2: Stop game (8-ball went in early)
    currentTurn = None # 0: Player 1, 1: Player 2 
    didBallSink = 0 # 0: No balls sank, 1: 1+ balls sank 
    lowPlayer = None
    highPlayer = None

    # Initial page 
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/game.html':

            # Open game.html 
            with open('game.html') as fp:
                content = fp.read()

                # Response 
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))

        # Respons for fail 
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    # Page updates 
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/game.html':

            # Parse information from html page 
            contentLength = int(self.headers['Content-Length'])
            postData = self.rfile.read(contentLength)
            data = json.loads(postData.decode('utf-8'))

            # Data passed through json 
            xDifference = data['xDiff']
            yDifference = data['yDiff']
            player1 = data['p1']
            player2 = data['p2']
            restartGameValue = data['restart']
            DoGetAndDoPost.currentTurn = data['turn']
            DoGetAndDoPost.lowPlayer = data['lp']
            DoGetAndDoPost.highPlayer = data['hp']

            # Player list for indexing purposes 
            playerList = []
            playerList.append(player1)
            playerList.append(player2)

            # Run this if game hasn't been initialized 
            if DoGetAndDoPost.gameInstance == None:
                DoGetAndDoPost.gameInstance = Physics.Game(gameName="Game 01", player1Name=player1, player2Name=player2) # Creates game instance with player names 
                DoGetAndDoPost.currentTable = DoGetAndDoPost.gameInstance.initializeGame(DoGetAndDoPost.db) # Initializes game table 
                DoGetAndDoPost.previousTable = DoGetAndDoPost.currentTable # Saves current table as previous table 

            # Run this if the reset button is pressed 
            if restartGameValue == 1:
                DoGetAndDoPost.db = Physics.Database(reset=True) # Reset data base 
                DoGetAndDoPost.db.createDB() # Create tables 
                DoGetAndDoPost.gameInstance = Physics.Game(gameName="Game 01", player1Name=player1, player2Name=player2) # Creates game instance with existing player names 
                DoGetAndDoPost.currentTable = DoGetAndDoPost.gameInstance.initializeGame(DoGetAndDoPost.db) # Initializes new game table 
                DoGetAndDoPost.previousTable = DoGetAndDoPost.currentTable # Saves current table as previous table 
                
                # Reset global variables 
                DoGetAndDoPost.currentTableID = None # Reset current table ID 
                DoGetAndDoPost.previousTableID = 0 # Reset previous table ID 
                DoGetAndDoPost.gameStatus = 1 # Game not stopped 
                DoGetAndDoPost.currentTurn = None # 0: Player 1, 1: Player 2 
                DoGetAndDoPost.didBallSink = 0 # 0: No balls sank, 1: 1+ balls sank 
            
            # Run this if game is initialized, game is supposed to continue, and the restart button was not pressed 
            if DoGetAndDoPost.gameInstance and DoGetAndDoPost.gameStatus and restartGameValue == 0:
                # Simulate the game with the parsed data 
                DoGetAndDoPost.currentTable, DoGetAndDoPost.currentTableID = DoGetAndDoPost.gameInstance.shoot("Game 01", playerList[DoGetAndDoPost.currentTurn], DoGetAndDoPost.currentTable, -xDifference * 10, -yDifference * 10)
                
                # Check if any events occured, return the fixed table, if the game should continue, the number of the first ball that was sunk, and who the next turn belongs to 
                fixedTable, DoGetAndDoPost.gameStatus, firstSunkBallNumber, DoGetAndDoPost.currentTurn = DoGetAndDoPost.gameInstance.gameRules(DoGetAndDoPost.currentTable, DoGetAndDoPost.previousTable, playerList[DoGetAndDoPost.currentTurn], DoGetAndDoPost.currentTurn, DoGetAndDoPost.didBallSink, DoGetAndDoPost.lowPlayer, DoGetAndDoPost.highPlayer)

                # Determines if high/low balls were assigned 
                if firstSunkBallNumber != 0:
                    DoGetAndDoPost.didBallSink = 1

                # Save current table to previous table for the next shot 
                DoGetAndDoPost.previousTable = DoGetAndDoPost.currentTable

                # Write fixed table to database 
                someTableID = DoGetAndDoPost.db.writeTable(fixedTable)
                
                # Svg creation for animation 
                svgString = ""
                svgTableID = DoGetAndDoPost.previousTableID
                DoGetAndDoPost.previousTableID = DoGetAndDoPost.currentTableID
                svgTable = DoGetAndDoPost.db.readTable(svgTableID)

                # Add first table to svg string 
                svgString += svgTable.svg()

                # Add every table from current tableID to the last tableID to the svg string 
                while svgTable:
                    svgTableID += 1
                    svgTable = DoGetAndDoPost.db.readTable(svgTableID)
                    if not svgTable:
                        break
                    svgString += svgTable.svg()

                # Format data that needs to be sent back to the page 
                dataList = []
                dataList.append(svgString) # Svg string 
                dataList.append(DoGetAndDoPost.gameStatus) # Game status 
                dataList.append(firstSunkBallNumber) # First ball sunk number 
                dataList.append(DoGetAndDoPost.currentTurn) # Turn number 

                # Reset this value in case the restart button was pressed 
                restartGameValue = 0

                # Convert dataList to JSON and gzip compress the data
                jsonData = json.dumps(dataList)
                compressedData = BytesIO()
                
                with gzip.GzipFile(fileobj=compressedData, mode='wb') as f:
                    f.write(jsonData.encode('utf-8'))

                compressedData = compressedData.getvalue()

                # Set the response headers and write the gzipped data
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Content-Encoding', 'gzip')
                self.send_header('Content-Length', str(len(compressedData)))
                self.end_headers()
                self.wfile.write(compressedData)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, 'utf-8'))


if __name__ == "__main__":

    DoGetAndDoPost.db = Physics.Database(reset=True)
    DoGetAndDoPost.db.createDB()

    httpd = HTTPServer(('localhost', int(sys.argv[1])), DoGetAndDoPost)
    print("Server listing in port:  ", int(sys.argv[1]))
    httpd.serve_forever()
