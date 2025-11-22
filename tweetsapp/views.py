from django.shortcuts import render # for rendering templates
from .models import Tweet # importing Tweet model
from .forms import TweetForm # importing TweetForm
from django.shortcuts import get_object_or_404 # to get object or return 404
from django.shortcuts import redirect # for redirecting after form submission
from django.contrib.auth.decorators import login_required # to ensure user is logged in
from django.contrib.auth import login # for logging in user after registration
from .forms import UserRegistrationForm # importing UserRegistrationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

# tweet listing
def tweet_list(request):
    query = request.GET.get('q') # getting search query from URL parameters
    tweets = Tweet.objects.all().order_by('-created_at')  # ordering by latest
    if query:
        tweets = tweets.filter(text__icontains=query)  # filters tweets whose text contains the search term
    return render(request, 'tweet_list.html', {'tweets': tweets, 'query': query})

# tweet creation
@login_required
def tweet_create(request):
    if request.method == 'POST': # on form submission
        form = TweetForm(request.POST, request.FILES) # by this we are accepting files and POST data
        if form.is_valid(): # for security measures
            tweet = form.save(commit=False) # we are not saving it directly to DB
            tweet.user = request.user  # assuming user is logged in
            tweet.save()  # now we save it to DB
            return redirect('tweet_list') # redirect to tweet list after creation
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form}) # rendering the form

# tweet editing
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user) # get the tweet or return 404, pk means primary key, request.user ensures only owner can edit
    if request.method == 'POST': # on form submission
        form = TweetForm(request.POST, request.FILES, instance=tweet) # bind to existing instance
        if form.is_valid():
            tweet = form.save(commit=False) # we are not saving it directly to DB
            tweet.user = request.user  # assuming user is logged in
            form.save()
            return redirect('tweet_list') # redirect to tweet list after editing
    else:
        form = TweetForm(instance=tweet) # pre-fill form with existing tweet data
    return render(request, 'tweet_form.html', {'form': form}) 

# tweet deletion
@login_required
def tweet_delete(request, tweet_id): 
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user) # get the tweet or return 404
    if request.method == 'POST': # on POST request only
        tweet.delete() # delete the tweet
        return redirect('tweet_list') # redirect to tweet list after deletion
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet}) # render confirmation page

# user registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # we are not saving it directly to DB
            user.set_password(form.cleaned_data['password1']) # hashing the password
            user.save()
            login(request, user) # log the user in after registration
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})