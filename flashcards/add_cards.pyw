from vocabulary_manager import Vocabulary
import csv

with open("./input/new_cards.csv", "r", encoding="utf-8") as file:
	rows = csv.reader(file)

	index = 1
	for row in rows:
		client = row[0]
		polish_english = row[1].split("/")
		polish = polish_english[0]
		english = polish_english[1]
		deck = "vocabulary"

		spell = Vocabulary().add_entry(client, deck, english, polish)

		index += 1
		print(f"Card number {index} processed.")