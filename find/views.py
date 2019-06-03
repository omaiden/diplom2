from django.contrib.auth.models import Group, User, Permission
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from . import faceRecog
import os

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def regis(request):
	form = forms.RegistrationForm()
	if request.method == 'POST':
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login')
	return render(request,'regis.html', {'form':form})

def thanks(request):
	return render(request, 'thanks.html')

def post_missing(request):
	if request.method == 'POST':
		form1 = forms.PostForm(request.POST)
		form2 = forms.Missing_personForm(request.POST, request.FILES)
		form3 = forms.RelativeForm(request.POST)
		
		if (form1.is_valid() and form2.is_valid() and form3.is_valid()):
			user_obj = request.user
			post_type_obj = models.Post_type.objects.get(pk=1)
			relative_obj = form3.save()
			post_obj = form1.save(commit=False)
			post_obj.relative = relative_obj
			post_obj.post_type = post_type_obj
			post_obj.user = user_obj
			post_obj.save()
			missing_obj = form2.save(commit=False)
			missing_obj.post = post_obj
			missing_obj.save()
			missing_obj.image = form2.cleaned_data['image']
			missing_obj.save()

			train_path = os.path.join(BASE_DIR, 'images/victim')
			#victim_obj = models.Victim.objects.order_by('-id')[0]
			id_victim = faceRecog.recog(missing_obj.image, train_path)
			if id_missing:
				match = models.Match()
				match.missing_person = missing_obj
				match.victim = models.Victim.objects.get(id=id_victim)
				match.save()

			return HttpResponseRedirect('/thanks')

	else:
		form1 = forms.PostForm(initial = {'text': 'Этот текст будет разместить на странице чтобы другие пользователи могут увидеть.'})
		form2 = forms.Missing_personForm()
		form3 = forms.RelativeForm()
	return render(request,'post_missing.html', {'form1': form1, 'form2': form2, 'form3': form3})


def post_victim(request):
	if request.method == 'POST':
		form1 = forms.PostForm(request.POST)
		form2 = forms.VictimForm(request.POST, request.FILES)
		form3 = forms.RelativeForm(request.POST)

		
		if (form1.is_valid() and form2.is_valid() and form3.is_valid()):
			print(form2.cleaned_data['image'])
			user_obj = request.user
			post_type_obj = models.Post_type.objects.get(pk=2)
			relative_obj = form3.save()
			
			post_obj = form1.save(commit=False)
			post_obj.relative = relative_obj
			post_obj.post_type = post_type_obj
			post_obj.user = user_obj
			post_obj.save()
			
			victim_obj = form2.save(commit=False)
			victim_obj.post = post_obj
			
			# return render(request, "image.html", {"image":form2.cleaned_data['image']})
			victim_obj.save()
			victim_obj.image = form2.cleaned_data['image']
			victim_obj.save()

			train_path = os.path.join(BASE_DIR, 'images/missing')
			#victim_obj = models.Victim.objects.order_by('-id')[0]
			id_missing = faceRecog.recog(victim_obj.image, train_path)
			if id_missing:
				match = models.Match()
				match.missing_person = models.Missing_person.objects.get(id=id_missing)
				match.victim = victim_obj
				match.save()
			return HttpResponseRedirect('/thanks')

	else:
		form1 = forms.PostForm(initial = {'text': 'Этот текст будет разместить на странице чтобы другие пользователи могут увидеть.'})
		form2 = forms.VictimForm()
		form3 = forms.RelativeForm()

	return render(request,'post_victim.html', {'form1': form1, 'form2': form2, 'form3': form3})


class PostList(ListView):
	# model = models.Post

	queryset = models.Post.objects.all().order_by("-time")
	template_name = 'posts.html'
	context_object_name = 'post'
	paginate_by = 10


class PostDetail(DetailView):
	model = models.Post
	template_name = 'mypost.html'


def post_detail(request, pk):
	post = get_object_or_404(models.Post, pk=pk)
	form = forms.CommentForm()
	if request.method == 'POST':
		form = forms.CommentForm(request.POST, user=request.user, post=post)
		if (form.is_valid()):
			form.save()
			return HttpResponseRedirect(request.path)
	return render(request, 'post_detail.html', {'post': post, 'form': form})


class Mypost(ListView):
	template_name = 'posts.html'
	context_object_name = 'post'
	paginate_by = 10
	def get_queryset(self):
		return models.Post.objects.filter(user=self.request.user)


def image(request):
	i = get_object_or_404(models.Missing_person, pk=8)
	return render(request, 'image.html', {'image': i})


def delete_everything(request):
    models.Post.objects.all().delete()
    return render(request,'index.html')


def train(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	train_path = os.path.join(BASE_DIR, 'images/missing')
	victim_obj = models.Victim.objects.order_by('-id')[0]
	id_missing = faceRecog.recog(victim_obj.image, train_path)
	return render(request, 'result.html', {'id':id_missing})