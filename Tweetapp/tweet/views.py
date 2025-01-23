from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

# list tweets
def Tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets':tweets})

# create tweets
def Tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) # do not save it in database
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})

# edit tweets
def Tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=Tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = redirect('tweet_list')
    else:
        form = TweetForm(instance=Tweet)
    return render(request, 'tweet_form.html', {'form':form})

# delete tweets
def Tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})