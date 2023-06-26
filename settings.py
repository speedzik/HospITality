FONT = "Calibri"
BIG_FONT_SIZE = 78
NORMAL_FONT_SIZE = 26

PINK = "#FF88BB"
BLUE = "#88BBFF"
WHITE = "#F2F2F2"
BLACK = "#282828"


db = mysql.connector.connect(
    host = "134.116.156.87 ",
    user = "root",
    passwd = "root",
    database = "hotel"
)
mycursor = db.cursor()