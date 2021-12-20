from django.db import models

class Lottos(models.Model):
    name = models.CharField(max_length=200)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField(null=True,blank=True)
    createddate = models.DateTimeField(auto_now_add=True)
    ip_addresses = models.TextField(default='0.0.0.0,')
    winners_drawn = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Prizes(models.Model):
    name = models.CharField(max_length=200)
    #is_given = models.BooleanField(default=False)
    amount = models.IntegerField(null=True,blank=True)
    lotto = models.ForeignKey(Lottos, on_delete=models.CASCADE,related_name='prizes')
    def __str__(self):
        return self.name

class PrizeSingle(models.Model):
    name = models.CharField(max_length=200)
    is_given = models.BooleanField(default=False)
    amount = models.IntegerField(null=True,blank=True)
    lotto = models.ForeignKey(Lottos, on_delete=models.CASCADE,related_name='lotto_prizes')
    def __str__(self):
        return self.name
        
class Tickets(models.Model):
    ticket_number = models.IntegerField()
    vertification_code = models.CharField(max_length=50,blank=True,null=True)
    is_used = models.BooleanField(default=False)
    lotto = models.ForeignKey(Lottos, on_delete=models.CASCADE,related_name='lottotickets')
    is_winner = models.BooleanField(default=False)
    prize = models.ForeignKey(PrizeSingle, on_delete=models.CASCADE,related_name='prizesss', null=True,blank=True)

    def __int__(self):
        return self.ticket_number
