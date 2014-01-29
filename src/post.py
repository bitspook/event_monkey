import random, os
from datetime import date

from sqlalchemy.sql.expression import func

from models import session
from models import Content
from cury import Cury

class Post(object):
    """Represents a single post in the blog.
    """

    def __init__(self, cury, post_type, raw_posts_dir='./raw_posts', images_url_file='./image_urls'):
        self.cury = cury
        self.real_content = self.get_post_content(num_posts=4)
        valid_post_types = [t.split('.')[0] for t in os.listdir(raw_posts_dir)]
        self.post_type = valid_post_types[random.randrange(0,2)]
        self.images_url_file = images_url_file
        if post_type:
            self.post_type = post_type
        if self.post_type not in valid_post_types:
            print "Invalid post type"
            print "Valid post types are:"
            for i in valid_post_types:
                print i
            from sys import exit
            exit()
        self.md_post = self.render_post_from_template(raw_posts_dir).encode('utf-8')

    def get_post_content(self, num_posts):
        return session.query(Content).order_by(func.random()).limit(num_posts).all()

    def render_post_from_template(self, raw_posts_dir):
        import os
        from jinja2 import Template
        templates = [i.replace('.md','') for i in os.listdir(raw_posts_dir)]
        selected_template = self.post_type
        if selected_template not in templates:
            print "Invalid post type. Make sure {}.md file is present in {}".format(selected_template, raw_posts_dir)
            import sys
            sys.exit()
        data={
            'messages': [c.body for c in self.real_content],
            'title': self.cury.title.replace('"',''),
            'keywords': self.cury.keywords,
            'search_terms': self.cury.search_terms,
            'date': str(date.today()),
            'images': self.get_random_image(num_images=3),
            'tags': self.cury.tags,
        }
        data['keyword'] = random.choice(data['search_terms']).replace('"','')
        data['excerpt'] = data['messages'][0].replace('\n','<br>').replace('"','')[:200]
        # following 3 lines are a hack. It's too late in night and i don't want to look into the matter
        # but messages appear without newlines by default. This fixes it.
        data['messages'][0] = data['messages'][0].replace('"','').replace('\n','<br>')
        data['messages'][1] = data['messages'][1].replace('"','').replace('\n','<br>')
        data['messages'][2] = data['messages'][2].replace('"','').replace('\n','<br>')
        with open("{}/{}.md".format(raw_posts_dir, selected_template)) as f:
            template = Template(f.read())
            md_post = template.render(data)
        return md_post

    def get_random_image(self, num_images):
        with open("{}".format(self.images_url_file)) as f:
            all_images = []
            for line in f:
                all_images.append(line.strip())
        images = random.sample(all_images, num_images)
        return images
