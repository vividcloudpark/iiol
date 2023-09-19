from __future__ import absolute_import, unicode_literals
# 어노테이션과 데코레이터는 다르다! python의 '데이코레이터' 사용을 위해 import
from celery import shared_task

# shared_task 데코레이팅 되어진 실질적 작업!


@shared_task
def add(x, y):
    return x + y
