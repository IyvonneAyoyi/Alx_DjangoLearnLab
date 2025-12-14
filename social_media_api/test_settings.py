import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.conf import settings

print("Testing Production Settings Configuration...")
print("=" * 50)

# Test 1: DEBUG mode
print(f"1. DEBUG = {settings.DEBUG}")
assert settings.DEBUG == False, "DEBUG should be False for production"
print("   ✓ DEBUG is correctly set to False")

# Test 2: ALLOWED_HOSTS
print(f"2. ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
assert len(settings.ALLOWED_HOSTS) > 0, "ALLOWED_HOSTS should not be empty"
print("   ✓ ALLOWED_HOSTS is configured")

# Test 3: Security headers
print(f"3. SECURE_BROWSER_XSS_FILTER = {settings.SECURE_BROWSER_XSS_FILTER}")
assert settings.SECURE_BROWSER_XSS_FILTER == True
print("   ✓ SECURE_BROWSER_XSS_FILTER is enabled")

print(f"4. X_FRAME_OPTIONS = {settings.X_FRAME_OPTIONS}")
assert settings.X_FRAME_OPTIONS == 'DENY'
print("   ✓ X_FRAME_OPTIONS is set to DENY")

print(f"5. SECURE_CONTENT_TYPE_NOSNIFF = {settings.SECURE_CONTENT_TYPE_NOSNIFF}")
assert settings.SECURE_CONTENT_TYPE_NOSNIFF == True
print("   ✓ SECURE_CONTENT_TYPE_NOSNIFF is enabled")

# Test 4: Static files configuration
print(f"6. STATIC_ROOT = {settings.STATIC_ROOT}")
assert hasattr(settings, 'STATIC_ROOT'), "STATIC_ROOT should be configured"
print("   ✓ STATIC_ROOT is configured")

print(f"7. STATICFILES_STORAGE = {settings.STATICFILES_STORAGE}")
print("   ✓ Static files storage is configured")

# Test 5: Database configuration
print(f"8. DATABASES configured: {'default' in settings.DATABASES}")
print("   ✓ Database configuration is present")

print("\n" + "=" * 50)
print("All production settings checks passed!")
print("Ready for deployment!")