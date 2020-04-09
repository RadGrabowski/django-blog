import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_website.settings')

import django

django.setup()

from faker import Faker
from blog.models import Post, User, Comment
from datetime import datetime
import random

fake = Faker()

if __name__ == '__main__':
    # for post in range(18):
    #     p = Post()
    #     p.author = random.choice(User.objects.all())
    #     p.body = fake.text()
    #     split = p.body.split()
    #     p.title = split[0] + ' ' + split[1]
    #     p.slug = split[0].lower() + '-' + split[1].lower()
    #     p.publish = datetime.now()
    #     p.status = 'published'
    #     p.save()

    # for comment in range(120):
    #     c = Comment()
    #     c.name = fake.name()
    #     c.post = random.choice(Post.published.all())
    #     c.email = fake.email()
    #     c.body = ' '.join(fake.text().split()[:10]) + '.'
    #     c.active = True
    #     c.save()

    for post in Post.objects.all():
        tags = []
        choices = ['music', 'health', 'sport', 'medicine', 'politics', 'money', 'education', 'science', 'humor',
                   'technology', 'art', 'food', 'nature', 'travelling', 'psychology', 'architecture', 'life', 'animals']
        random.shuffle(choices)
        for tag in range(3):
            tags.append(choices.pop())
        # print(post, tags)
        post.tags.add(*tags)
