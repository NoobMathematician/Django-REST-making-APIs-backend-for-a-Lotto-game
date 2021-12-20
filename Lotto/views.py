from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import Lottos, Prizes, Tickets,PrizeSingle
from django.views.decorators.csrf import csrf_exempt
from .serializer import LottosSerializer,TicketSerializer,PrizesSerializer,LottosSerializerSingle
import random


import os

@api_view(['GET'])
def Homepage(request):
    return Response({"message": "Hello, Welcome!"})


@api_view(['GET','POST',])
@csrf_exempt
def lottos_list(request):

    """ Get manager IPs """
    MANAGER_IPS = os.environ.get('MANAGER_IPS')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    """ List lottos starting from latest """
    if request.method == 'GET':
        lottos = Lottos.objects.all().order_by("-createddate")
        serializer = LottosSerializer(lottos, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    """ Create lottos """
    if request.method == 'POST':

        """ Only manager ip can create lotto """
        if ip in MANAGER_IPS:
            data = request.data
            ticket_count = int(data['total_tickets'])

            """ Count amount of prizes of the lotto """
            total_prize = 0            
            for prize in data["prizes"]:
                    total_prize += int(prize['amount'])

            """ The total amout of tickets must be hight than the total amount of prizes """
            if total_prize > ticket_count:
                return Response({"message":"Too many prizes"},status=status.HTTP_400_BAD_REQUEST)

            """ Render the prizes, if prizes are not empty """
            if len(data["prizes"]) > 0:
                ticket_count = int(data['total_tickets'])
                newlotto = Lottos(name=data['name'],total_tickets=ticket_count,available_tickets=ticket_count)
                newlotto.save()

                for prize in data["prizes"]:
                    amount = int(prize['amount'])
                    newprize = Prizes(name=prize['name'],amount=amount,lotto=newlotto)
                    newprize.save()
                    for item in range(amount):
                        prizesingle = PrizeSingle(name=prize['name'],amount=amount,lotto=newlotto)
                        prizesingle.save()

                for item in range(ticket_count):
                    newticket = Tickets(ticket_number=item+1,lotto=newlotto)
                    newticket.save()

                """ Return created lotto with HTTP_201_CREATED """
                return Response({"name": f"{newlotto.name}","total_tickets": f"{newlotto.total_tickets}","available_tickets": f"{newlotto.total_tickets}","winners_drawn": False,"id": newlotto.id},status=status.HTTP_201_CREATED)

            else:
                """ If prizes are empty, return HTTP_400_BAD_REQUEST """
                return Response({"message":"Empty Prizes"},status=status.HTTP_400_BAD_REQUEST)

        else:
            """ Unable to create lotto without manager's ip, return HTTP_400_BAD_REQUEST """
            return Response({"message": "Only Manaher can create lotto"},status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"message": "Okay"})



@api_view(['GET'])
def lotto_detail(request, pk):
    
    """ Get lotto detail by the lotto's id"""
    try:
        lotto = Lottos.objects.get(pk=pk)
    except Lottos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LottosSerializerSingle(lotto)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST','GET'])
def lotto_winners(request, pk):
    
    """Get the lotto by id"""
    try:
        lotto = Lottos.objects.get(pk=pk)
    except Lottos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """ Get manager IPs """
    MANAGER_IPS=os.environ.get('MANAGER_IPS')

    """ Get users IPs """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    """ Draw the winners """
    if request.method == 'POST':
        if ip in MANAGER_IPS:
            tickets = lotto.lottotickets.filter(is_used=False)
            if not tickets:
                if lotto.winners_drawn is False:
                    prizes = lotto.lotto_prizes.all()
                    winnercount = prizes.count()
                    for i in range(winnercount):
                        prizes = lotto.lotto_prizes.filter(is_given=False)
                        tickets_list = lotto.lottotickets.filter(is_winner=False)
                        winner_ticket = random.choice(tickets_list)
                        winner_ticket.is_winner = True
                        winner_prize = random.choice(prizes)
                        winner_ticket.prize = winner_prize
                        winner_ticket.save()
                        winner_prize.is_given = True
                        winner_prize.save()
                    lotto.winners_drawn = True
                    lotto.save()
                    serializer = LottosSerializerSingle(lotto)
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    return Response({"Winners for the lotto have already been drawn"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"Winners can't be drawn when tickets are still available"},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Only manager can draw winner"},status=status.HTTP_403_FORBIDDEN )
    if request.method == 'GET':
        tickets_list = lotto.lottotickets.filter(is_winner=True)
        serializer = TicketSerializer(tickets_list, many=True)
        return Response(serializer.data)

""" Create random verification code function """
def randomstring():
    result_str = ''.join((random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(15)))
    return result_str

@api_view(['POST','GET'])
def ticket_get(request, pk):
    
    """ Check if the lotto exists """
    try:
        lotto = Lottos.objects.get(pk=pk)
    except Lottos.DoesNotExist:
        return Response({"Lotto":"Does not exit"},status=status.HTTP_404_NOT_FOUND)

    """ Get user's ip and save it for checking """
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        userip = f"{ip},"
        useripcheck = ip
        already_buy_ips = lotto.ip_addresses
        ip_list = already_buy_ips.split(",")

        """ Check if the player already bought a ticket """
        if useripcheck in ip_list:
            return Response({"Your ip address has already participated in this lotto"},status=status.HTTP_403_FORBIDDEN)

        """ Get a ticket from available tickets"""
        tickets = lotto.lottotickets.filter(is_used=False)
        if tickets:
            random_ticket = random.choice(tickets)
            vertification_code_random = randomstring()
            random_ticket.vertification_code = vertification_code_random
            random_ticket.is_used = True
            random_ticket.save()
            lotto.ip_addresses += userip
            lotto.available_tickets -= 1
            lotto.save()
            ticket_number = int(random_ticket.ticket_number)
            return Response({"verification_code": f"{vertification_code_random}","lotto_id": lotto.id,"ticket_number": ticket_number},status=status.HTTP_201_CREATED)
        else:
            return Response({"Tickets to this lotto are no longer available"},status=status.HTTP_410_GONE)
    if request.method == 'GET':
        return Response({"message": "Okay"})

@api_view(['POST','GET'])
def ticket_verification(request, pk):

    """ Check if the lotto exists """
    try:
        lotto = Lottos.objects.get(pk=pk)
    except Lottos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    """ Check verification code which was sent with ticket in the get ticket process """
    if request.method == 'POST':
        if lotto.winners_drawn is True:
            data = request.data
            code = data['verification_code']
            winnerticket = lotto.lottotickets.filter(is_winner=True).filter(vertification_code=code).first()
            if winnerticket is not None:
                return Response({"Success": "You Are a Winner of this Raffel","Lotto Number": f"{lotto.id}","Ticket Number": f"{winnerticket.ticket_number}","Prize":f"{winnerticket.prize}"})
            else:
                return Response({"Error": "Wrong Verification Code or This ticket is not winner"})
        else:
            return Response({"Error": "Winners for the lotto have not been drawn yet"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return Response({"message": "Okay"})