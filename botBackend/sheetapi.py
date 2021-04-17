import gspread
from decouple import config
from gspread_formatting import CellFormat, Color, format_cell_range, format_cell_ranges

def setupSheet(players : list, picks : int):
    
    # grab the sheet object so we can use it
    worksheet = __load_worksheet()

    """this sets up default values for the sheet. 
    This includes player names, pick count, and metadata
    in case the session needs to be restarted down
    the line"""
    
    # sheet setup pipeline
    __add_picks_incrementer(worksheet, picks)
    __add_players(worksheet, players)
    __add_color(worksheet, players, picks)

def __add_picks_incrementer(worksheet : object, picks : int):

    """ This adds an incrementer to the first column 
    in the sheet for the total number of picks. If 
    there are X picks for each player, then it will 
    number cells (2,1) to (X, 1) from 1 to X.\n
    (1,1)--> "Players"\n
    (2,1) --> 1\n
    (3,1) --> 2\n
    (4,1) --> 3\n
    (X,1) --> X-1\n   
    Notation: (Row, Col)\n
    Note: (1,1) is reserved for the word "Players" """

    row_player = 1
    row_incrementer = 2
    column = 1

    # save word "player" to (1,1) square
    worksheet.update_cell(row_player, column, "Players") 

    # number the first column starting at row 2
    # from numbers 1 to n where n is the pick count

    for i in range(picks):
        worksheet.update_cell(i + row_incrementer, column, i + 1) # row column info

def __add_players(worksheet : object, players : list):
    
    """ This adds the names of the players drafting
    to the sheet. """

    # row where names will be stored
    row = 1
    # shift over by 2 since index = 0 and we want to start at column 2
    columnShift = 2

    for i in range(len(players)):
        worksheet.update_cell(row, i + columnShift, str(players[i])) # row / column

def __add_color(worksheet : object, players : list, picks : int):
        
        """ This adds colors to the columns of the 
        players that are drafting. A unique color 
        is added to the player name and a second is 
        added to their card choices. """

        # list of colors to add to columns for player names (max of 8)
        # this is RGB in range of (0 - 1) * 255
        # order of colors: 
        # 0 - red - (248, 118, 118) ------- (244, 204, 204)
        # 1 - turqiouse - (122, 240, 255) ------- (224, 247, 250)
        # 2 - green - (132, 255, 187) ------- (231, 249, 239)
        # 3 - yellow - (255, 226, 123) ------- (254, 248, 227)
        # 4 - orange - (255, 142, 101) ------- (255, 230, 221)
        # 5 - blue - (122, 170, 255) ------- (232, 240, 254)
        # 6 - purple - (194, 167, 255) ------- (222, 208, 253)
        # 7 - pink - (250, 133, 207) ------- (248, 185, 225)                                   
        colorPlayerNames = [(248/255, 118/255, 118/255), (122/255, 240/255, 255/255), 
        (132/255, 255/255, 187/255), (255/255, 226/255, 123/255), (255/255, 142/255, 101/255), 
        (122/255, 170/255, 255/255), (194/255, 167/255, 255/255), (250/255, 133/255, 207/255)    ]

        colorCardSlots = [(244/255, 204/255, 204/255), (224/255, 247/255, 250/255), 
        (231/255, 249/255, 239/255), (254/255, 248/255, 227/255), (255/255, 230/255, 221/255), 
        (232/255, 240/255, 254/255), (222/255, 208/255, 253/255), (248/255, 185/255, 225/255)]

        # columns on first row for player names (up to 8 columns) 
        playerColumns = ['B1','C1','D1','E1','F1','G1','H1','I1']
    
        # first row is player name, 2nd down is cards so we have a shift of 1
        shift = 1

        # columns with row ranges for the card choices (up to 8 columns) 
        cardColumns = ['B2:B' + str(picks + shift),'C2:C' + str(picks + shift),
        'D2:D' + str(picks + shift),'E2:E' + str(picks + shift), 
        'F2:F' + str(picks + shift),'G2:G' + str(picks + shift),
        'H2:H' + str(picks + shift),'I2:I' + str(picks + shift)]

        for i in range(len(players)):
            playerColor = CellFormat(backgroundColor=Color(colorPlayerNames[i][0], colorPlayerNames[i][1], colorPlayerNames[i][2]))
            format_cell_range(worksheet, playerColumns[i], playerColor)
            cellColor = CellFormat(backgroundColor=Color(colorCardSlots[i][0], colorCardSlots[i][1], colorCardSlots[i][2]))
            format_cell_range(worksheet, cardColumns[i], cellColor)

def __load_worksheet():

    """this private method gets the worksheet in our google doc
    so we can start performing operations on it"""

    # load in the credentials file / json
    serviceAccount = gspread.service_account(filename='credentials.json')

    # grab the sheet I'm sharing by opening with the key in the url
    sheet = serviceAccount.open_by_key(config('GOOGLE_SHEET_URL_KEY'))

    # grab the first sheet
    worksheet = sheet.sheet1

    return worksheet

def pick(card_name : str, row : int, column : int):
    
    worksheet = __loadWorksheet()

    """ This adds the names of the players drafting
    to the sheet. """
    worksheet.update_cell(row, column, card_name)

def reset_sheet():

    """This clears the data on the sheet so it can 
    be ready for the next draft."""
    
    worksheet = __load_worksheet()
    
    # remove all values
    worksheet.clear()

    # remove color (set all to white)
    fmt = CellFormat(backgroundColor=Color(1, 1, 1))
    format_cell_ranges(worksheet, [('A:J', fmt)])
