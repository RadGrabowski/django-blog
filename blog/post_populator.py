import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_website.settings')

import django
django.setup()

from faker import Faker
from blog.models import Post, User
from datetime import datetime
import random


fake = Faker()

if __name__ == '__main__':
    for post in range(18):
        p = Post()
        p.author = random.choice(User.objects.all())
        p.body = fake.text()
        split = p.body.split()
        p.title = split[0] + ' ' + split[1]
        p.slug = split[0].lower() + '-' + split[1].lower()
        p.publish = datetime.now()
        p.status = 'published'
        p.save()
