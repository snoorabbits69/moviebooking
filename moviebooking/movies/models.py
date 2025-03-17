from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse
# Create your models here.


class Room(models.Model):
     name=models.CharField(max_length=50)
     seats_row= models.PositiveIntegerField(blank=True)
     num_seats = models.PositiveIntegerField(blank=True)
  





class Movie(models.Model):
    
    class RatingChoices(models.TextChoices):
     G = "G", "G"
     PG = "PG", "PG"
     PG_13 = "PG-13", "PG-13"
     R = "R", "R"
     A = "A", "A"

        
    title=models.CharField(max_length=200)
    genre=TaggableManager()
    description=models.TextField(max_length=500,blank=True)
    posterimage=models.ImageField(
        upload_to="poster/%Y/%m/%d",
        blank=True
    )
    languages=models.JSONField(default=list,blank=True)
    duration=models.TextField(max_length=40, blank=True)
    created=models.DateTimeField(auto_now_add=True,blank=True)
    Rating=models.TextField(
        max_length=6,
        choices=RatingChoices.choices,
        blank=True
    )
    class Meta:
        indexes=[models.Index(fields=['-created'])]
        ordering=['-created']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('movie_detail',args=[self.id])
    
    
class Show(models.Model):
    movie=models.ForeignKey(Movie,related_name='show_times',on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Start Date",null=True)
    price = models.PositiveIntegerField(verbose_name="Ticket Price")
    room=models.ForeignKey(
        Room,
        related_name='running_shows',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    showtime = models.TimeField(verbose_name="Showtime",auto_now=False, auto_now_add=False,blank=True, null=True)
    class Meta:
        indexes=[models.Index(fields=['-showtime'])]
        ordering=["-start_date"]
    def __str__(self):
     return f"{self.movie.title} - {self.showtime.strftime('%H:%M') if self.showtime else 'No Time'}"
    
    def generate_seats(self):
     total_seats = self.room.num_seats
     num_rows =self.room.seats_row
     
     seatindex = [chr(65 + i) for i in range(num_rows)]  
     
     full_row_size = total_seats // num_rows 
     remaining_seats = total_seats % num_rows 
 
     seats = []  
     
     for i in range(num_rows):
         row_size = full_row_size + (1 if i < remaining_seats else 0)  
         for j in range(1, row_size + 1):
             seats.append(f"{seatindex[i]}{j}")  
  
     Seat.objects.bulk_create([Seat(show=self, seat_num=seat) for seat in seats])
 
    def get_absolute_url(self):
        return reverse("book_show", args=[self.id,self.movie])
    
    def save(self, *args, **kwargs):
     is_new = self.pk is None  # Check if the object is new (unsaved)
     super().save(*args, **kwargs)  # Save the Show first
 
     if is_new and not Seat.objects.filter(show=self).exists():
         self.generate_seats()

    
   
    
    
class Seat(models.Model):
 show=models.ForeignKey(
     Show,
     related_name='seat_num',
     on_delete=models.CASCADE
 )
 seat_num = models.CharField(max_length=25)
 booked=models.BooleanField(default=False)