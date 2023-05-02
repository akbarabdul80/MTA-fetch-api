import requests
from bs4 import BeautifulSoup
import data.db_brosur as db_brosur
import data.model.data_db as model_data_db
import ext.string_ext

# Database
from conf import conf_db
import ext.database_ext as db_ext

# Firebase
import firebase_admin
from firebase_admin import credentials

from ext.download_etx import download_file_pdf

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

last_brosur = db_ext.get_last_brosur_by_date()

# list brosur
result_brosur = []
for data in hasil:
    result_brosur.append(
        model_data_db.DataBrosur(
            data[0],
            ext.string_ext.format_string_to_date_sqlite(data[3]),
            data[4],
            data[1],
            data[2]
        )
    )

# sort brosur by date
result_brosur.sort(key=lambda x: x.date_create, reverse=False)

# insert to db
if last_brosur is not None and result_brosur[len(result_brosur) - 1].file_url == last_brosur.file_url:
    print("Data is up to date")
    exit()
else:
    for data in result_brosur:
        if last_brosur is not None and data.file_url == last_brosur.file_url:
            break
        else:
            db_brosur.insert_data(data)
            download_file_pdf(data.title, data.file_url)
