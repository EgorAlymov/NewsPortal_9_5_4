# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models import Sum
# from django.urls import reverse_lazy
#
#
# class Author(models.Model):
#     authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
#     ratingAuthor = models.SmallIntegerField(default=0)
#
#     def __str__(self) -> str:
#         return self.authorUser.username
#
#     def update_rating(self):  # Рейтинг состоит из следующих слагаемых:
#         #  суммарный рейтинг статей автора умножается на 3;
#         postRat = self.post_set.all().aggregate(sum=Sum('rating'))['sum']
#         #  суммарный рейтинг все.х комментариев автора;
#         userRat = self.authorUser.comment_set.all().aggregate(sum=Sum('rating'))['sum']
#         #  суммарный рейтинг всех комментариев к статьям автора.
#         commentRat = Comment.objects.filter(commentPost__author=self).aggregate(sum=Sum('rating'))['sum']
#         self.ratingAuthor = postRat * 3 + userRat + commentRat
#         self.save()
#
#
# class Category(models.Model):
#     categoryName = models.CharField(max_length=64, unique=True)
#     subscribers = models.ManyToManyField(User, blank=True)
#
#     def __str__(self) -> str:
#         return self.categoryName
#
#
# class Post(models.Model):
#     ARTICLE = 'AR'
#     NEWS = 'NW'
#     POST_TYPE = [
#         (ARTICLE, 'Статья'),
#         (NEWS, 'Новость')
#     ]
#
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
#     categoryType = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE, verbose_name='Тип')
#     dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#     postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
#     title = models.CharField(max_length=128, verbose_name='Заголовок')
#     text = models.TextField(verbose_name='Текст')
#     rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')
#
#     def __str__(self) -> str:
#         return f'{self.title} {self.preview()}'
#
#     def like(self):
#         self.rating += 1
#         self.save()
#
#     def dislike(self):
#         self.rating -= 1
#         self.save()
#
#     def preview(self):
#         return self.text[:124] + '...'
#
#     def get_absolute_url(self):
#         return reverse_lazy('post-detail', kwargs={'pk': self.pk})
#
#
# class PostCategory(models.Model):
#     postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
#     categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#
# class Comment(models.Model):
#     commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
#     commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     dateCreation = models.DateTimeField(auto_now_add=True)
#     rating = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.commentUser.username
#
#     def like(self):
#         self.rating += 1
#         self.save()
#
#     def dislike(self):
#         self.rating -= 1
#         self.save()



from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser}'


    def update_rating(self):
        postRat = self.post_set.aggregate(postRating= Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '....'


    def get_absolute_url(self):
        return f'/news/{self.id}'



class PostCategory(models.Model):
    postThought = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThought = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.postThought}'

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()







