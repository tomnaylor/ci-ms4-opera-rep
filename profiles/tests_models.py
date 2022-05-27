""" TESTS FOR PROFILES MODELS """

from django.test import TestCase
from .models import UserComment, UserLike


class ProductionCommentModelTest(TestCase):
    """ Test production comment """
    fixtures = ["testdbdata.json"]

    def test_production_comment_model(self):
        """ Test production comment pass """
        comment = UserComment.objects.create(
                                            production_id=2,
                                            user_id=1,
                                            comment='Comment')
        self.assertTrue(isinstance(comment, UserComment))
        self.assertTrue(comment.comment == 'Comment')

    def test_production_likes_model(self):
        """ Test production likes pass """
        comment = UserLike.objects.create(production_id=1, user_id=1)
        self.assertTrue(isinstance(comment, UserLike))
