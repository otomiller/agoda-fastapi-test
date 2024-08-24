# Database connection parameters
DB_PARAMS = {
    'dbname': 'agoda',
    'user': 'postgres',
    'password': '9vtTWvyxyHCpEvq',
    'host': '10.0.255.250',
    'port': '5432'
}

API_URL = f'https://affiliatefeed.agoda.com/datafeeds/feed/getfeed?apikey={API_KEY}&mtypeid=1&feed_id=19&mHotel_id='

HOTEL_IDS = [
    28722004, 28721997, 28722003, 28722002, 28722001, 28722000, 28721999,
    28721998, 28722006, 28722005, 2937, 64748, 105040, 105262, 147265,
    1144272, 1144275, 2064981, 6139, 70299, 61912, 782709, 9107, 90772,
    263253, 178562, 51461, 285764, 51921, 267656, 178523, 6063, 240568,
    234458, 267698, 196931, 267121, 240353, 42976, 6852414, 9412311,
    1095091, 1193699, 4521, 118508, 11484, 2713, 43775, 70697, 178188,
    7947, 4877
]

XML_DIRECTORY = 'objects'