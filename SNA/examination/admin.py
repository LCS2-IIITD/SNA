from django.contrib import admin
from .models import Question, Test, UserResponse, UserTests, Answer, Topic, questionmap
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.
class AnswerInline(admin.StackedInline):
    model = Answer
    max_num = 4

class QuestionInline(admin.StackedInline):
    model = questionmap
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question','topic', 'difficulty',)
    inlines = (AnswerInline,)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display= ('name',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'test_code', 'num_questions',)
    inlines=(QuestionInline,)
    
@admin.register(UserTests)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test',)
    
@admin.register(UserResponse)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('response', 'test',)