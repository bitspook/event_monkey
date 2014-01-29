#!/usr/bin/env python
import re
import os
import sh
import random
from datetime import date

from sqlalchemy.sql.expression import func

from models import Base, engine, session
from models import Event, Content, Tag

from post import Post
from cury import Cury


def syncdb():
    Base.metadata.drop_all(engine)
    print "Dropped all tables."
    Base.metadata.create_all(engine)
    print "Created all tables."

def shell():
    from IPython.terminal import embed
    ipshell = embed.InteractiveShellEmbed()
    Base.metadata.create_all(engine)
    ipshell()

def genpost(masalas=None, masala_dir=None, spices=1, num_posts=1, post_type=None, gen_posts_dir='./octopress_site/source/_posts', raw_posts_dir='./raw_posts'
):
    posts = []
    if not post_type:
        post_type = random.choice([t.split('.')[0] for t in os.listdir(raw_posts_dir)])

    if post_type and post_type != 'random' and not masalas:
        masalas = post_type


    for i in range(num_posts):
        cury = Cury(masalas=masalas, masala_dir=masala_dir, spices=spices)
        post = Post(cury=cury, post_type=post_type)
        write_post_in_dir(post, gen_posts_dir)

def write_post_in_dir( post, gen_posts_dir):
    post_file_name = "{date}-{title}.md".format(date=date.today(), title=re.sub(r'[,\'\.\|]', '', post.cury.title.encode('utf-8')).replace(' ','-').lower())

    if post_file_name in os.listdir('{}'.format(gen_posts_dir)):
        from time import time
        post_file_name = "{date}-{title}-{time}.md".format(date=date.today(), title=re.sub(r'[,\'\.\|]', '', post.cury.title).replace(' ','-').lower(), time=unicode(int(time())))
        print "Repeated post renamed"

    with open("{}/{}".format(gen_posts_dir, post_file_name), 'wb') as f:
        f.write(post.md_post)
    print "Post generated: {}/{}".format(gen_posts_dir, post_file_name)

def autogen(num_posts=1):
    sites = [
        './octopress_site_1',
        './octopress_site_2',
        './octopress_site_3',
        './octopress_site_4',
    ]
    for site in sites:
        print genpost(gen_posts_dir="{}/source/_posts".format(site), num_posts=num_posts)

        sh.cd(site)
        print sh.rake('generate')
        print sh.rake('push')
        sh.cd("../")

def clock(time_minutes=15):
    from apscheduler.scheduler import Scheduler
    from apscheduler.events import EVENT_JOB_EXECUTED
    print "Starting scheduler"
    sched = Scheduler()
    sched.start()

    def a_g():
        print autogen()


    sched.add_interval_job(a_g, minutes=time_minutes)

    while True:
        pass

if __name__ == "__main__":
    import argh
    argh.dispatch_commands([shell, genpost, autogen, clock])
