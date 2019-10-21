import boto3
import time
import pandas as pd
import uuid

DOC = {'S3Object': {
    'Bucket': 'textract-console-us-east-1-62dd1c71-8d02-4a3f-a0c0-52df49f047a4',
    'Name': 'doc2.pdf'
}}

CRT = str(uuid.uuid4())


def extract_word(id, dict, blocks):
    try:
        return(dict[id])
    except KeyError:
        newid = [x for x in blocks if x['Id'] == id][0]['Relationships'][0]['Ids'][0]
        return(extract_word(newid, dict, blocks))


def process_forms(form, dict, blocks):
    try:
        value = [x['Ids'] for x in form['Relationships'] if x['Type'] == 'VALUE'][0]
        value = [extract_word(x, dict, blocks) for x in value]
    except (IndexError, KeyError):
        value = ""
    try:
        key =   [x['Ids'] for x in form['Relationships'] if x['Type'] == 'CHILD'][0]
        key =   [extract_word(x, dict, blocks) for x in key]
    except (IndexError, KeyError):
        key = ""
    if key and value:
        output = ' '.join(key)+' '+' '.join(value)
    else:
        output = None
    return(output)


def process_table_elem(teid, dict, blocks):
    child = [x for x in blocks if x['Id'] == teid][0]
    colid = child['ColumnIndex']
    colsp = child['ColumnSpan']
    rowid = child['RowIndex']
    rowsp = child['RowSpan']
    try:
        words_ids = [x['Ids'] for x in child['Relationships'] if x['Type'] == 'CHILD'][0]
        words =  [extract_word(x, dict, blocks) for x in words_ids]
        words = ' '.join(words)
    except KeyError:
        words = ""
    output = {
        "colid": colid,
        "colsp": colsp,
        "rowid": rowid,
        "rowsp": rowsp,
        "conte": words
    }
    return(output)


def process_tables(table, dict, blocks):
    table_elem = table['Relationships'][0]['Ids']
    elems = [process_table_elem(x, dict, blocks) for x in table_elem]
    ncol = max([x['colid'] for x in elems])
    nrow = max([x['rowid'] for x in elems])
    table = pd.DataFrame(columns = [x for x in range(ncol)], index = [x for x in range(nrow)])
    for e in elems:
        col_to_populate = [x for x in range(e['colid']-1,e['colid']-1+e['colsp'])]
        row_to_populate = [x for x in range(e['rowid']-1,e['rowid']-1+e['rowsp'])]
        for i in col_to_populate:
            for j in row_to_populate:
                table[i][j] = e['conte']
    return(table)


client = boto3.client('textract', region_name='us-east-1')
start = client.start_document_analysis(
    DocumentLocation=DOC,
    FeatureTypes=['TABLES', 'FORMS'],
    ClientRequestToken=CRT
)

collect = {'JobStatus': 'IN_PROGRESS'}

while collect['JobStatus'] == "IN_PROGRESS":
    time.sleep(3)
    collect = client.get_document_analysis(
        JobId = start['JobId']
    )

tables = [x for x in collect['Blocks'] if x['BlockType'] == 'TABLE']
forms =  [x for x in collect['Blocks'] if x['BlockType'] == 'KEY_VALUE_SET']
words =  [x for x in collect['Blocks'] if x['BlockType'] == 'WORD']
wdict = {}
for i in words:
    wdict[i['Id']] = i['Text']

addt_info = [process_forms(f, wdict, collect['Blocks']) for f in forms]
formatted_tables = [process_tables(t, wdict, collect['Blocks']) for t in tables]

for t in range(len(formatted_tables)):
    formatted_tables[t].to_csv('COA_Output_{}.csv'.format(t), header=False, index=False)
