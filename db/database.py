import psycopg2


"""
table "websites" columns: domain, status ('1'="phishing"/0="not phishing"/2="not in db". default - 0), 
                          is_phish (integer. start from 0), is_leg (integer. start from 0).
"""


def create_tables(cursor):
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS websites (domain text PRIMARY KEY, status integer DEFAULT 0,
                   is_phish integer DEFAULT 0, is_leg integer DEFAULT 0)
                   """)
    cursor.execute('CREATE TABLE IF NOT EXISTS verifiers (service_name text PRIMARY KEY, link text NOT NULL)')
    cursor.execute('INSERT INTO verifiers VALUES (%s, %s) ON CONFLICT DO NOTHING', ('GOOGLE_SECURE', 'https://transparencyreport.google.com/safe-browsing/search'))
    cursor.execute('INSERT INTO verifiers VALUES (%s, %s) ON CONFLICT DO NOTHING', ('PHISHTANK', 'http://checkurl.phishtank.com/checkurl/'))


def db_connect():
    conn = psycopg2.connect(dbname='phishsites', user='postgres',
                            password='postgres', host='127.0.0.1', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor


def db_disconnect(conn, cursor):
    cursor.close()
    conn.close()


def add_website(cursor, domain):
    cursor.execute('INSERT INTO websites (domain) VALUES (%s) ON CONFLICT DO NOTHING', (domain,))


def get_website_status(cursor, domain):
    cursor.execute('SELECT status FROM websites WHERE domain = %s', (domain,))
    status = cursor.fetchone()
    if status is None:
        return 2  # domain + 'is not in DB'
    elif status[0] == 1:
        return 1  # 'Phishing'
    else:
        return 0  # 'Legitimate'


def update_website_status(cursor, domain, new_status):
    status = 0
    if new_status == 'phish':
        status = 1
    cursor.execute('UPDATE websites SET status = %s WHERE domain = %s', (status, domain,))


def add_vote(cursor, domain, vote_type):
    add_website(cursor, domain)
    if vote_type == 'phish':
        cursor.execute('UPDATE websites SET is_phish = is_phish + 1 WHERE domain = %s', (domain,))
    else:
        cursor.execute('UPDATE websites SET is_leg = is_leg + 1 WHERE domain = %s', (domain,))


def get_votes(cursor, domain):
    cursor.execute('SELECT is_phish FROM websites WHERE domain = %s', (domain,))
    is_phish = cursor.fetchone()[0]
    cursor.execute('SELECT is_leg FROM websites WHERE domain = %s', (domain,))
    is_leg = cursor.fetchone()[0]
    return is_phish, is_leg


def get_verifiers_link(cursor, service):
    cursor.execute('SELECT link FROM verifiers WHERE service_name = %s', (service,))
    link = cursor.fetchone()[0]
    return link

