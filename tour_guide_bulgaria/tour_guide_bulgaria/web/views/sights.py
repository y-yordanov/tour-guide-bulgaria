from django.contrib.auth import get_user_model
from django.contrib.auth import mixins as auth_mixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from tour_guide_bulgaria.web.forms import AddSightForm, EditSightForm, SightCommentForm
from tour_guide_bulgaria.web.models import Sight, Category, SightLike, SightComment

UserModel = get_user_model()

@login_required(login_url='accounts/login')
def user_sights_view(request):
    category = request.GET.get('category')
    current_user = request.user

    if category == None:
        user_sights = Sight.objects\
            .filter(user_id=current_user.id)\
            .order_by('-post_date')
    else:
        user_sights = Sight.objects.filter(user_id=current_user.id, category__name=category)

    user_categories_count = len(Sight.objects.filter(user_id=current_user.id))
    categories = Category.objects.filter(sight__user=current_user).annotate(posts_count=Count('sight'))

    page_number = request.GET.get('page')
    paginator = Paginator(user_sights, 4)

    try:
        user_sights = paginator.page(page_number)
    except PageNotAnInteger:
        user_sights = paginator.page(1)
    except EmptyPage:
        user_sights = paginator.page(paginator.num_pages)

    context = {
        'user_sights': user_sights,
        'categories': categories,
        'user_categories_count': user_categories_count,
    }

    return render(request, 'accounts/../../templates/sights/user_sights.html', context)


class AddSightView(auth_mixin.LoginRequiredMixin, views.CreateView):
    model = Sight
    form_class = AddSightForm
    template_name = 'sights/add_sight.html'
    success_url = reverse_lazy('show dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@login_required(login_url='accounts/login')
def like_sight(request, pk):
    user_liked_sight = SightLike.objects \
        .filter(sight_id=pk, user_id=request.user.pk)

    if user_liked_sight:
        user_liked_sight.delete()
    else:
        SightLike.objects.create(
            sight_id=pk,
            user_id=request.user.pk,
        )

    return redirect('sight details', pk)


@login_required(login_url='accounts/login')
def sight_details(request, pk):
    print("the correct view is being called")
    sight = Sight.objects.get(pk=pk)
    # comments = SightComment.objects.filter(sight=sight)
    comments = sight.sight_comments.all()
    user_like_sights = Sight.objects.filter(pk=pk, user_id=request.user.pk)
    user = request.user
    form = SightCommentForm(instance=sight)
    if request.method == 'POST':
        form = SightCommentForm(request.POST, instance=sight)

        if form.is_valid():
            print("this form is valid")
            body = form.cleaned_data['body']
            c = SightComment(sight=sight, body=body, user=user)
            c.save()

            return redirect('sight details', pk)
        else:
            print("Invalid Form")
            print("errors : {}".format(form.errors))
    else:
        form = SightCommentForm()

    context = {
            'is_owner': sight.user_id == request.user.id,
            'sight_author': sight.user,
            'sight': sight,
            'has_user_liked_sight': user_like_sights,
            'likes_count': sight.sightlike_set.count(),
            'form': form,
            'comments': comments,
            'comments_count': sight.sight_comments.count(),
        }

    return render(request, 'sights/sight_details.html', context)


class EditSightView(auth_mixin.LoginRequiredMixin, auth_mixin.UserPassesTestMixin, views.UpdateView):
    model = Sight
    form_class = EditSightForm
    template_name = 'sights/edit_sight.html'

    def get_success_url(self):
        return reverse_lazy('sight details', kwargs={'pk': self.object.id})

    def test_func(self):
        sight = get_object_or_404(Sight, pk=self.kwargs["pk"])
        return self.request.user == sight.user


class DeleteSightView(auth_mixin.LoginRequiredMixin, auth_mixin.UserPassesTestMixin, views.DeleteView):
    model = Sight
    template_name = 'sights/delete_sight.html'
    success_url = reverse_lazy('show dashboard')

    def test_func(self):
        sight = get_object_or_404(Sight, pk=self.kwargs["pk"])
        return self.request.user == sight.user








