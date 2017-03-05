# coding: utf-8

from celery import Celery

app = Celery('blog', include=['celery_tasks'])
app.config_from_object('local_settings')

if __name__ == '__main__':
    app.start()
