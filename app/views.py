from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Blog, Comment
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Subscriber
import io
from openpyxl import Workbook

import re
from django.template.defaultfilters import truncatechars
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def index(request):
    latest_posts = Blog.objects.order_by('-date_created')[:6]
    context = {"posts": latest_posts}
    return render(request, "app/index.html", context)

def custom_page_not_found(request, exception):
    return render(request, 'app/error404.html', status=404)

def custom_server_error(request):
    return render(request, 'app/error500.html', status=500)
def blog(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    comments = post.comments.order_by('-created_at')
    latest = None
    if comments:
        latest = comments[0]
    context = {"blog": post, "comments": comments, "last": latest}
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('comment')
        if not name or not message:
            messages.error(request, 'Name and message are required')
            return render(request, "app/read.html", context)
        new_comment = Comment.objects.create(blog=post, author=name, text=message)
        new_comment.save()
        return redirect(reverse("read", kwargs={'slug':slug}))
    return render(request, "app/read.html", context)
def comment(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('comment')
        if not name or not message:
            return JsonResponse({"status":False, "message": 'Name and message are required'})
        new_comment = Comment.objects.create(blog=post, author=name, text=message)
        new_comment.save()
        comments = post.comments.order_by('-created_at')
        return JsonResponse({"status":True, "comments": comments})
    return redirect(reverse('index'))

def load_more_posts(request):
    blog_posts = Blog.objects.all()
    posts_per_page = 6
    paginator = Paginator(blog_posts, posts_per_page)
    page = request.GET.get('page')
    try:
        page = int(page)
        if page < 1:
            page = paginator.num_pages
    except BaseException:
        pass
    try:
        blog_posts_page = paginator.page(page)
    except PageNotAnInteger:
        blog_posts_page = paginator.page(1)
        page = 1
    except EmptyPage:
        blog_posts_page = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    truncated_posts = []
    for post in blog_posts_page:
        truncated_post = {
            'title': post.title,
            'body': truncatechars(post.body, 82),
            'picture': post.picture.url,
            'slug': post.slug,
        }
        truncated_posts.append(truncated_post)
    return JsonResponse({"status":True, 'blog_posts_page': truncated_posts, 'page':page})

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"status":False, "message": "Email is required"})
        if not is_valid_email(email):
            return JsonResponse({"status":False, "message": "Invalid email format"})
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({"status":False, "message": "You are already a subscriber"})
        new_sub = Subscriber.objects.create(email = email)
        new_sub.save()
        return JsonResponse({"status":True})
    return redirect(reverse('index'))



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def show_client_ip(request):
#     client_ip = get_client_ip(request)
#     return HttpResponse(f"Your IP address is {client_ip}")

def export_subscriber_emails(request):
    # Fetch all subscribers
    subscribers = Subscriber.objects.all()

    # Create a new Excel workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Subscriber Emails'

    # Add headers to the worksheet
    headers = ['Email']
    worksheet.append(headers)

    # Add subscriber emails to the worksheet
    for subscriber in subscribers:
        worksheet.append([subscriber.email])

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=subscriber_emails.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    # Redirect to the index page
    return response