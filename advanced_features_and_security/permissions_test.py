"""
Automated permissions testing script.
Run with: python permissions_test.py
"""

import os
import sys
import django

# Add LibraryProject to path - MUST be before Django setup
project_dir = os.path.join(os.path.dirname(__file__), 'LibraryProject')
sys.path.insert(0, project_dir)
os.chdir(project_dir)

# Setup Django BEFORE any imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# NOW import Django and app models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from relationship_app.models import Book, Author, Library  # type: ignore
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

# Import after Django setup
try:
    from bookshelf.models import CustomUser as User  # type: ignore
except ImportError:
    from django.contrib.auth.models import User

class PermissionsTestSuite:
    """Test suite for verifying permissions and groups system."""
    
    def __init__(self):
        self.client = Client()
        self.test_users = {}
        self.test_book = None
        self.passed_tests = 0
        self.failed_tests = 0
        
    def setup_test_data(self):
        """Create test users and data."""
        print("\n" + "=" * 70)
        print("SETTING UP TEST DATA")
        print("=" * 70)
        
        # Create test book
        try:
            self.test_book = Book.objects.first()
            if not self.test_book:
                library = Library.objects.first() or Library.objects.create(name="Test Library")
                author = Author.objects.first() or Author.objects.create(name="Test Author")
                self.test_book = Book.objects.create(
                    title="Test Book",
                    author=author,
                    publication_date="2024-01-01"
                )
            print(f"[OK] Test book created/retrieved: {self.test_book.title}")
        except Exception as e:
            print(f"[ERROR] Failed to create test book: {e}")
        
        # Create test users
        groups = ['Viewers', 'Editors', 'Admins']
        for group_name in groups:
            username = f"test_{group_name.lower()}"
            try:
                user = User.objects.filter(username=username).first()
                if not user:
                    user = User.objects.create_user(
                        username=username,
                        password='testpass123',
                        email=f'{username}@test.com'
                    )
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                    print(f"[CREATED] User: {username} -> Group: {group_name}")
                else:
                    print(f"[EXISTS] User: {username}")
                self.test_users[group_name] = user
            except Exception as e:
                print(f"[ERROR] Failed to create user {username}: {e}")
        
        # Create unauthenticated user (for testing permission checks)
        try:
            unauthenticated = User.objects.filter(username="test_unauthenticated").first()
            if not unauthenticated:
                unauthenticated = User.objects.create_user(
                    username="test_unauthenticated",
                    password='testpass123',
                    email='unauthenticated@test.com'
                )
                print(f"[CREATED] User: test_unauthenticated (no groups)")
            self.test_users['Unauthenticated'] = unauthenticated
        except Exception as e:
            print(f"[ERROR] Failed to create unauthenticated user: {e}")
    
    def test_groups_exist(self):
        """Test that all required groups exist."""
        print("\n" + "=" * 70)
        print("TEST 1: Verify Groups Exist")
        print("=" * 70)
        
        required_groups = ['Viewers', 'Editors', 'Admins']
        for group_name in required_groups:
            try:
                group = Group.objects.get(name=group_name)
                perm_count = group.permissions.count()
                print(f"[PASS] Group '{group_name}' exists with {perm_count} permissions")
                self.passed_tests += 1
            except Group.DoesNotExist:
                print(f"[FAIL] Group '{group_name}' not found")
                self.failed_tests += 1
    
    def test_permissions_assigned_correctly(self):
        """Test that permissions are assigned to groups correctly."""
        print("\n" + "=" * 70)
        print("TEST 2: Verify Permissions Assigned to Groups")
        print("=" * 70)
        
        permission_matrix = {
            'Viewers': ['can_view_book'],
            'Editors': ['can_view_book', 'can_create_book', 'can_edit_book', 'can_manage_authors'],
            'Admins': ['can_view_book', 'can_create_book', 'can_edit_book', 'can_delete_book', 'can_publish_book', 'can_manage_authors']
        }
        
        for group_name, expected_perms in permission_matrix.items():
            try:
                group = Group.objects.get(name=group_name)
                actual_perms = list(group.permissions.values_list('codename', flat=True))
                actual_perms.sort()
                expected_perms.sort()
                
                if actual_perms == expected_perms:
                    print(f"[PASS] {group_name}: All {len(expected_perms)} permissions correct")
                    self.passed_tests += 1
                else:
                    print(f"[FAIL] {group_name}: Permission mismatch")
                    print(f"  Expected: {expected_perms}")
                    print(f"  Got: {actual_perms}")
                    self.failed_tests += 1
            except Exception as e:
                print(f"[FAIL] {group_name}: {e}")
                self.failed_tests += 1
    
    def test_user_permissions_inheritance(self):
        """Test that users inherit permissions through group membership."""
        print("\n" + "=" * 70)
        print("TEST 3: Verify User Permission Inheritance from Groups")
        print("=" * 70)
        
        test_cases = {
            'Viewers': ['relationship_app.can_view_book'],
            'Editors': ['relationship_app.can_view_book', 'relationship_app.can_create_book', 
                       'relationship_app.can_edit_book', 'relationship_app.can_manage_authors'],
            'Admins': ['relationship_app.can_view_book', 'relationship_app.can_create_book',
                      'relationship_app.can_edit_book', 'relationship_app.can_delete_book',
                      'relationship_app.can_publish_book', 'relationship_app.can_manage_authors']
        }
        
        for group_name, expected_perms in test_cases.items():
            user = self.test_users.get(group_name)
            if not user:
                print(f"[SKIP] Test user for {group_name} not found")
                continue
            
            try:
                # Get all permissions for user through groups
                user_perms = Permission.objects.filter(group__user=user).values_list('content_type__app_label', 'codename')
                user_perms = [f"{app}.{perm}" for app, perm in user_perms]
                user_perms = sorted(set(user_perms))
                expected_perms_sorted = sorted(set(expected_perms))
                
                if user_perms == expected_perms_sorted:
                    print(f"[PASS] {group_name} user has correct permissions")
                    self.passed_tests += 1
                else:
                    print(f"[FAIL] {group_name} user permissions mismatch")
                    print(f"  Expected: {expected_perms_sorted}")
                    print(f"  Got: {user_perms}")
                    self.failed_tests += 1
            except Exception as e:
                print(f"[FAIL] {group_name}: {e}")
                self.failed_tests += 1
    
    def test_viewers_access(self):
        """Test Viewers group access (read-only)."""
        print("\n" + "=" * 70)
        print("TEST 4: Verify Viewers Group Access (Read-Only)")
        print("=" * 70)
        
        user = self.test_users.get('Viewers')
        if not user:
            print("[SKIP] Viewers test user not found")
            return
        
        self.client.login(username='test_viewers', password='testpass123')
        
        # Should be able to view books
        try:
            response = self.client.get('/relationship_app/books/')
            if response.status_code == 200:
                print("[PASS] Viewers can access book list (200 OK)")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Viewers got {response.status_code} instead of 200 on book list")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing book list: {e}")
            self.failed_tests += 1
        
        # Should NOT be able to add books
        try:
            response = self.client.get('/relationship_app/books/add/')
            if response.status_code == 403:
                print("[PASS] Viewers cannot access add book (403 Forbidden)")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Viewers got {response.status_code} instead of 403 on add book")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing add book: {e}")
            self.failed_tests += 1
        
        self.client.logout()
    
    def test_editors_access(self):
        """Test Editors group access (create/edit)."""
        print("\n" + "=" * 70)
        print("TEST 5: Verify Editors Group Access (Create/Edit)")
        print("=" * 70)
        
        user = self.test_users.get('Editors')
        if not user:
            print("[SKIP] Editors test user not found")
            return
        
        self.client.login(username='test_editors', password='testpass123')
        
        # Should be able to view books
        try:
            response = self.client.get('/relationship_app/books/')
            if response.status_code == 200:
                print("[PASS] Editors can access book list (200 OK)")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Editors got {response.status_code} on book list")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing book list: {e}")
            self.failed_tests += 1
        
        # Should be able to add books
        try:
            response = self.client.get('/relationship_app/books/add/')
            if response.status_code == 200:
                print("[PASS] Editors can access add book (200 OK)")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Editors got {response.status_code} on add book")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing add book: {e}")
            self.failed_tests += 1
        
        # Should NOT be able to delete books
        if self.test_book:
            try:
                response = self.client.get(f'/relationship_app/books/{self.test_book.id}/delete/')
                if response.status_code == 403:
                    print("[PASS] Editors cannot delete books (403 Forbidden)")
                    self.passed_tests += 1
                else:
                    print(f"[FAIL] Editors got {response.status_code} instead of 403 on delete")
                    self.failed_tests += 1
            except Exception as e:
                print(f"[FAIL] Error accessing delete book: {e}")
                self.failed_tests += 1
        
        self.client.logout()
    
    def test_admins_access(self):
        """Test Admins group access (full permissions)."""
        print("\n" + "=" * 70)
        print("TEST 6: Verify Admins Group Access (Full Permissions)")
        print("=" * 70)
        
        user = self.test_users.get('Admins')
        if not user:
            print("[SKIP] Admins test user not found")
            return
        
        self.client.login(username='test_admins', password='testpass123')
        
        # Should be able to view books
        try:
            response = self.client.get('/relationship_app/books/')
            if response.status_code == 200:
                print("[PASS] Admins can access book list (200 OK)")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Admins got {response.status_code} on book list")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing book list: {e}")
            self.failed_tests += 1
        
        # Should be able to add books
        try:
            response = self.client.get('/relationship_app/books/add/')
            if response.status_code == 200:
                print("[PASS] Admins can access add book (200 OK)")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Admins got {response.status_code} on add book")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing add book: {e}")
            self.failed_tests += 1
        
        # Should be able to delete books
        if self.test_book:
            try:
                response = self.client.get(f'/relationship_app/books/{self.test_book.id}/delete/')
                if response.status_code == 200:
                    print("[PASS] Admins can access delete book (200 OK)")
                    self.passed_tests += 1
                else:
                    print(f"[FAIL] Admins got {response.status_code} on delete book")
                    self.failed_tests += 1
            except Exception as e:
                print(f"[FAIL] Error accessing delete book: {e}")
                self.failed_tests += 1
        
        self.client.logout()
    
    def test_unauthenticated_access(self):
        """Test unauthenticated user access."""
        print("\n" + "=" * 70)
        print("TEST 7: Verify Unauthenticated User Access")
        print("=" * 70)
        
        # Should redirect to login (not return 200)
        try:
            response = self.client.get('/relationship_app/books/')
            if response.status_code in [302, 403]:  # 302 redirect or 403 forbidden
                print(f"[PASS] Unauthenticated user redirected/forbidden (status {response.status_code})")
                self.passed_tests += 1
            else:
                print(f"[FAIL] Unauthenticated user got {response.status_code}, expected redirect")
                self.failed_tests += 1
        except Exception as e:
            print(f"[FAIL] Error accessing book list unauthenticated: {e}")
            self.failed_tests += 1
    
    def run_all_tests(self):
        """Run all permission tests."""
        print("\n\n")
        print("=" * 70)
        print(" " * 15 + "DJANGO PERMISSIONS TESTING SUITE")
        print("=" * 70)
        
        self.setup_test_data()
        self.test_groups_exist()
        self.test_permissions_assigned_correctly()
        self.test_user_permissions_inheritance()
        self.test_viewers_access()
        self.test_editors_access()
        self.test_admins_access()
        self.test_unauthenticated_access()
        
        # Print summary
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests:  {total_tests}")
        print(f"Passed:       {self.passed_tests}")
        print(f"Failed:       {self.failed_tests}")
        print(f"Pass Rate:    {pass_rate:.1f}%")
        print("=" * 70 + "\n")
        
        
        if self.failed_tests == 0:
            print("[PASS] All tests passed! Permissions system is working correctly.\n")
            return True
        else:
            print(f"[FAIL] {self.failed_tests} test(s) failed. Please review the errors above.\n")
            return False


if __name__ == '__main__':
    suite = PermissionsTestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
