from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Wallet


def home(request):

    user = request.user
    try:
        user = request.user  # Get the current authenticated user
        wallet = Wallet.objects.get(user=user)  # Retrieve the associated wallet

    except Wallet.DoesNotExist:
       
        wallet = Wallet.objects.create(user=user, balance=0)
    
    context = {
        'user':user,
        'wallet':wallet,
    }

    return render(request, "wallet/home.html",context)



@login_required
def transferFund(request):
    if request.method == 'POST':
        wallet_id = request.POST.get('wallet-id')

        try:
            recipient_wallet = Wallet.objects.select_for_update().get(id=wallet_id)  #select_for_update() ensures that the selected record is locked until the end of the transaction
        except Wallet.DoesNotExist:
            return redirect('wallet:error-page')


        user_wallet = request.user.wallet
        transfer_amount = int(request.POST.get('transfer-amount'))

        if recipient_wallet != user_wallet:  # Check if recipient wallet is not the same as the user's wallet
            with transaction.atomic():
                if user_wallet.balance >= transfer_amount:
                    user_wallet.balance -= transfer_amount
                    recipient_wallet.balance += transfer_amount
                    user_wallet.save()
                    recipient_wallet.save()
                    return redirect('wallet:success-page')
                else:
                    messages.error(request, 'Insufficient balance.')
                    return redirect('wallet:home')
        else:
            messages.error(request, "You cannot transfer funds to your own wallet.")
            return redirect('wallet:home')  # Replace 'home' with the appropriate URL name for the home page


    return render(request, 'wallet/home.html')



def error(request):
    return render(request,"wallet/error.html")


def successPage(request):
    return render(request,"wallet/success.html")


