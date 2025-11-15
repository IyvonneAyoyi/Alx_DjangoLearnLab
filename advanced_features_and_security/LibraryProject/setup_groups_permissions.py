"""
Script to set up groups and permissions for the library application.
Run this with: python manage.py shell < setup_groups_permissions.py

Or from Python:
from django.core.management import call_command
exec(open('setup_groups_permissions.py').read())
"""

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

def setup_groups_and_permissions():
    """
    Create groups and assign permissions to them.
    
    Groups to create:
    - Viewers: Can view books (read-only access)
    - Editors: Can create and edit books
    - Admins: Full permissions including delete
    """
    
    print("Setting up groups and permissions...")
    
    # Get all Book permissions
    content_type = ContentType.objects.get_for_model(Book)
    
    # Get specific permissions
    can_view = Permission.objects.get(codename='can_view_book', content_type=content_type)
    can_create = Permission.objects.get(codename='can_create_book', content_type=content_type)
    can_edit = Permission.objects.get(codename='can_edit_book', content_type=content_type)
    can_delete = Permission.objects.get(codename='can_delete_book', content_type=content_type)
    can_publish = Permission.objects.get(codename='can_publish_book', content_type=content_type)
    can_manage_authors = Permission.objects.get(codename='can_manage_authors', content_type=content_type)
    
    # Create Viewers group (read-only access)
    viewers_group, created = Group.objects.get_or_create(name='Viewers')
    viewers_group.permissions.set([can_view])
    print(f"[{'CREATED' if created else 'EXISTS'}] Group: Viewers - Permissions: can_view_book")
    
    # Create Editors group (create and edit access)
    editors_group, created = Group.objects.get_or_create(name='Editors')
    editors_group.permissions.set([can_view, can_create, can_edit, can_manage_authors])
    print(f"[{'CREATED' if created else 'EXISTS'}] Group: Editors - Permissions: can_view_book, can_create_book, can_edit_book, can_manage_authors")
    
    # Create Admins group (full access)
    admins_group, created = Group.objects.get_or_create(name='Admins')
    admins_group.permissions.set([can_view, can_create, can_edit, can_delete, can_publish, can_manage_authors])
    print(f"[{'CREATED' if created else 'EXISTS'}] Group: Admins - Permissions: All permissions")
    
    print("\nGroups and permissions setup complete!")
    print("\nPermission Summary:")
    print("=" * 60)
    print("Viewers Group:")
    print("  - can_view_book: View/list books")
    print("\nEditors Group:")
    print("  - can_view_book: View/list books")
    print("  - can_create_book: Create new books")
    print("  - can_edit_book: Edit existing books")
    print("  - can_manage_authors: Manage authors")
    print("\nAdmins Group:")
    print("  - can_view_book: View/list books")
    print("  - can_create_book: Create new books")
    print("  - can_edit_book: Edit existing books")
    print("  - can_delete_book: Delete books")
    print("  - can_publish_book: Publish books")
    print("  - can_manage_authors: Manage authors")
    print("=" * 60)
    
    return viewers_group, editors_group, admins_group


def assign_user_to_group(username, group_name):
    """
    Assign a user to a group.
    
    Args:
        username: Username of the user
        group_name: Name of the group ('Viewers', 'Editors', 'Admins')
    """
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        print(f"User '{username}' added to group '{group_name}'")
        return True
    except User.DoesNotExist:
        print(f"Error: User '{username}' does not exist")
        return False
    except Group.DoesNotExist:
        print(f"Error: Group '{group_name}' does not exist")
        return False


def remove_user_from_group(username, group_name):
    """
    Remove a user from a group.
    
    Args:
        username: Username of the user
        group_name: Name of the group
    """
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        user.groups.remove(group)
        print(f"User '{username}' removed from group '{group_name}'")
        return True
    except User.DoesNotExist:
        print(f"Error: User '{username}' does not exist")
        return False
    except Group.DoesNotExist:
        print(f"Error: Group '{group_name}' does not exist")
        return False


def list_user_permissions(username):
    """
    List all permissions for a specific user.
    
    Args:
        username: Username of the user
    """
    try:
        user = User.objects.get(username=username)
        print(f"\nPermissions for user '{username}':")
        print("=" * 60)
        
        # Get permissions from groups
        group_permissions = Permission.objects.filter(group__user=user).distinct()
        
        # Get direct permissions
        direct_permissions = user.user_permissions.all()
        
        all_permissions = (group_permissions | direct_permissions).distinct()
        
        if all_permissions:
            for perm in all_permissions:
                print(f"  - {perm.content_type.app_label}.{perm.codename}: {perm.name}")
        else:
            print("  No permissions assigned")
        
        print("=" * 60)
        return all_permissions
    except User.DoesNotExist:
        print(f"Error: User '{username}' does not exist")
        return None


def list_all_groups():
    """List all groups and their permissions."""
    groups = Group.objects.all()
    print("\nAll Groups and Permissions:")
    print("=" * 60)
    
    for group in groups:
        print(f"\nGroup: {group.name}")
        perms = group.permissions.all()
        if perms:
            for perm in perms:
                print(f"  - {perm.content_type.app_label}.{perm.codename}: {perm.name}")
        else:
            print("  No permissions assigned")
    
    print("=" * 60)


# Run setup when script is executed
if __name__ == '__main__':
    setup_groups_and_permissions()
    list_all_groups()

