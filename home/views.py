from blog.models import article
from django.shortcuts import render


def home(request):
  articles = article.objects.all()
  # مرتب‌سازی فقط بر اساس جدیدترین تاریخ ایجاد
  recent_articles = article.objects.order_by("-created")[:3]

  return render(
      request,
      "home/index.html",
      {"articles": articles, "recent_articles": recent_articles},
  )