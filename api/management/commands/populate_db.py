import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User,Product,Order,OrderItem


class Command(BaseCommand):
    help='Creates application data'


    def handle(self,*args,**kwargs):
        #gets or create superuser
        user=User.objects.filter(username='admin').first()
        if not user:
            user =User.objects.create_superuser(username='admin',password='testing')

        #create products = name,price,stock,image

        products=[

            Product(name="A Scanner Darkly",description=lorem_ipsum.paragraph(),price=Decimal('12.90'),stock=4),
            Product(name="Coffee Machine",description=lorem_ipsum.paragraph(),price=Decimal('70.99'),stock=6),
            Product(name="Velvet Underground & Nico",description=lorem_ipsum.paragraph(),price=Decimal('15.99'),stock=11),
            Product(name="Enter the wu-tang",description=lorem_ipsum.paragraph(),price=Decimal('17.99'),stock=2),
            Product(name="Digital camera",description=lorem_ipsum.paragraph(),price=Decimal('350.99'),stock=4),
            Product(name="Watch",description=lorem_ipsum.paragraph(),price=Decimal('500.05'),stock=0),
            
        ]

#create products & refetch from DB

        Product.objects.bulk_create(products)
        products=Product.objects.all()


#create some dummy orders tied to the super user
     
        for _ in range(3):
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), 2):  # ✅ FIXED
               OrderItem.objects.create(
                order=order, product=product, quantity=random.randint(1, 3)
        )


