from django.shortcuts import render
from Registration.models import Course, Student
from django.http import  HttpResponseRedirect
from django.urls import reverse

# Create your views here.

# COURSE
def index(request):
    return render(request,'index.html')

def new_course(request):
    if request.method =="POST":
        c_code=request.POST['code']
        c_desc=request.POST['desc']
        data=Course(code=c_code,description=c_desc)
        data.save()
        return render(request,'new_course.html' , {'message':'Data Save'})
    else:
        return render(request,'new_course.html')
    
def course(request):
    allcourse = Course.objects.all()
    dict = {
        'allcourse':allcourse
    }
    return render (request, 'course.html',dict)

def search_course(request):
    if request.method=='GET':
        data=Course.objects.filter(code=request.GET.get('c_code'))
        dict = {
            'data':data
        }
        return render(request,'search_course.html', dict)
    else:
        return render(request,'search_course.html')

def update_course(request, code):
    data=Course.objects.get(code=code)
    dict = {
        'data':data
    }
    return render (request, 'update_course.html', dict)

def save_update_course(request, code):
    c_desc = request.POST['desc']
    data = Course.objects.get(code=code)
    data.description=c_desc
    data.save()
    return HttpResponseRedirect(reverse("course"))

def delete_course(request, code):
    data = Course.objects.get(code=code)
    data.delete()
    return HttpResponseRedirect(reverse("course"))

#STUDENT

def new_student(request):
    c_code = Course.objects.all()

    if request.method =="POST":
        #get data from html page (new student)
        Id=request.POST['s_id']
        Name=request.POST['s_name']
        Address=request.POST['s_add']
        Phone=request.POST['s_phone']
        S_Code=request.POST['s_course']

        #get fk from reference table
        data_course = Course.objects.get(code=S_Code)
        
        #assign value data
        data=Student(id=Id,name=Name, address=Address, phone=Phone, course_code=data_course )
        
        # save data
        data.save()    

        dict = {
            'c_code':c_code,
            'message' : "Data Save"
        }
        
    else: 
        dict = {
            'c_code':c_code
        }

    return render (request, 'new_student.html', dict)

def search_by_student (request):
    if request.method=='POST':
        s_id=request.POST['s_id']
        data_student=Student.objects.get(id=s_id)
        #check data_student exsis
        data_course = Course.objects.get (code=data_student.course_code_id)
        dict = {
            'data_student':data_student,  
            'data_course':data_course         
        }
        return render(request,'search_by_student.html', dict)
    else:
        return render(request,'search_by_student.html')

def search_by_course (request):
    c_code = Course.objects.all()
    if request.method=='GET':
        stud_course = Student.objects.filter(course_code=request.GET.get('s_course'))
        dict={
            'stud_list':stud_course,
            'course': request.GET.get('s_course'),
            'c_code':c_code
        }
    else:
        dict = {
            'c_code':c_code
        }
    return render(request, 'search_by_course.html',dict)
