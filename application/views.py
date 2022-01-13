from django.contrib.messages.api import warning
from django.shortcuts import render
from .models import User,Post,FndF,Comment,Like,Message,online
from django.forms import ModelForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
import random

# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def logout(request):
    user=User.objects.get(userid=request.session['userid'])
    user.logintime=timezone.now()
    user.save()
    for each in online.objects.all():
        if(each.userid==user.userid):
            each.delete()
    del request.session['name']
    del request.session['userid']
    return render(request,'homepage.html')

def myfun(e):
    return e.datetime

def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        cpassword=request.POST.get('pass')
        if(username=='' or cpassword==''):
            messages.warning(request,f'Fields Cannot be Empty, Please Try Again!')
            return render(request,'signin.html')
        obj=User.objects.all()
        for each in obj:
            if(each.userid==username and each.password==cpassword):
                request.session['userid']=each.userid
                request.session['name']=each.name
                each.logintime=timezone.now()
                each.save()
                allfollowers=FndF.objects.filter(fuserid=username)
                allpost=Post.objects.all()
                online(userid=username).save()
                post=[]
                for each1 in allpost:
                    for every in allfollowers:
                        if(each1.userid==every.tuserid):
                            post.append(each1)
                if(len(post)==0):      
                    messages.warning(request,f'Nothing to show, Please Add some friends!')
                like=[]
                for each1 in Like.objects.all():
                    if(each1.userid==username):
                        like.append(each1.postid)
                post.sort(reverse=True,key=myfun)
                return render(request,'userhome.html',{'name':each.name,'userid':each.userid,'posts':post,'alluser':obj,'comment':Comment.objects.all(),'like':like}) 
        messages.warning(request,f'No Matching User Found, Please Try Again!')        
        return render(request,'signin.html')
    return render(request,'signin.html')

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['name','profilepic','userid','password','emailid']

def signup(request):
    if request.method=="POST":
        curname=request.POST.get('name')
        curmail=request.POST.get('emailid')
        curusername=request.POST.get('userid')
        curpass=request.POST.get('password')
        currepass=request.POST.get('repass')
        if(curname=='' or curmail=='' or curusername=='' or curpass=='' or currepass==''):
            messages.warning(request,f'Fields Cannot be Empty, Please Try Again!')
            return render(request,'signup.html')
        if(curpass != currepass):
            messages.warning(request,f'Passwords Donot Match, Please Try Again!')
            return render(request,'signup.html')
        obj=User.objects.all()
        for each in obj:
            if(each.userid==curusername):
                messages.warning(request,f'Duplicate Username Found, Please Try Again with another Username!')
                return render(request,'signup.html')
        form=UserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        messages.success(request,f'Registration Successful, Please Log In to continue!')
        return render(request,'signin.html')
    return render(request,'signup.html')

def forgotpass(request):
    if request.method=="POST":
        curmail=request.POST.get('emailid')
        curusername=request.POST.get('userid')
        curpass=request.POST.get('password')
        currepass=request.POST.get('repass')
        if(curmail=='' or curusername=='' or curpass=='' or currepass==''):
            messages.warning(request,f'Fields Cannot be Empty, Please Try Again!')
            return render(request,'forgotpass.html')
        if(curpass != currepass):
            messages.warning(request,f'Passwords Donot Match, Please Try Again!')
            return render(request,'forgotpass.html')
        obj=User.objects.all()
        for each in obj:
            if(each.userid==curusername and each.emailid==curmail):
                each.password=curpass
                each.save()
                messages.success(request,f'Password Updated Successfully!')
                return render(request,'signin.html')
        messages.warning(request,f'No Matching User Found, Please Try Again!')
        return render(request,'forgotpass.html')
    return render(request,'forgotpass.html')

def feed(request):
    obj=User.objects.all()
    userid=request.session.get('userid')
    name=request.session.get('name')
    allfollowers=FndF.objects.filter(fuserid=userid)
    allpost=Post.objects.all()
    post=[]
    for each in allpost:
        for every in allfollowers:
            if(each.userid==every.tuserid):
                post.append(each)
    if(len(post)==0):      
        messages.warning(request,f'Nothing to show, Please Add some friends!')
    like=[]
    for each in Like.objects.all():
        if(each.userid==userid):
            like.append(each.postid)
    post.sort(reverse=True,key=myfun) 
    return render(request,'userhome.html',{'userid':userid,'name':name,'posts':post,'alluser':obj,'comment':Comment.objects.all(),'like':like})

def search(request):
    if request.method=="POST":
        userid=request.POST.get('userid')
        if(userid==''):
            messages.warning(request,f'Field cannot be empty!')
            return feed(request)
        obj=User.objects.all()
        curuserid=request.session.get('userid')
        curname=request.session.get('name')
        list1=[]
        for each in obj:
            if(each.userid==userid and each.userid!=curuserid):
                list1.append(each)
        if(len(list1)==0):
            messages.warning(request,f'No Matching User Found, Please Try Again!')
            return feed(request)
        userposts=[]
        for each in Post.objects.all():
            if(each.userid==list1[0].userid):
                userposts.append(each)
        followers=FndF.objects.filter(fuserid=curuserid,tuserid=userid)
        like=[]
        for each in Like.objects.all():
            if(each.userid==curuserid):
                like.append(each.postid)
        messages.success(request,f'Search Result')
        userposts.sort(reverse=True,key=myfun)
        return render(request,'profile.html',{'userid':curuserid,'name':curname,'profile':list1[0],'posts':userposts,'alluser':obj,'status':len(followers),'comment':Comment.objects.all(),'like':like})

def profile(request):
    profileid=request.GET.get('profileid')
    userprofile=User.objects.filter(userid=profileid)
    userposts=[]
    for each in Post.objects.all():
        if(each.userid==profileid):
            userposts.append(each)
    userid=request.session.get('userid')
    name=request.session.get('name')
    followers=FndF.objects.filter(fuserid=userid,tuserid=userprofile[0].userid)
    like=[]
    for each in Like.objects.all():
        if(each.userid==userid):
            like.append(each.postid)
    userposts.sort(reverse=True,key=myfun)
    return render(request,'profile.html',{'userid':userid,'name':name,'profile':userprofile[0],'posts':userposts,'alluser':User.objects.all(),'status':len(followers),'comment':Comment.objects.all(),'like':like})

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=['picture','caption']

def newpost(request):
    if request.method=="POST":
        userid=request.session.get('userid')
        name=request.session.get('name')
        user=User.objects.all()
        for each in user:
            if(each.userid==userid):
                each.postct+=1
                each.save()
                curpostid=str(each.userid)+str(random.randint(0,2000))
                while len(Post.objects.filter(postid=curpostid))!=0:
                    curpostid=str(each.userid)+str(random.randint(10,2000))
                curpost=Post(userid=userid,postid=curpostid)
                form=PostForm(request.POST,request.FILES,instance=curpost)
                if form.is_valid():
                    form.save()
                messages.success(request,f'Post Created !')      
                return feed(request)
    userid=request.session.get('userid')
    name=request.session.get('name')
    return render(request,'newpost.html',{'userid':userid,'name':name,})

def follow(request):
    fuserid=request.GET.get('userid')
    tuserid=request.GET.get('profileid')
    FndF(fuserid=fuserid,tuserid=tuserid).save()
    user1=User.objects.get(userid=fuserid)
    user2=User.objects.get(userid=tuserid)
    user1.following+=1
    user1.save()
    user2.followers+=1
    user2.save()
    return profile(request)

def unfollow(request):
    fuserid=request.GET.get('userid')
    tuserid=request.GET.get('profileid')
    obj1=FndF.objects.get(fuserid=fuserid,tuserid=tuserid)
    obj1.delete()
    user1=User.objects.get(userid=fuserid)
    user2=User.objects.get(userid=tuserid)
    user1.following-=1
    user1.save()
    user2.followers-=1
    user2.save()
    return profile(request)

def followers(request):
    userid=request.GET.get('userid')
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    allfollow=FndF.objects.all()
    obj1=User.objects.all()
    follows=[]
    for each in allfollow:
        if(each.tuserid==userid):
            for every in obj1:
                if(each.fuserid==every.userid):
                    follows.append(every)
    if(len(follows)==0):
        messages.warning(request,f'No Followers Found!')
    else:
        messages.success(request,f'Followers List')
    return render(request,'searchresult.html',{'userid':curuserid,'name':curname,'search':follows})

def following(request):
    userid=request.GET.get('userid')
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    allfollow=FndF.objects.all()
    obj1=User.objects.all()
    follows=[]
    for each in allfollow:
        if(each.fuserid==userid):
            for every in obj1:
                if(each.tuserid==every.userid):
                    follows.append(every)
    if(len(follows)==0):
        messages.warning(request,f'No Followings Found!')
    else:
        messages.success(request,f'Following List')
    return render(request,'searchresult.html',{'userid':curuserid,'name':curname,'search':follows})

def like(request):
    curpostid=request.GET.get('postid')
    curuserid=request.session.get('userid')
    like=Like.objects.filter(postid=curpostid,userid=curuserid)
    post=Post.objects.get(postid=curpostid)
    if(len(like)==0):
        Like(postid=curpostid,userid=curuserid).save()
        post.likecount+=1
        post.save()
    else:
        like.delete()
        post.likecount-=1
        post.save()
    return feed(request)

def likedisplay(request):
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    curpostid=request.GET.get('postid')
    like=Like.objects.filter(postid=curpostid)
    user=User.objects.all()
    obj1=[]
    for each in like:
        for every in user:
            if(each.userid==every.userid):
                obj1.append(every)
    if(len(obj1)==0):
        messages.warning(request,f'No Likes Found!')
    else:
        messages.success(request,f'Liked by following users')
    return render(request,'searchresult.html',{'userid':curuserid,'name':curname,'search':obj1})

def comment(request):
    curuserid=request.session.get('userid')
    curpostid=request.POST.get('postid')
    comment=request.POST.get('comment')
    post=Post.objects.get(postid=curpostid)
    post.commentcount+=1
    post.save()
    Comment(postid=curpostid,userid=curuserid,comment=comment).save()
    return feed(request)


class UpdatedUserForm(ModelForm):
    class Meta:
        model=User
        fields=['profilepic']

def editprofile(request):
    if request.method=="POST":
        curuserid=request.POST.get('userid')
        newemail=request.POST.get('emailid')
        newname=request.POST.get('name')
        status=request.POST.get('status')
        user=User.objects.get(userid=curuserid)
        user.name=newname
        request.session['name']=newname
        user.emailid=newemail
        user.save()
        if(status):
            form=UpdatedUserForm(request.POST,request.FILES,instance=user)
            if form.is_valid():
                form.save()
        messages.success(request,f'Profile Update Successfully!')
        return feed(request)
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    user=User.objects.get(userid=curuserid)
    return render(request,'editprofile.html',{'userid':curuserid,'name':curname,'profile':user})

def changepassword(request):
    if request.method=="POST":
        curuserid=request.session.get('userid')
        curname=request.session.get('name')
        oldpass=request.POST.get('curpass')
        newpass=request.POST.get('newpass')
        repass=request.POST.get('repass')
        if(oldpass=='' or newpass=='' or repass==''):
            messages.warning(request,f'Fields cannot be empty!')
            return render(request,'changepassword.html',{'userid':curuserid})
        if(newpass!=repass):
            messages.warning(request,f'New Passwords donnot match!')
            return render(request,'changepassword.html',{'userid':curuserid})
        user=User.objects.get(userid=curuserid)
        if(user.password!=oldpass):
            messages.warning(request,f'Old Password Donnot match!')
            return render(request,'changepassword.html',{'userid':curuserid})
        user.password=newpass
        user.save()    
        messages.success(request,f'Password Updated Successfully!')
        return feed(request)
    curuserid=request.POST.get('userid')
    curname=request.POST.get('name')
    return render(request,'changepassword.html',{'userid':curuserid,'name':curname})

def chatbox(request):
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    list=[]
    for each in FndF.objects.filter(fuserid=curuserid):
        obj=FndF.objects.filter(fuserid=each.tuserid,tuserid=curuserid)
        for every in obj:
            list.append(User.objects.get(userid=every.fuserid))
    if(len(list)==0):
        messages.warning(request,f'No Connected Friends Found!')
        return feed(request)
    onlineusers=[]
    for each in online.objects.all():
        onlineusers.append(each.userid)
    return render(request,'chatbox.html',{'userid':curuserid,'name':curname,'friends':list,'status':0,'online':onlineusers})  

def chatmessages(request):
    profileid=request.GET.get('profileid')
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    Chat=[]
    for each in Message.objects.all():
        if(each.fuserid==profileid and each.tuserid==curuserid):
            Chat.append(each)
        if(each.tuserid==profileid and each.fuserid==curuserid):
            Chat.append(each)
    list=[]
    for each in FndF.objects.filter(fuserid=curuserid):
        obj=FndF.objects.filter(fuserid=each.tuserid,tuserid=curuserid)
        for every in obj:
            list.append(User.objects.get(userid=every.fuserid))
    Chat.sort(key=myfun)
    onlineusers=[]
    for each in online.objects.all():
        onlineusers.append(each.userid)
    return render(request,'chatbox.html',{'userid':curuserid,'name':curname,'friends':list,'status':1,'message':Chat,'recipient':User.objects.get(userid=profileid),'online':onlineusers})

def delete(request):
    postid=request.GET.get('postid')
    post=Post.objects.get(postid=postid)
    post.delete()  
    for each in Like.objects.all():
        if each.postid==postid:
            each.delete()
    for each in Comment.objects.all():
        if each.postid==postid:
            each.delete()
    user=User.objects.get(userid=request.session.get('userid'))
    user.postct-=1
    user.save()
    messages.success(request,f'Post Deleted Succesfully!')
    return profile(request)

def update(request):
    if request.method=="POST":
        postid=request.POST.get('postid')
        caption=request.POST.get('caption')
        post=Post.objects.get(postid=postid)
        post.caption=caption
        post.save()
        messages.success(request,f'Caption Updated!')
        
        curuserid=request.session.get('userid')
        curname=request.session.get('name')
        userprofile=User.objects.filter(userid=curuserid)
        userposts=[]
        for each in Post.objects.all():
            if(each.userid==curuserid):
                userposts.append(each)
        followers=FndF.objects.filter(fuserid=curuserid,tuserid=userprofile[0].userid)
        like=[]
        for each in Like.objects.all():
            if(each.userid==curuserid):
                like.append(each.postid)
        userposts.sort(reverse=True,key=myfun)
        return render(request,'profile.html',{'userid':curuserid,'name':curname,'profile':userprofile[0],'posts':userposts,'alluser':User.objects.all(),'status':len(followers),'comment':Comment.objects.all(),'like':like})
    postid=request.GET.get('postid')
    return render(request,'updatepost.html',{'postid':postid})

def sendmsg(request):
    message=request.POST.get('message')
    profileid=request.POST.get('profileid')
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    if(message!=''):
        Message(fuserid=curuserid,tuserid=profileid,textmessage=message).save()
    Chat=[]
    for each in Message.objects.all():
        if(each.fuserid==profileid and each.tuserid==curuserid):
            Chat.append(each)
        if(each.tuserid==profileid and each.fuserid==curuserid):
            Chat.append(each)
    list=[]
    for each in FndF.objects.filter(fuserid=curuserid):
        obj=FndF.objects.filter(fuserid=each.tuserid,tuserid=curuserid)
        for every in obj:
            list.append(User.objects.get(userid=every.fuserid))
    Chat.sort(key=myfun)
    onlineusers=[]
    for each in online.objects.all():
        onlineusers.append(each.userid)
    return render(request,'chatbox.html',{'userid':curuserid,'name':curname,'friends':list,'status':1,'message':Chat,'recipient':User.objects.get(userid=profileid),'online':onlineusers})

class MsgForm(ModelForm):
    class Meta:
        model=Message
        fields=['picturemessage']

def picturemsg(request):
    if request.method=="POST":
        profileid=request.POST.get('profileid')
        msg=Message(fuserid=request.session.get('userid'),tuserid=profileid)
        form=MsgForm(request.POST,request.FILES,instance=msg)
        if(form.is_valid()):
            form.save()
        curuserid=request.session.get('userid')
        curname=request.session.get('name')
        Chat=[]
        for each in Message.objects.all():
            if(each.fuserid==profileid and each.tuserid==curuserid):
                Chat.append(each)
            if(each.tuserid==profileid and each.fuserid==curuserid):
                Chat.append(each)
        list=[]
        for each in FndF.objects.filter(fuserid=curuserid):
            obj=FndF.objects.filter(fuserid=each.tuserid,tuserid=curuserid)
            for every in obj:
                list.append(User.objects.get(userid=every.fuserid))
        Chat.sort(key=myfun)
        onlineusers=[]
        for each in online.objects.all():
            onlineusers.append(each.userid)
        return render(request,'chatbox.html',{'userid':curuserid,'name':curname,'friends':list,'status':1,'message':Chat,'recipient':User.objects.get(userid=profileid),'online':onlineusers})
    profileid=request.GET.get('profileid')
    return render(request,'picturemsg.html',{'profileid':profileid})


class MsgFormNew(ModelForm):
    class Meta:
        model=Message
        fields=['audiomessage']

def audiomsg(request):
    if request.method=="POST":
        profileid=request.POST.get('profileid')
        msg=Message(fuserid=request.session.get('userid'),tuserid=profileid)
        form=MsgFormNew(request.POST,request.FILES,instance=msg)
        if(form.is_valid()):
            form.save()
        
        curuserid=request.session.get('userid')
        curname=request.session.get('name')
        Chat=[]
        for each in Message.objects.all():
            if(each.fuserid==profileid and each.tuserid==curuserid):
                Chat.append(each)
            if(each.tuserid==profileid and each.fuserid==curuserid):
                Chat.append(each)
        list=[]
        for each in FndF.objects.filter(fuserid=curuserid):
            obj=FndF.objects.filter(fuserid=each.tuserid,tuserid=curuserid)
            for every in obj:
                list.append(User.objects.get(userid=every.fuserid))
        Chat.sort(key=myfun)
        onlineusers=[]
        for each in online.objects.all():
            onlineusers.append(each.userid)
        return render(request,'chatbox.html',{'userid':curuserid,'name':curname,'friends':list,'status':1,'message':Chat,'recipient':User.objects.get(userid=profileid),'online':onlineusers})
    profileid=request.GET.get('profileid')
    return render(request,'audiomsg.html',{'profileid':profileid})

def share(request):
    postid=request.GET.get('postid')
    curuserid=request.session.get('userid')
    curname=request.session.get('name')
    list=[]
    for each in FndF.objects.filter(fuserid=curuserid):
        obj=FndF.objects.filter(fuserid=each.tuserid,tuserid=curuserid)
        for every in obj:
            list.append(User.objects.get(userid=every.fuserid))
    if(len(list)==0):
        messages.warning(request,f'No Connected Friends Found!')
        return feed(request)
    return render(request,'share.html',{'userid':curuserid,'name':curname,'friends':list,'postid':postid})  

def sharehere(request):
    userid=request.session.get('userid')
    profileid=request.GET.get('profileid')
    postid=request.GET.get('postid')
    post=Post.objects.get(postid=postid)
    msg=''
    msg='Here is a post by '+User.objects.get(userid=post.userid).name+'. Click to Open!'
    link='/msgpost?postid='+postid
    Message(fuserid=userid,tuserid=profileid,picturemessage=post.picture,textmessage=msg,linkmessage=link).save()
    messages.success(request,f'Message Sent')
    return feed(request)

def msgpost(request):
    postid=request.GET.get('postid')
    post=Post.objects.get(postid=postid)
    newuser=User.objects.get(userid=post.userid)
    status=False
    for each in Like.objects.all():
        if(each.userid==request.session.get('userid') and each.postid==postid):
            status=True
    return render(request,'post.html',{'userid':request.session.get('userid'),'name':request.session.get('name'),'newuser':newuser,'post':post,'like':status,'comment':Comment.objects.all()})