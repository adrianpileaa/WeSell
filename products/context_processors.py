from account.models import *
from .models import *
def message_processor(request):
    global number
    number = 0
    if request.user.is_authenticated:   
        profile = Profile.objects.get(pk=request.user.id)
        fav, created = Favourite.objects.get_or_create(user = profile)
        nr = fav.products.all().count()
        if nr > 0:
            number = nr
        else:
            number = ''
    return {
        'fav_number' : number
    }