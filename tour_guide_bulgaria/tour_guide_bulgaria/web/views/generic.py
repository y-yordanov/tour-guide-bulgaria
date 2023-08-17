from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render
from django.views import generic as views
from django.core.mail import send_mass_mail
from tour_guide_bulgaria.common.view_mixins import RedirectToDashboard
from tour_guide_bulgaria.settings import EMAIL_HOST_USER
from tour_guide_bulgaria.web.models import Sight, Category


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'common/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class AboutUsView(views.TemplateView):
    template_name = 'common/about_us.html'


def contact_view(request):
    email_user = EMAIL_HOST_USER
    if request.method == 'POST':
        message_subject = request.POST['message_email']
        sender_message = request.POST['sender_message']
        sender_name = request.POST['sender_name']
        sender_email = message_subject

        message1 = (
            message_subject,
            sender_message,
            sender_email,
            [email_user]
        )

        message2 = (
            'Your inquiry',
            'Thank you for your inquiry. We will respond shortly to your message.',
            email_user,
            (sender_email,)
        )

        send_mass_mail((message1, message2), fail_silently=False)

        return render(request, 'common/contact_page.html', {'sender_name': sender_name})
    else:
        return render(request, 'common/contact_page.html')


@login_required(login_url='accounts/login')
def show_dashboard(request):
    category = request.GET.get('category')
    if category == None:
        sights = Sight.objects.order_by('-post_date')
    else:
        sights = Sight.objects.filter(category__name=category)

    categories = Category.objects.all().annotate(posts_count=Count('sight'))
    sights_count_by_category = len(Sight.objects.all())

    page_number = request.GET.get('page')
    paginator = Paginator(sights, 4)

    try:
        sights = paginator.page(page_number)
    except PageNotAnInteger:
        sights = paginator.page(1)
    except EmptyPage:
        sights = paginator.page(paginator.num_pages)

    context = {
        'sights': sights,
        'categories': categories,
        'sights_count_by_category': sights_count_by_category,

    }
    return render(request, 'common/home_with_profile.html', context)