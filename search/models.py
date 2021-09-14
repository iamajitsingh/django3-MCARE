from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)


class Post(models.Model):
    STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West   Bengal'),
        ('Andaman and Nicobar', 'Andaman and Nicobar Island'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
        ('Daman and Diu', 'Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Ladakh', 'Ladakh'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Puducherry', 'Puducherry')
    ]
    RESOURCE_CHOICES = [
        ('Oxygen', 'Oxygen'),
        ('Hospital Bed', 'Hospital Bed'),
        ('Blood Plasma', 'Blood Plasma'),
        ('Remdesevir', 'Remdesevir'),
        ('Tocilizumab', 'Tocilizumab'),
        ('Vaccine', 'Vaccine')
    ]
    AGE_CHOICES = [
        ('Senior Citizen', 'Senior Citizen'),
        ('Co-Morbid Adult', 'Co-Morbid Adult'),
        ('Adult', 'Adult'),
        ('Under 18', 'Under 18')
    ]
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", 'Other')
    ]
    op = models.CharField(max_length=20)
    patient = models.CharField(max_length=20)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, default='Senior Citizen')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Other')
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='Delhi')
    district = models.CharField(max_length=20)
    resource = models.CharField(max_length=20, choices=RESOURCE_CHOICES, default='Oxygen')
    is_completed = models.BooleanField(default=False)
    contact_email = models.EmailField(max_length=30, blank=True)
    contact_phone = models.PositiveBigIntegerField(blank=True, default='001')
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.patient)
