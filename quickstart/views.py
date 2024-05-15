from django.shortcuts import render

# Create your views here.
from quickstart.models import Entry,Blog,Author, Student
from quickstart.serializers import EntrySerializer, BlogSerializer,AutherSerializer, BlogListSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # entry = Entry.objects.all()
        # entry = Entry.objects.values_list()
        # entry = Entry.objects.filter(headline__contains='1')
       # entry = Entry.objects.exclude(headline='headline1')
        # SELECT "quickstart_entry"."id", "quickstart_entry"."blog_id", "quickstart_entry"."headline", "quickstart_entry"."body_text", "quickstart_entry"."pub_date", "quickstart_entry"."mod_date", "quickstart_entry"."number_of_comments", "quickstart_entry"."number_of_pingbacks", "quickstart_entry"."rating" FROM
        # "quickstart_entry" WHERE NOT ("quickstart_entry"."headline" = headline1)
        # entry = Entry.objects.all().order_by('blog__name')
        # entry = Entry.objects.filter(blog__tagline__exact='blog1 taglie')
        # SELECT "quickstart_entry"."id", "quickstart_entry"."blog_id", "quickstart_entry"."headline", 
        # "quickstart_entry"."body_text", "quickstart_entry"."pub_date", "quickstart_entry"."mod_date",
        # "quickstart_entry"."number_of_comments", "quickstart_entry"."number_of_pingbacks",
        # "quickstart_entry"."rating" FROM "quickstart_entry" INNER JOIN "quickstart_blog" ON ("quickstart_entry"."blog_id" = "quickstart_blog"."id")
        # WHERE "quickstart_blog"."tagline" = blog1 taglie
        # entry = Entry.objects.filter(blog__id=1)
        # count author for each entry
        #entry = Entry.objects.annotate(num_authors = Count('authors'))
        entry = Entry.Objects.select_related('blog')

        print(entry.query)
        serializer = EntrySerializer(entry, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.db.models import Count
class BlogList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # blog = Blog.objects.all()
        # count entry for each blog

        # blog  = Blog.objects.annotate(entry_count=Count('entry'))

        #SELECT "quickstart_blog"."id", "quickstart_blog"."name", "quickstart_blog"."tagline",
        # COUNT("quickstart_entry"."id") AS "entry_count" 
        #FROM "quickstart_blog" LEFT OUTER JOIN "quickstart_entry" ON ("quickstart_blog"."id" =
        # "quickstart_entry"."blog_id") GROUP BY "quickstart_blog"."id", "quickstart_blog"."name", "quickstart_blog"."tagline"
        
        # print(blog.query)
        # data = {}
        # for blog in blog:
        #     data[blog.name]=blog.entry_count
        # return Response(data)
        # blog = Blog.objects.values_list('name', flat=True)

        # print(blog.query)
        # serializer = BlogSerializer(blog, many=True)
        # return Response(serializer.data)

        #blog = Blog.objects.values('name').distinct()
        #SELECT DISTINCT "quickstart_blog"."name" FROM "quickstart_blog"y
        # print(blog.query)
        # serializer = BlogListSerializer(blog, many=True)
        # return Response(serializer.data)
        from django.db import models
        # give the who has duplicate blog name 
        duplicate_blog_names = Blog.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)
        #<QuerySet [{'name': 'blog1', 'name_count': 2}, {'name': 'blog2', 'name_count': 1}, {'name': 'blog3', 'name_count': 1}, {'name': 'blog4', 'name_count': 1}]>
        #filter(name_count__gt=1)
        #<QuerySet [{'name': 'blog1', 'name_count': 2}]>
        duplicate_blogs = Blog.objects.filter(name__in=duplicate_blog_names.values('name'))
        #duplicate_blog_names.values('name'): This retrieves just the names from the duplicate_blog_names queryset

        #print(blog.query)
        #serializer = BlogSerializer(duplicate_blogs, many=True)
        #return Response(serializer.data)
        #Lookups that span relationships
        blog = Blog.objects.filter(entry__body_text__contains="blog2").values()
        blog = Blog.objects.filter(entry__authors__name="author2").values()
        blog = Blog.objects.filter(entry__authors__isnull=False).values()
        blog = Blog.objects.filter(entry__authors__isnull=True).values()
        blog = Blog.objects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)
        # filter blog headline = headline1 and years 2023
        blog = Blog.objects.filter(entry__headline__contains="headline1", entry__pub_date__year=2023).values()
        # or we can write like this
        #blog =  Blog.objects.filter(entry__headline__contains="headline1").filter(entry__pub_date__year=2023)
         # or
        blog = Blog.objects.filter(Q(entry__headline__contains="headline1") & Q(entry__pub_date__year=2023)).values()
    
        blog = Blog.objects.filter(~Q(entry__headline__contains="headline1") | ~Q(entry__pub_date__year=2023)).values()

        return Response({"meassage":blog})

    
    def post(self , request):
        blog = Blog(name="story telling", tagline="story")
        # blog.name = "asnmsd"
        blog.save()
        #Saving ForeignKey in entry model which id 1
        entry = Entry.objects.get(pk=1)
        cheese_blog = Blog.objects.get(name="story telling")
        entry.blog = cheese_blog
        entry.save

        #Saving ManyToManyField in entry model which id 1
        # entry = Entry.objects.get(pk=1)
        # john = Author.objects.create(name="John")
        # paul = Author.objects.create(name="Paul")
        # entry.authors.add(john,paul)
        
        
        return Response({"sucess":"done"})


    

class AuthorList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        author = Author.objects.all()
        
        print(author.query)
        serializer = EntrySerializer(author, many=True)
        return Response(serializer.data)


class EntryApiView(APIView):

    def get(self,request):
        entry_data = []
        entry = Entry.objects.all()#<QuerySet [<Entry: headlin2>, <Entry: headline1>]>)
        entry = Entry.objects.all().values()# or Entry.objects.values()
        #<QuerySet [{'id': 1, 'blog_id': 2, 'headline': 'headlin2', 'body_text': 'entery1 body text',
        # 'pub_date': datetime.date(2024, 2, 1),
        # 'mod_date': datetime.date(2024, 2, 18), 'number_of_comments': 5, 
        #'number_of_pingbacks': 3, 'rating': 6}, {'id': 2, 'blog_id': 1, 'headline': 'headline1',
        # 'body_text': 'blog1 body text', 'pub_date': datetime.date(2024, 2, 2), 'mod_date': datetime.date(2024, 2, 12), 'number_of_comments': 2, 'number_of_pingbacks': 2, 'rating': 6}]>
        entry = Entry.objects.all()
        for entry in  entry:
            entry_dict = {"entry_blog_name":entry.blog.name,
                          "entry_blog_email":entry.blog.tagline
            }
            entry_data.append(entry_dict)
        

        entry = Entry.objects.values_list()
        #<QuerySet [(1, 2, 'headlin2', 'entery1 body text', datetime.date(2024, 2, 1), datetime.date(2024, 2, 18), 5, 3, 6),
        # (2, 1, 'headline1', 'blog1 body text', datetime.date(2024, 2, 2), datetime.date(2024, 2, 12), 2, 2, 6)]>
        #return Response({"entry":entry,"message":"sucess"})

        #return Response({"entry":entry_data,"message":"sucess"})

         # field lookups means where clause and example
        entry = Entry.objects.filter(blog_id=1).values()
        #or
        entry = Entry.objects.filter(blog__id=1).values()
        entry = Entry.objects.filter(headline__exact="headline1").values()
        entry = Entry.objects.filter(blog__tagline__exact="blog1 taglie").values()

        entry = Entry.objects.get(headline__contains="2")
        entry = {
            "id":entry.id,
            "headline":entry.headline
        }
        #Lookups that span relationships
        return Response({"entry":entry,"message":"sucess"})

from django.db.models import Case, When, BooleanField
from datetime import date, timedelta
from datetime import datetime
from django.db.models import Q

class StudentApiView(APIView):
    def get(self, request):
        eighteen_years_ago = date.today() - timedelta(days=18*365)
        #give student from student model whose age grater than 18
        #student = Student.objects.filter(birth_date__lt=eighteen_years_ago).values_list()
        # give student his age less than 18
        #student = Student.objects.filter(birth_date__gt=eighteen_years_ago).values()

        # add dynamic field is_active=True/False when age less than 18 or grater
        data = []
        student = Student.objects.annotate(
        is_active=Case(
            When(birth_date__lt=eighteen_years_ago, then=True),
            default=False,
            output_field=BooleanField()
        )
        
        )
        for student in student:
            student_data = {
                 'name': student.first_name, 
                'is_active': student.is_active,
             }
            
            data.append(student_data)
        # student = student.values()
        student = Student.objects.filter(birth_date__year=2024).values()
        student = Student.objects.filter(birth_date__month=5).values()
        # Filter students born on the 5th day of any month
        student = Student.objects.filter(birth_date__day=5).values()
        #To filter students by birth month (specifically May) without using the numeric representation of the month,
        month_names_to_numbers = {
            'January': 1,
            'May': 5,
            'June': 6,
           
        }
        june_month_number = month_names_to_numbers['June']
        student = Student.objects.filter(birth_date__month=june_month_number).values()
        # Filter students born in May or June
        student = Student.objects.filter(birth_date__month=6).values() | Student.objects.filter(birth_date__month=5).values()
        #or
        student = Student.objects.filter(Q(birth_date__month=6) | Q(birth_date__month=5)) .values() 
        # Filter students born within the specified date range
        # Define start and end dates for the range
        start_date = datetime(year=2000, month=1, day=1)
        end_date = datetime(year=2005, month=12, day=31)
        student = Student.objects.filter(birth_date__range=(start_date, end_date))
        # filter student that birth month 5 or 6 but noth 12 date
        student = Student.objects.filter(Q(birth_date__month=5) | Q(birth_date__month=6)).exclude(birth_date__day=13).values()
        # Filter students whose birth date month is not June (month 6)
        student = Student.objects.exclude(birth_date__month=6)
        student = Student.objects.filter(birth_date__month=6).exclude(first_name = 'raju').values()
        student = Student.objects.filter(birth_date__month=6).exclude(first_name__startswith = 's').values()
        # use order by
        student = Student.objects.order_by('first_name').values()
        # student = Student.objects.order_by('first_name')[0]
        student = Student.objects.get(pk=3)
        student = Student.objects.order_by('first_name')[0]
        student = {
            'id':student.id,
            'first_name':student.first_name
        }
    
        return Response({"message":student})
