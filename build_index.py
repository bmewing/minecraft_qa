import argparse
import os
import json
import whoosh.index
from whoosh.fields import Schema, TEXT, ID
from tqdm import tqdm
from utils import ArticleAnalyzer


ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', default='whoosh',
                help='Name of directory to build whoosh index in')
ap.add_argument('-n', '--name', default='minecraft',
                help='Name to give whoosh index')
args = vars(ap.parse_args())

if not os.path.isdir(args['output']):
    os.mkdir(args['output'])

# Create whoosh index (or open if already exists)
if not whoosh.index.exists_in(args['output']):
    schema = Schema(
        pID=ID(stored=True, unique=True),
        url=ID(stored=True),
        content=TEXT(stored=True, analyzer=ArticleAnalyzer()),
        content_ner=TEXT(analyzer=ArticleAnalyzer()),
    )

    idx = whoosh.index.create_in(args['output'], schema=schema, indexname=args['name'])
else:
    idx = whoosh.index.open_dir(args['output'], indexname=args['name'])

# Write items articles to index
writer = idx.writer()
for i in tqdm(os.listdir('pages')):
    with open('pages/'+i) as f:
        doc = json.load(f)
    ner = ''
    if doc['ner'] is not None:
        ner = ' '.join(doc['ner'])
    writer.update_document(
        pID=i,
        url=doc['url'],
        content=doc['p'],
        content_ner=ner,
    )

writer.commit()