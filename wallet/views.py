from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Wallet

import qrcode
from PIL import Image
import hashlib
from io import BytesIO
from django.core.files import File
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def home(request):

    if not request.user.is_anonymous:
        try:
            user = request.user  # Get the current authenticated user
            wallet = Wallet.objects.get(user=user)  # Retrieve the associated wallet

        except Wallet.DoesNotExist:

            data = user.username

            # Create a SHA-256 hash object
            hash_object = hashlib.sha256()

            # Update the hash object with the data
            hash_object.update(data.encode('utf-8'))

            # Get the hexadecimal representation of the hash
            hash_value = hash_object.hexdigest()

            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(hash_value)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Create a BytesIO object to hold the image data
            image_io = BytesIO()

            # Save the image to the BytesIO object
            img.save(image_io, format='PNG')

            # Create a File object from the BytesIO data
            image_file = File(image_io)

            # Create the Wallet instance and save it
            wallet = Wallet.objects.create(
                user=user, 
                balance=200, 
                id_hash=hash_value,
            )
            wallet.qr_code.save(f'{user.username}.png', image_file, save=True)


        
        context = {
            'user':user,
            'wallet':wallet,
        }

        return render(request, "wallet/index.html",context)
    
    else:
        return redirect('account/login')



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


