
from blog.models import article, Category


def recent_articles(request):
    articles = article.objects.all().order_by('-created','-updated')[:3]
    return {'recent_posts': articles}

def categories(request):
    categories = Category.objects.all()[:5]
    return {'categories': categories}