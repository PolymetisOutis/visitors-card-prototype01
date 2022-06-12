from django.db import models

# # Create your models here.


class Visitors(models.Model):
    date = models.DateField(verbose_name='日付')
    time = models.TimeField(verbose_name='来室時刻')
    company_name = models.CharField(verbose_name='会社名', max_length=50, null=True, blank=True)
    visitor_name = models.CharField(verbose_name='お名前', max_length=25)
    temperature = models.FloatField(verbose_name='検温')
    accompany1_name = models.CharField(verbose_name='同行者1お名前', max_length=25, null=True, blank=True)
    accompany1_temp = models.FloatField(verbose_name='同行者1検温', null=True, blank=True)
    accompany2_name = models.CharField(verbose_name='同行者2お名前', max_length=25, null=True, blank=True)
    accompany2_temp = models.FloatField(verbose_name='同行者2検温', null=True, blank=True)
    accompany3_name = models.CharField(verbose_name='同行者3お名前', max_length=25, null=True, blank=True)
    accompany3_temp = models.FloatField(verbose_name='同行者3検温', null=True, blank=True)
    position = models.CharField(verbose_name='役職', max_length=25, null=True, blank=True)
    interviewer = models.CharField(verbose_name='担当者', max_length=25, null=True, blank=True)
    content = models.TextField(verbose_name='ご用件', null=True, blank=True)
    is_contacted = models.BooleanField(default=False, help_text='コンタクトしたらTrue')


    def __str__(self):
        return str(self.date) + '/' + self.company_name + '/' + self.visitor_name

    class Meta:
        db_table = 'visitors_history'
        verbose_name = '来訪者履歴'
        verbose_name_plural = '来訪者履歴'


class Post(models.Model):
    name = models.CharField(verbose_name='役職名', max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = '役職'
        verbose_name = '役職'
        verbose_name_plural = '役職'

class Member(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='氏名', max_length=25, null=True, blank=True)

    def __str__(self):
        return self.post.name + ' / ' + self.name

    class Meta:
        db_table = '社員メンバー'
        verbose_name = '社員メンバー'
        verbose_name_plural = '社員メンバー'

class Contact(models.Model):
    contact = models.OneToOneField(Visitors, on_delete=models.CASCADE, verbose_name='来訪者履歴')
    interviewer = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='担当者', null=True, blank=True)
    time = models.TimeField(verbose_name='退室時刻', null=True, blank=True)
    contents = models.TextField(verbose_name='内容', null=True, blank=True)

    def __str__(self):
        if self.interviewer == None:
            self.interviewer = Member.objects.get(id=9)
            return str(self.contact.date) + ' / ' + self.contact.visitor_name  + ' / ' + self.interviewer.name
        else:
            return str(self.contact.date) + ' / ' + self.contact.visitor_name  + ' / ' + self.interviewer.name

    class Meta:
        db_table = 'contact_history'
        verbose_name = 'コンタクト履歴'
        verbose_name_plural = 'コンタクト履歴'