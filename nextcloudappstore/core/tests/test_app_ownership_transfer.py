from django.contrib.auth.models import User
from django.test import TestCase
from nextcloudappstore.core.models import App, AppOwnershipTransfer


class AppOwnershipTransferTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.user2 = User.objects.create_user(username='user2')
        self.app = App.objects.create(name='App', owner=self.user1)

    def test_transfer(self):
        transfer = AppOwnershipTransfer.objects.create(
            app=self.app, new_owner=self.user2)
        self.assertEquals(transfer.old_owner, self.user1)
        transfer.commit()
        self.assertEquals(self.app.owner, self.user2)
        self.assertEquals(transfer.id, None)

    def test_transfer_to_self(self):
        with self.assertRaises(RuntimeError):
            AppOwnershipTransfer.objects.create(
                app=self.app, new_owner=self.user1)
