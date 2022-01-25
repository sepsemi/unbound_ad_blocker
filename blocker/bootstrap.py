import re
import json
import requests
from concurrent.futures import as_completed, ThreadPoolExecutor

from database import Database

config = {}
valid_tlds = []

session = requests.Session()

domain_regex = re.compile(
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

def yield_get_content(category, url):
    chunk_size = 8096

    print("[get_content]: category={}, url={}".format(category, url))
    
    response = session.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=chunk_size):
        yield chunk.decode()

def bootstrap_database(database, result):
    for chunk in result:
        for line in chunk.split():      

            match_domain = domain_regex.search(line)
            if not match_domain:
                continue 

            domain = match_domain.group(0)
                
            # Check if tld is valid
            tld = domain.split('.')[-1]
            if tld not in valid_tlds:
                 continue 
            
            lenght = len(domain)
            database.table_insert('blacklist', lenght=lenght, tld=tld, domain=domain)

def bootstrap_domains(database):
    results = []
    lists = config['filter-lists']

    with ThreadPoolExecutor(max_workers = 10) as executor:
        for category, urls in lists.items():
            for url in urls:
                thread = executor.submit(yield_get_content, category, url)
                results.append(thread)    
        
        for future in as_completed(results):
            result = future.result()
            bootstrap_database(database, result)    
        
    # Commit the transaction
    database.conn.commit()


def main():
    global config
    global valid_tlds

    with open('./etc/tlds.txt') as fp:
        for line in fp.readlines():
            valid_tlds.append(line.rstrip())

    with open('./etc/config.json', 'r') as fp:
        config = json.load(fp)
   
    # create database and cursor
    database = Database()

    # Create the database with the tables we want
    for table in ['blacklist', 'whitelist', 'redacted']:
        database.table_create(table)

    # Start bootstrapping
    bootstrap_domains(database)
    
    

main()
