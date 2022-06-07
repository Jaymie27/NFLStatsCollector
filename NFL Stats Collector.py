
from bs4 import BeautifulSoup
import requests 
import xlsxwriter

# This code is scraping data on ESPN 
# You get NFL players stats (from the best to the worst)

url = "https://www.espn.com/nfl/stats/player"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

stats = []
i = 0
colRank = 0
colPlayer = 1
colTeam= 2
colCMP = 3
colYDS= 4
colTD = 5
colINT = 6
colRating = 7


workbook = xlsxwriter.Workbook('NFLStats.xlsx')
worksheet = workbook.add_worksheet("2021_NFL_Season")

#############################################

def write_in_excel_file(row, col, content):
        worksheet.write(row, col, content)

def write_header():
    worksheet.write("A1", "Rank")
    worksheet.write("B1", "Player")
    worksheet.write("C1", "Team")
    worksheet.write("D1", "CMP %")
    worksheet.write("E1", "YDS")
    worksheet.write("F1", "TD")
    worksheet.write("G1", "INT")
    worksheet.write("H1", "Rating")

def scrape_rank_player_team():
    i = 0
    for rows in soup.find_all("tr", {'class': "Table__TR--sm"}):           
        player = rows.find('a', {'class': "AnchorLink"})
        team = rows.find('span', {'class': "pl2 n10 athleteCell__teamAbbrev"})
        rank = rows.find('td', {'class': "Table__TD"})

        if player is not None:
            write_in_excel_file(i + 1, colRank, rank.get_text())
            write_in_excel_file(i + 1, colPlayer, player.get_text())
            write_in_excel_file(i + 1, colTeam, team.get_text())

        i = i + 1

def scrape_BuildStats():
    i = 0
    table = soup.find('table', {'class': "Table Table--align-right"})
    for rows in table.find_all('tr'):   
        datas = rows.find_all("td")[2:]
        stats.append(datas)  
        i = i + 1

def write_Stats_in_excel():
    i = 1
    for data in stats:
        if i < 51:
            write_in_excel_file(i, colCMP, stats[i][2].get_text())
            write_in_excel_file(i, colYDS, stats[i][3].get_text())
            write_in_excel_file(i, colTD, stats[i][7].get_text())
            write_in_excel_file(i, colINT, stats[i][8].get_text())
            write_in_excel_file(i, colRating, stats[i][12].get_text())
        i = i + 1


################################################


write_header()

scrape_rank_player_team()

scrape_BuildStats()

write_Stats_in_excel()

workbook.close()