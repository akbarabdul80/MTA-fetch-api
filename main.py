import requests
from bs4 import BeautifulSoup
import data.db_brosur as db_brosur
import data.model.data_db as model_data_db
from conf import conf_db

# Firebase
import firebase_admin
from firebase_admin import credentials

# Fetch the service account key JSON file contents
cred = credentials.Certificate(conf_db.CRED_FIREBAE)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': conf_db.DATABASE_URL
})

headers = {
    'authority': 'mta.or.id',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'sec-ch-ua-platform': 'macOS',
    'origin': 'https://mta.or.id',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://mta.or.id/?page_id=0&limit=&q=%20&catid=31',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'PHPSESSID=d26a3ea42a576f99873e04a8e1a0e50d',
}

params = (
    ('juwpfisadmin', 'false'),
    ('action', 'wpfd'),
    ('task', 'search.display'),
)

data = {
    'limit': "-1",
    'q': ' ',
    'catid': '31'
}

response = requests.post('https://mta.or.id/wp-admin/admin-ajax.php', headers=headers, params=params, data=data)

data = BeautifulSoup(response.text, 'html.parser')
table = data.findAll("table", {"class": "table"})[0]

rows = table.findAll("tr")
count = 1

hasil = []
for row in rows:
    info = []
    for cell in row.findAll(["td", "th"]):
        if cell.get_text(strip=True) != "":
            info.append(cell.get_text(strip=True))
        else:
            href = cell.find("a", {"class": "downloadlink"}, href=True)
            if href is not None:
                info.append(href["href"])
                count += 1

    hasil.append(info)

for data in hasil:
    db_brosur.insert_schedule(
        model_data_db.DataBrosur(
            data[0],
            data[3],
            data[4],
            data[1],
            data[2]
        )
    )
