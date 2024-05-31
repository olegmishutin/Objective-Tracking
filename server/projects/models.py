import os
from django.db import models
from django.contrib.auth import get_user_model


class Projects(models.Model):
    name = models.CharField('название', max_length=128)
    description = models.TextField('описание', null=True, blank=True)
    image = models.ImageField('картинка', upload_to='projects_image/', null=True, blank=True)
    is_completed = models.BooleanField('закончен ли', default=False)

    created_at = models.DateTimeField('время создания', auto_now_add=True)
    date_started = models.DateTimeField('дата начала')
    date_ended = models.DateTimeField('дата окончания')

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='my_projects',
                              verbose_name='Владелец')
    participants = models.ManyToManyField(get_user_model(), related_name='projects', db_table='UserProject',
                                          verbose_name='Участники')

    class Meta:
        db_table = 'Projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def setImage(self, image):
        if image:
            if self.image and os.path.exists(self.image.path):
                os.remove(self.image.path)

            self.image = image

    def delete(self, using=None, keep_parents=False):
        if self.image and os.path.exists(self.image.path):
            os.remove(self.image.path)

        return super(Projects, self).delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField('название', max_length=128)
    description = models.TextField('описание')
    is_completed = models.BooleanField('закончен ли', default=False)

    created_at = models.DateTimeField('время создания', auto_now_add=True)
    date_to_end = models.DateTimeField('дата окончания')

    executor = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='tasks',
                                 null=True, blank=True, verbose_name='Исполнитель')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='tasks', verbose_name='Проект')

    class Meta:
        db_table = 'Task'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
