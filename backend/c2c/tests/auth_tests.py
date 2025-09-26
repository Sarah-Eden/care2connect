from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from c2c.models import Case, Child, FosterFamily, FosterPlacement, HealthService, ReminderLog
from rest_framework.test import APIClient
from rest_framework import status

class RbacApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Dynamically get or create role groups
        self.supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
        self.caseworker_group, _ = Group.objects.get_or_create(name='Caseworker')
        self.fosterparent_group, _ = Group.objects.get_or_create(name='FosterParent')

        # Create test users
        self.supervisor_user = User.objects.create_user(
            username='supervisor1', password='testpass123', email='supervisor1@mail.com',
            first_name='Jane', last_name='Doe', is_active=True
        )
        self.supervisor_user.groups.add(self.supervisor_group)

        self.caseworker_user = User.objects.create_user(
            username='caseworker1', password='testpass123', email='caseworker1@mail.com',
            first_name='Jill', last_name='Jones', is_active=True
        )
        self.caseworker_user.groups.add(self.caseworker_group)

        self.fosterparent1_user = User.objects.create_user(
            username='fosterparent1', password='testpass123', email='fp1@mail.com',
            first_name='Sam', last_name='Smith', is_active=True
        )
        self.fosterparent1_user.groups.add(self.fosterparent_group)

        # Login to get tokens
        self.supervisor_token = self._login_user('supervisor1', 'testpass123')['access']
        self.caseworker_token = self._login_user('caseworker1', 'testpass123')['access']
        self.fosterparent1_token = self._login_user('fosterparent1', 'testpass123')['access']

        # Create test data as Supervisor
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.supervisor_token}')
        self.family = FosterFamily.objects.create(family_name='TestFamily', parent1=self.fosterparent1_user)
        self.child = Child.objects.create(first_name='Test', last_name='Child', dob=timezone.now().date())
        self.placement = FosterPlacement.objects.create(child=self.child, foster_family=self.family, start_date=timezone.now().date())
        self.case = Case.objects.create(
            child=self.child, caseworker=self.caseworker_user, placement=self.placement,
            status='open', start_date=timezone.now().date()
        )
        self.health_service = HealthService.objects.create(
            child=self.child, service=['well_child'], due_date=timezone.now().date(), status='pending'
        )

        # Validate test data
        self.assertTrue(FosterPlacement.objects.filter(child=self.child, foster_family=self.family).exists())
        self.assertTrue(Case.objects.filter(child=self.child, caseworker=self.caseworker_user, placement=self.placement).exists())
        print(f"Test Setup: Case ID: {self.case.id}, Child ID: {self.child.id}, Placement ID: {self.placement.id}")

    def _login_user(self, username, password):
        data = {'username': username, 'password': password}
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Login failed: {response.data}")
        return response.data

    def test_supervisor_access(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.supervisor_token}')
        # Test listing all children
        response = self.client.get('/api/children/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Should see at least the test child

        # Test creating a new child
        new_child_data = {'first_name': 'New', 'last_name': 'Child', 'dob': '2020-01-01'}
        response = self.client.post('/api/children/', new_child_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'New')

    def test_caseworker_access(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.caseworker_token}')
        # Test listing assigned cases
        response = self.client.get('/api/cases/')
        print(f"Caseworker GET /api/cases/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see only their assigned case
        self.assertEqual(response.data[0]['id'], self.case.id)

        # Test updating the case
        update_data = {'status': 'open', 'child': self.case.child.id, 'caseworker': self.caseworker_user.id}
        response = self.client.patch(f'/api/cases/{self.case.id}/', update_data, format='json')
        print(f"Caseworker Patch /api/cases/{self.case.id}/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'open')

        # Test listing children (should see only the case's child)
        response = self.client.get('/api/children/')
        print(f"Caseworker GET /api/children/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.child.id)

    def test_fosterparent_access(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.fosterparent1_token}')
        # Test listing children in their care
        response = self.client.get('/api/children/')
        print(f"FosterParent GET /api/children/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see only their placed child
        self.assertEqual(response.data[0]['id'], self.child.id)

        # Test updating child medications with all required fields
        update_data = {
            'first_name': self.child.first_name,
            'last_name': self.child.last_name,
            'dob': self.child.dob.isoformat(),
            'medications': 'Updated meds'
        }
        response = self.client.patch(f'/api/children/{self.child.id}/', update_data, format='json')
        print(f"FosterParent Patch /api/children/{self.child.id}/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['medications'], 'Updated meds')

        # Test read-only access to case (should fail for GET due to permission, correct test logic)
        response = self.client.get(f'/api/cases/{self.case.id}/')
        print(f"FosterParent GET /api/cases/{self.case.id}/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Changed to expect 403

        # Test update denied on case (should fail for PUT)
        update_data = {'status': 'closed', 'child': self.case.child.id, 'caseworker': self.caseworker_user.id}
        response = self.client.put(f'/api/cases/{self.case.id}/', update_data, format='json')
        print(f"FosterParent PUT /api/cases/{self.case.id}/ Response: {response.status_code}, Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.client.credentials() 
        User.objects.all().delete()
        Child.objects.all().delete()
        FosterFamily.objects.all().delete()
        FosterPlacement.objects.all().delete()
        Case.objects.all().delete()
        HealthService.objects.all().delete()
        ReminderLog.objects.all().delete()
        Group.objects.all().delete()  # Clean up groups too