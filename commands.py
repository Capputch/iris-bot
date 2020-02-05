from models import Karma, KarmaChange
from sqlalchemy import desc
import random

def say(db_session, *args):
    return [' '.join(args)]

def rand(db_session, *args):
    if len(args) != 2:
        return ['!rand <min> <max>']
    try:
        return [str(random.randint(int(args[0]), int(args[1])))]
    except ValueError:
        return ['Please give me integers']

def randf(db_session, *args):
    return [str(random.random())]

def karma(db_session, *args):
    reply = ''
    if len(args) == 0:
        return ['No item provided.']

    items = []
    no_karma = []
    for a in args:
        a = a.strip().lower()
        kitem = db_session.query(Karma).filter(Karma.name == a).one_or_none()
        if kitem:
            last_change = db_session.query(KarmaChange).filter(KarmaChange.karma_id==kitem.id).order_by(desc(KarmaChange.changed_at)).first()
            items.append((a,last_change.score))
        else:
            no_karma.append(a)

    if len(items) > 1:
        k_plural = 's are'
    else:
        k_plural = ' is'

    if len(no_karma) > 1:
        nk_plural = 'these have'
    else:
        nk_plural = 'this has'


    if len(items) > 0:
        reply += f'The karma score{k_plural} as follows:\n'
        for i,s in items:
            reply += f' • **{i}** ({s})\n'

    if len(no_karma) > 0:
        reply += f'Sorry, {nk_plural} no karma:\n'
        for nk in no_karma:
            reply += f' • **{nk}**\n'

    return [reply.rstrip()]
