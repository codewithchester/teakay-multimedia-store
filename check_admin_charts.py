import os
import sys
import django
from pathlib import Path

# Set up Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeAlpha_Ecommerce.settings')
django.setup()

from django.conf import settings
from django.contrib.admin import site
from django.apps import apps

def check_admincharts():
    """Check if admincharts is properly installed and configured"""
    
    print("\n" + "="*60)
    print("🔍 ADMINCHARTS DIAGNOSTIC CHECK")
    print("="*60)
    
    # 1. Check if package is installed
    print("\n📦 1. Checking admincharts installation...")
    try:
        import admincharts
        print("   ✅ admincharts is installed")
        print(f"   📍 Location: {admincharts.__file__}")
        print(f"   📌 Version: {getattr(admincharts, '__version__', 'Unknown')}")
    except ImportError:
        print("   ❌ admincharts is NOT installed!")
        print("   💡 Run: pip install django-admincharts")
        return
    
    # 2. Check if it's in INSTALLED_APPS
    print("\n📋 2. Checking INSTALLED_APPS...")
    if 'admincharts' in settings.INSTALLED_APPS:
        print("   ✅ admincharts is in INSTALLED_APPS")
    else:
        print("   ❌ admincharts is NOT in INSTALLED_APPS!")
        print("   💡 Add 'admincharts' to INSTALLED_APPS BEFORE 'django.contrib.admin'")
    
    # 3. Check order in INSTALLED_APPS
    print("\n📋 3. Checking installation order...")
    apps_list = settings.INSTALLED_APPS
    admin_index = apps_list.index('django.contrib.admin') if 'django.contrib.admin' in apps_list else -1
    charts_index = apps_list.index('admincharts') if 'admincharts' in apps_list else -1
    
    if charts_index >= 0 and admin_index >= 0:
        if charts_index < admin_index:
            print(f"   ✅ admincharts is BEFORE django.contrib.admin (Position: {charts_index})")
        else:
            print(f"   ❌ admincharts is AFTER django.contrib.admin (Position: {charts_index})")
            print("   💡 Move 'admincharts' BEFORE 'django.contrib.admin'")
    
    # 4. Check static files configuration
    print("\n📂 4. Checking static files configuration...")
    if hasattr(settings, 'STATIC_ROOT'):
        print(f"   ✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    else:
        print("   ❌ STATIC_ROOT is NOT set!")
        print("   💡 Add: STATIC_ROOT = BASE_DIR / 'staticfiles'")
    
    if hasattr(settings, 'STATIC_URL'):
        print(f"   ✅ STATIC_URL: {settings.STATIC_URL}")
    
    # 5. Check if Order model is registered with AdminChartMixin
    print("\n📝 5. Checking Order admin registration...")
    try:
        from store.models import Order
        from store.admin import OrderAdmin
        
        # Check if OrderAdmin uses AdminChartMixin
        from admincharts.admin import AdminChartMixin
        if issubclass(OrderAdmin, AdminChartMixin):
            print("   ✅ OrderAdmin uses AdminChartMixin")
        else:
            print("   ❌ OrderAdmin does NOT use AdminChartMixin")
            print("   💡 Make sure OrderAdmin inherits from AdminChartMixin")
            print("   💡 Example: class OrderAdmin(AdminChartMixin, admin.ModelAdmin):")
    except ImportError:
        print("   ❌ Could not import OrderAdmin")
        print("   💡 Check your store/admin.py file")
    except Exception as e:
        print(f"   ❌ Error checking OrderAdmin: {e}")
    
    # 6. Check if orders exist in database
    print("\n📊 6. Checking database for orders...")
    try:
        from store.models import Order
        order_count = Order.objects.count()
        if order_count > 0:
            print(f"   ✅ Found {order_count} orders in database")
            
            # Show order distribution by month
            from datetime import datetime
            months = {}
            for order in Order.objects.all():
                month_key = order.created_at.strftime('%b %Y')
                months[month_key] = months.get(month_key, 0) + 1
            
            if months:
                print("   📈 Order distribution:")
                for month, count in sorted(months.items()):
                    print(f"      - {month}: {count} order(s)")
        else:
            print("   ⚠️ No orders found in database!")
            print("   💡 Add some test orders to see the chart")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    # 7. Check static directory structure
    print("\n📁 7. Checking static directory...")
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root:
        try:
            import os
            if os.path.exists(static_root):
                print(f"   ✅ STATIC_ROOT exists at: {static_root}")
                
                # Check if admincharts has static files
                charts_static = os.path.join(static_root, 'admincharts')
                if os.path.exists(charts_static):
                    print(f"   ✅ admincharts static files found")
                    print(f"      📁 {charts_static}")
                else:
                    print("   ⚠️ admincharts static files NOT found in STATIC_ROOT")
                    print("   💡 Run: python manage.py collectstatic")
            else:
                print(f"   ⚠️ STATIC_ROOT does NOT exist at: {static_root}")
                print(f"   💡 Run: python manage.py collectstatic")
        except Exception as e:
            print(f"   ❌ Error checking static: {e}")
    
    # 8. Check Jazzmin configuration
    print("\n🎨 8. Checking Jazzmin...")
    if 'jazzmin' in settings.INSTALLED_APPS:
        print("   ✅ Jazzmin is installed")
        if hasattr(settings, 'JAZZMIN_SETTINGS'):
            print("   ✅ Jazzmin settings are configured")
        else:
            print("   ⚠️ No custom Jazzmin settings found")
    else:
        print("   ⚠️ Jazzmin is NOT installed (optional)")
    
    # Summary
    print("\n" + "="*60)
    print("📋 SUMMARY")
    print("="*60)
    
    # Collect all issues
    issues = []
    if 'admincharts' not in settings.INSTALLED_APPS:
        issues.append("❌ admincharts not in INSTALLED_APPS")
    
    if charts_index > admin_index and charts_index >= 0:
        issues.append("❌ admincharts must be BEFORE django.contrib.admin")
    
    if not hasattr(settings, 'STATIC_ROOT'):
        issues.append("❌ STATIC_ROOT not set")
    
    try:
        from store.admin import OrderAdmin
        from admincharts.admin import AdminChartMixin
        if not issubclass(OrderAdmin, AdminChartMixin):
            issues.append("❌ OrderAdmin doesn't use AdminChartMixin")
    except:
        issues.append("❌ OrderAdmin not properly configured")
    
    if issues:
        print("\n🔧 Issues Found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ All checks passed!")
        print("   If chart still doesn't show, try:")
        print("   1. python manage.py collectstatic --noinput")
        print("   2. python manage.py runserver")
        print("   3. Go to: http://127.0.0.1:8000/admin/store/order/")
        print("   4. Check browser console for errors (F12)")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_admincharts()