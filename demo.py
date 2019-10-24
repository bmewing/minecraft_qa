#! /usr/local/bin/python3.7

from utils import search_index, BertSquad
import argparse

bert_squad = BertSquad()

ap = argparse.ArgumentParser()
ap.add_argument('-q', '--question', default='where can I find diamonds',
                help='Question you want answered.')
ap.add_argument('-d', '--dir', default='whoosh',
                help='Directory of whoosh index')
ap.add_argument('-i', '--index', default='minecraft',
                help='Name of whoosh index')
ap.add_argument('-l', '--limit', default=5,
                help='How many results to return?')
args = vars(ap.parse_args())

if __name__ == '__main__':
    relevant = search_index(question=args['question'],
                       dir=args['dir'],
                       indexname=args['index'],
                       limit=int(args['limit']))
    answers = [bert_squad.ask_question([r], [args['question']]) for r in relevant]
    for a in answers:
        print(a)