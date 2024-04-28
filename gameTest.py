import Physics;

db = Physics.Database( reset=True )
db.createDB()

gameInstance = Physics.Game( gameName="Game 01", player1Name="Stefan", player2Name="Efren Reyes" )
gameInstance.initializeGame(db)

