import sqlite3
import argparse

parser = argparse.ArgumentParser(description="arguments for building a test database.")
parser.add_argument('--db', default='covid19.db', help='sqlite3 database')
parser.add_argument('--schema', default='schema.sql', help='schema definition')
parser.add_argument('--data', default='covid.sql', help='data')
args = parser.parse_args()

def init_db(dump_bulkdata=False):
    db = sqlite3.connect(
    args.db,        
    detect_types=sqlite3.PARSE_DECLTYPES
    )
    with open(args.schema, 'rt') as f_schema:
        db.executescript(f_schema.read())
    
    if (dump_bulkdata == True):
        with open(args.data) as f_data:
            db.executescript(f_data.read())

if __name__ == "__main__":
    init_db(dump_bulkdata=True)     