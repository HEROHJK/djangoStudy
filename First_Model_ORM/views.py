from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from First_Model_ORM.models import Post, Comment
from django.contrib.sessions.models import Session
import json

@csrf_exempt
def SignUp(request):
    try:
        inputId         = request.POST['id']
        inputPassword   = request.POST['password']
        inputEMail      = request.POST['email']

        print('여기까지 진입함')

        user = User.objects.create_user(
            username    = inputId,
            email       = inputEMail,
            password    = inputPassword
        )
        user.save()

        message = 'success'

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

@csrf_exempt
def SignIn(request):
    try:
        inputID = request.POST['id']
        inputPassword = request.POST['password']
        user = authenticate(username = inputID, password = inputPassword)

        if user != None:
            login(request,user)
            message = 'success'
        else:
            message = 'failed'

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

@csrf_exempt
def SignOut(request):
    user = request.user

    print(user)

    [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]

    return HttpResponse('success')

@csrf_exempt
def Write(request):
    try:
        inputTitle = request.POST['title']
        inputText = request.POST['text']
        id = request.user

        post = Post.objects.create(
            writer=id,
            title=inputTitle,
            text=inputText
        )
        post.save()

        postIndex = Post.objects.order_by('-id').first().id
        message = 'success : ' + str(postIndex)

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

@csrf_exempt
def WriteComment(request):
    try:
        inputPostId     = request.POST['postid']
        inputText       = request.POST['text']

        comment = Comment.objects.create(
            writer      = request.user,
            text        = inputText,
            postIndex   = Post.objects.filter(id=inputPostId).first()
        )

        comment.save()

        message = 'success'
    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

def GetPosts(request):
    try:
        inputPostId = request.GET.get('postid')

        if inputPostId != None :
            post = Post.objects.filter(id=inputPostId).first()
            postJson = []
            comments = Comment.objects.filter(postIndex_id=inputPostId)
            commentList = []
            for comment in comments:
                commentList.append({
                    'writer' : str(comment.writer),
                    'text' : comment.text,
                    'date' : str(comment.date)
                })
            postJson.append({
                'index' : inputPostId,
                'writer' : str(post.writer),
                'title' : post.title,
                'text' : post.text,
                'date' : str(post.date),
                'comments' : commentList
            })

            message = json.dumps(postJson, ensure_ascii=False)

        else :
            posts = Post.objects.order_by('-id').all()

            postList = []

            for post in posts:
                postList.append({
                    'index' : str(post.id),
                    'title' : post.title
                })

            message = json.dumps(postList, ensure_ascii=False)

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)