from bs4 import BeautifulSoup
import requests

url = "https://www.ewrc-results.com"

def removeCancelled(rally_list):
    for rally in list(rally_list):
        page = requests.get(rally_list[rally])
        bs = BeautifulSoup(page.content, 'html.parser')
        widget = bs.find("div", class_ = "widget-canceled")
        if widget:
            del rally_list[rally]
    return rally_list

def rallyList(season):
    global url
    seasonUrl = (url + ("/season/{0}/").format(season))
    rally_list = dict()

    page = requests.get(seasonUrl)
    bs = BeautifulSoup(page.content, 'html.parser')

    for item in bs.findAll("div", class_ = "season-event-name"):
        rallyName = item.find("a").contents[0]
        rally_list[str(rallyName)] = (url + item.find('a')['href'])
    
    return removeCancelled(rally_list)

def rallyResults(rally, season):
    global rallyList
    rally_list = rallyList(season)

    rally_standings = dict()

    page = requests.get(rally_list[rally])
    bs = BeautifulSoup(page.content, 'html.parser')

    results = bs.find(id='mainblock')

    for driver in results.findAll('td', class_ = "final-entry"):
        driver_result = dict()
        try:
            driver_result["Nimi"] = driver.find('a').contents[0]
            driver_result["Auto"] = driver.find("td", class_ = "final-results-car").contents[0]
            driver_result["Aeg"] = driver.find("td", class_ = "bold td_right final-results-times").contents[0]
            rally_standings[driver_result["Nimi"]] = driver_result
        except:
            pass
    
    return rally_standings


def driverList(season):
    global url
    seasonUrl = (url + ("/season/{0}/").format(season))
    driver_list = []

    page = requests.get(seasonUrl)
    bs = BeautifulSoup(page.content, 'html.parser')
    table = bs.find("table", class_ = "points table_h")

    for row in table.findAll("tr", {"class":['table_sude', 'table_liche']}):
        driver_list.append(row.find('a').contents[0])
    
    return sorted(driver_list)

def driverResults(season, driverName):
    pass

# rallyResults("88. Rallye Automobile de Monte-Carlo 2020", 2020)