# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    dt = [datetime.strptime(odt, "%Y-%m-%d").strftime('%d %b %Y') for odt in old_dates]
    return dt

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    v = []
    
    date_start_with = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        v.append(date_start_with + timedelta(days=i))
        
    return v


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    vls_len = len(values)
    x = date_range(start_date, len(values))
    i = list(zip(x, values))
    return i

def extractFeeData(infile):
    
    fields = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as f:
        removehdr = DictReader(f, fieldnames=fields)
        removehdr_rows = [row for row in removehdr]

        removehdr_rows.pop(0)
    
    return removehdr_rows

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    
    frmt = '%m/%d/%Y'
    dats = extractFeeData(infile)
    onlyfees = defaultdict(float)

    for eachline in dats:
       
        patron = eachline['patron_id']
        dueper = datetime.strptime(eachline['date_due'], frmt)
        returned_per = datetime.strptime(eachline['date_returned'], frmt)

        ds = (returned_per - dueper).days

        onlyfees[patron]+= 0.25 * ds if ds > 0 else 0.0

    storeRes = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in onlyfees.items()
    ]

    with open(outfile, 'w') as f:
        r = DictWriter(f, ['patron_id', 'late_fees'])
        r.writeheader()
        r.writerows(storeRes)



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    #BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    #BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report('book_returns.csv', OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
