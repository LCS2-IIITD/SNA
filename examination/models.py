from django.db import models
from token_validation.models import Account
# from django_better_admin_arrayfield.models.fields import ArrayField
from tinymce import HTMLField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.


class Topic(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=30)
    def __str__(self):
        return self.name


class Test(models.Model):
    test_name = models.CharField(blank=False, max_length=50)
    test_code = models.CharField(blank=False, unique=True, max_length=20)
    test_description = models.TextField(blank=True, unique=False)
    num_questions = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(default=20,blank=False)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.test_name

class Question(models.Model):
    question = HTMLField()
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(max_length=200, blank=True, default="Dummy Description")
    test = models.ForeignKey(Test, blank=True, on_delete = models.CASCADE)
    def __str__(self):
        return self.description

class Answer(models.Model):
    answer = HTMLField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")
    is_correct = models.BooleanField(default=False)

class UserTests(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    @property
    def calculate_score(self):
        correct = UserResponse.objects.filter(test=self, response__is_correct=True).count()
        #total_questions = self.test.num_questions
        return correct
    
    @property
    def total_questions(self):
        return self.test.num_questions

class UserResponse(models.Model):
    response = models.ForeignKey(Answer, blank=True, null=True, on_delete = models.CASCADE)
    ques = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    test = models.ForeignKey(UserTests, on_delete=models.CASCADE)

    def is_correct(self):
        return self.response.is_correct
    
class questionmap(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Question in this test"
        verbose_name_plural = "Questions in this test"
