from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Author, Comment, Post
from django.forms.models import model_to_dict
from django.core import serializers
from .authenticate import check_authenticate
import datetime
import json

# Create your views here.
def index(request):

    #Testing authentication check via HTTP Basic Auth
    authenticated = check_authenticate(request)

    if(authenticated == None):
        return HttpResponse("Not authenticated")
    else:
        return HttpResponse("Authenticated as user" + authenticated.username)

def create_post(post):
	new_post = Post.objects.create(title=post['title'],
		source=post['source'],
		origin=post['origin'],
		author_id=post['author_id'],
		description=post['description'],
		contentType=post['contentType'],
		content=post['content'],
		categories=post['categories'],
		published=datetime.datetime.now(),
		visibility=post['visibility'])
	return new_post

def create_json_response_with_location(data, id, path):
	json_response = JsonResponse(data)
	json_response['Location'] = path + str(id)
	json_response.status_code = 201
	return json_response

def posts_handler_generic(request):

	if (request.method == 'POST'):
		#TODO: ADD validation
		post = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
		new_post = create_post(post)
		data = model_to_dict(new_post)
		return create_json_response_with_location(data, new_post.id, request.path)

	elif (request.method == 'GET'):
		#TODO: this should return all the posts that a user can see, i.e their stream, not all posts in db
		posts = Post.objects.all()
		serialized_posts = serializers.serialize('json', posts)
		return JsonResponse(serialized_posts, safe=False)

	elif (request.method == 'PUT'):
		#TODO: VALIDATION... again
		body = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
		new_post = create_post(body)
		data = model_to_dict(new_post)
		return create_json_response_with_location(data, new_post.id, request.path)

def posts_handler_specific(request, id):

	if (request.method == 'POST'):
		return HttpResponse(status=405)
	elif (request.method == 'PUT' or request.method == 'PATCH'):
		body = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
		post = Post.objects.get(pk=id)
		for k,v in body.iteritems():
			post[k] = v
		post.save()
		return HttpResponse(status=200)


	elif (request.method == 'GET'):
		#validation to see if they can actually access this post based on its permissions
		post = Post.objects.get(pk=id)
		serialized_post = serializers.serialize('json', [post])
		return JsonResponse(serialized_post, safe=False)
	elif (request.method == 'DELETE'):
		#validation to see if they can actually delete the object, i.e it's their post

		user = check_authenticate(request)
		if(user == None):
			return HttpResponse(status=403)

		author = Author.objects.get(userID=user.id)

		post = Post.objects.get(pk=uuid)

		if(post.author == author):
			post.delete()
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=403)

def author_handler(request):
	if (request.method == 'POST'):
		return
	return HttpResponse("")

def friend_handler(request):
	return HttpResponse("My united states of")
