from django.db import models

class Card(models.Model):
	card_id = models.IntegerField(primary_key = True)
	client = models.CharField(max_length=200)
	deck = models.CharField(max_length=200)
	english = models.CharField(max_length=200)
	polish = models.CharField(max_length=200)
	publication_date = models.IntegerField()
	due_date = models.IntegerField()
	interval = models.IntegerField()
	number_of_reviews = models.IntegerField()
	answers = models.CharField(max_length=200)
	card_opening_times = models.CharField(max_length=200)
	card_closing_times = models.CharField(max_length=200)
	durations = models.CharField(max_length=200)
	card_revision_days = models.CharField(max_length=200)
	line = models.IntegerField()

class Client(models.Model):
	client = models.CharField(max_length=200)
	daily_limit_of_new_cards = models.IntegerField()