from vocabulary_manager import Vocabulary
import csv

with open("./output/cards.csv", "w+", encoding="utf-8", newline="") as file:
	writer = csv.writer(file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

	cards = Vocabulary().download_database()

	for card in cards:
		card_id = card[0]
		client = card[1]
		deck = card[2]
		english = card[3]
		polish = card[4]
		publication_date = card[5]
		due_date = card[6]
		interval = card[7]
		number_of_reviews = card[8]
		answers = card[9]
		card_opening_times = card[10]
		card_closing_times = card[11]
		durations = card[12]
		card_revision_days = card[13]
		line = card[14]

		writer.writerow([card_id, client, deck, english, polish, publication_date, due_date, interval, number_of_reviews, answers, card_opening_times, card_closing_times, durations, card_revision_days, line])