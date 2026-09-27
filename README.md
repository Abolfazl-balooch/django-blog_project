# پروژه بلاگ با Django

یک پروژه وبلاگ (Blog) کامل ساخته‌شده با فریم‌ورک **Django**، شامل سیستم احراز هویت کاربران، مدیریت مقالات، دسته‌بندی، نظرات، جستجو، سیستم لایک و پنل مدیریت سفارشی‌سازی‌شده.

## ✨ امکانات

### احراز هویت کاربر
- ثبت‌نام (Register)
- ورود (Login)
- خروج (Logout)
- ویرایش اطلاعات پروفایل کاربر

### مقالات
- مدل مقالات با روابط `ForeignKey`، `ManyToMany` و `OneToOne`
- دسته‌بندی مقالات (Categories)
- پروفایل کاربر مرتبط با مقالات
- صفحه جزئیات مقاله با URL اختصاصی (`slug` و `get_absolute_url`)
- نمایش لیست مقالات و صفحه‌بندی (Pagination)
- نمایش «مقالات اخیر»
- اشتراک‌گذاری مقالات در شبکه‌های اجتماعی

### نظرات (Comments)
- ثبت نظر برای مقالات
- پاسخ به نظرات (Nested comments)

### جستجو
- امکان جستجوی ساده در میان مقالات

### سیستم لایک
- لایک/آنلایک مقالات با استفاده از **AJAX** (بدون رفرش صفحه)

### فرم‌ها
- فرم‌های سفارشی و ModelForm
- نمایش خطاهای اعتبارسنجی (Validation Errors)
- استفاده از `django-widget-tweaks` برای طراحی بهتر فرم‌ها

### Class-Based Views
- استفاده از `TemplateView`، `ListView`، `DetailView`، `FormView`، `CreateView`، `UpdateView`، `DeleteView` و `RedirectView`
- استفاده از Mixin ها برای افزودن قابلیت‌های مشترک

### پنل مدیریت (Admin)
- سفارشی‌سازی کامل پنل مدیریت جنگو

### سایر قابلیت‌ها
- Context Processors برای داده‌های مشترک در تمام قالب‌ها
- Template Tags و Template Filters سفارشی (`simple tag`, `inclusion tag`)
- ارث‌بری در قالب‌ها (Template Inheritance)
- استفاده از `django-cleanup` برای پاک‌سازی خودکار فایل‌های آپلودی

## 🛠 تکنولوژی‌ها

- Python
- Django
- HTML / CSS / JavaScript (AJAX)
- django-widget-tweaks
- django-cleanup

## ⚙️ نصب و راه‌اندازی

```bash
# کلون کردن پروژه
git clone <آدرس-ریپازیتوری>
cd <نام-پوشه-پروژه>

# ساخت محیط مجازی
python -m venv venv
source venv/bin/activate    # در ویندوز: venv\Scripts\activate

# نصب پکیج‌ها
pip install -r requirements.txt

# اجرای مایگریشن‌ها
python manage.py migrate

# ساخت سوپریوزر برای دسترسی به پنل ادمین
python manage.py createsuperuser

# اجرای سرور توسعه
python manage.py runserver
```

سپس پروژه در آدرس زیر در دسترس خواهد بود:

```
http://127.0.0.1:8000/
```

پنل مدیریت نیز در آدرس زیر:

```
http://127.0.0.1:8000/admin/
```

## 📁 ساختار پروژه (نمونه)

```
├── .venv/                  # محیط مجازی پایتون
├── account/                # اپلیکیشن احراز هویت و پروفایل کاربر
├── blog/                   # اپلیکیشن اصلی مقالات، دسته‌بندی و نظرات
├── context_processors/     # کانتکست پروسسورهای سفارشی پروژه
├── home/                   # اپلیکیشن صفحه‌ی اصلی
├── media/                  # فایل‌های آپلودی کاربران
├── standblog1/              # پوشه تنظیمات اصلی پروژه (settings, urls, wsgi)
├── static/                 # فایل‌های استاتیک (CSS, JS)
├── templates/               # قالب‌های HTML
└── manage.py
```

## 📄 مجوز (License)

این پروژه صرفاً برای اهداف آموزشی ساخته شده است.
