from django.db import models

class ai_analysis_log(models.Model):
    id = models.AutoField(primary_key=True)  # イント、11桁、オートインクリメント
    imagePath = models.CharField(max_length=255, default=None, null=True)  # 文字列、255文字、デフォルトNULL
    success = models.CharField(max_length=255, default=None, null=True)  # 文字列、255文字、デフォルトNULL
    message = models.CharField(max_length=255, default=None, null=True)  # 文字列、255文字、デフォルトNULL
    cls = models.IntegerField(default=None, null=True)  # イント、11桁、デフォルトNULL
    confidence = models.DecimalField(max_digits=5, decimal_places=4, default=None, null=True)  # デシマル、整数1桁、少数4桁、デフォルトNULL
    requestTimestamp = models.IntegerField(default=None, null=True)  # イント、10桁、デフォルトNULL
    responseTimestamp = models.IntegerField(default=None, null=True)  # イント、10桁、デフォルトNULL

    def __str__(self):
        return f'{self.id} - {self.imagePath}'