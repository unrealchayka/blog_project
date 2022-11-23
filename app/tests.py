from django.test import TestCase
from .models import *

class TestPost(TestCase):

    def setUp(self) -> None:
        Post.objects.all()
        return super().setUp()