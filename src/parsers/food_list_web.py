from bs4 import BeautifulSoup


with open(r'./demo/foodlist.htm', 'r', encoding='iso-8859-1') as f:
    page_source = f.read()
    soup = BeautifulSoup(page_source, 'lxml')
    tds = soup.find_all("td")

    food_list = []
    for td in tds[11:-9]:
        food_list.extend(td.text.strip().split("\n"))

