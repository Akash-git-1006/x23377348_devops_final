from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class house (models.Model):

     class  bedrooms_Choices(models.TextChoices):
        bed1 = '1'
        bed2 ='2'
        bed3 ='3'
        bed4 ='4'
        bed5 ='5'
        bed6 ='6'
        bed7 ='7'
        bed8 ='8'

     class  bathrooms_Choice(models.TextChoices):
        bath1 = '1'
        bath2 ='2'
        bath3 ='3'
        bath4 ='4'
        bath5 ='5'
        bath6 ='6'
        bath7 ='7'
        bath8 ='8'
    
     class  property_Choices(models.TextChoices):
        House = 'House'
        Apartment ='Apartment'
        StudioApartment ='Studio Apartment'
                        
    
    # title = models.CharField(max_length=200)
     description = models.TextField(blank=True, null=True)  # Description of the property
     property_id = models.AutoField(primary_key=True)
     location = models.CharField(max_length=200)  # Location of the property
     rent = models.DecimalField(max_digits=10, decimal_places=2)  # Rent amount
     property_type = models.CharField(max_length=50, choices=property_Choices.choices)
     square_feet = models.IntegerField()  # Size of the property in square feet

    # Property specifications
     number_of_bedrooms = models.IntegerField()  # Number of bedrooms
     number_of_bathrooms = models.IntegerField()  # Number of bathrooms

    # Owner details
    # owner_name = models.CharField(max_length=100)  # Name of the owner
     seller = models.ForeignKey(User,on_delete=models.CASCADE)
     phone_number = models.CharField(max_length=15)  # Owner's phone number
    # email = models.EmailField()  # Owner's email address

    # Timestamp
     date_posted = models.DateTimeField(default=timezone.now)
     Available_from = models.DateField() 
     image1 = models.ImageField(upload_to='item_images/', blank=True, null=True)
     image2 = models.ImageField(upload_to='item_images/', blank=True, null=True)
     image3 = models.ImageField(upload_to='item_images/', blank=True, null=True)


     def __str__(self):
        return f"Product {self.property_id}: {self.description}"



