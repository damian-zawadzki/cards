from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from vocabulary_manager import Vocabulary
from time_machine import TimeMachine
import csv

card_opening_time = 0


def home(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name

        total_phrases = Vocabulary().total_cards(current_user)
        new_phrases = Vocabulary().new_cards(current_user)

        return render(request, 'home.html', {"total_phrases": total_phrases, "new_phrases": new_phrases})

    return render(request, 'home.html', {})


@login_required(login_url='login_user.html')
def vocabulary(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name

        all_due_entries = Vocabulary().display_due_entries(current_user)

        if len(all_due_entries) == 0:
            Vocabulary().reset_line(current_user)
            return render(request, 'congratulations.html', {})

        else:
            global card_opening_time

            now = TimeMachine().now_colons()
            now_number = TimeMachine().date_time_to_number(now)
            card_opening_time = now_number

            card_id = all_due_entries[0][0]
            polish = all_due_entries[0][1]
            english = all_due_entries[0][2]
            old_due_today = len(Vocabulary().display_old_due_entries(current_user))
            new_due_today = len(Vocabulary().display_new_due_entries(current_user))
            problematic_due_today = len(Vocabulary().display_problematic_due_entries(current_user))

            if request.method == "POST":
                if request.POST["answer"] != "edit":
                    return render(request, 'vocabulary.html', {"polish": polish, "old_due_today": old_due_today, "new_due_today": new_due_today, "problematic_due_today": problematic_due_today})
                else:
                    return render(request, "edit_card.html", {"card_id": card_id, "polish": polish, "english": english})

            return render(request, 'vocabulary.html', {"polish": polish, "old_due_today": old_due_today, "new_due_today": new_due_today, "problematic_due_today": problematic_due_today})

@login_required(login_url='login_user.html')
def view_answer(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name

        all_due_entries = Vocabulary().display_due_entries(current_user)

        card_id = all_due_entries[0][0]
        polish = all_due_entries[0][1]
        english = all_due_entries[0][2]
        old_due_today = len(Vocabulary().display_old_due_entries(current_user))
        new_due_today = len(Vocabulary().display_new_due_entries(current_user))
        problematic_due_today = len(Vocabulary().display_problematic_due_entries(current_user))
        interval = all_due_entries[0][4]
        print(polish)

        # If a button is clicked
        if request.method == "POST":
            if request.POST["answer"] != "edit":
                answer = request.POST["answer"]
                Vocabulary().update_card(card_id, answer, card_opening_time)

                all_due_entries = Vocabulary().display_due_entries(current_user)

                # If there are no more cards to review
                if len(all_due_entries) == 0:
                    Vocabulary().reset_line(current_user)
                    return redirect('congratulations.html')

                else:
                    return redirect('vocabulary.html')
            else:
                return render(request, "edit_card.html", {"card_id": card_id, "polish": polish, "english": english})

        # If no button is clicked
        return render(request, 'view_answer.html', {"polish": polish, "english": english,  "old_due_today": old_due_today, "new_due_today": new_due_today, "problematic_due_today": problematic_due_today, "interval": interval})


@login_required
def congratulations(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name
        reset_line = Vocabulary().reset_line(current_user)
        messages.success(request, ("You're done for today!"))

        return render(request, 'congratulations.html', {})


def login_user(request):
    if request.method == "POST":
        email_address = request.POST["email_address"]
        password = request.POST["password"]

        items = User.objects.values_list("email", "first_name", "last_name")

        for item in items:
            if item[0] == email_address:
                username = item[1] + item[2]
                username = username.lower()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have successfully logged in."))
            return redirect("home")
        else:
            messages.error(request, ("Wrong password or username. Try again."))
            return redirect("login_user")

    else:
        return render(request, "login_user.html", {})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("Come back soon!"))
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        email_address = request.POST["email_address"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        username = first_name.lower() + last_name.lower()
        user = authenticate(request, username=username, password=password)

        if user is None:
            user = User.objects.create_user(username, email_address, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, ("The student has been added to the database."))
            return redirect("home")

        else:
            messages.success(request, ("The student already exists."))

    return render(request, "register_user.html", {})


@login_required
def options(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name

        if request.method == "POST":
            current_daily_limit_of_new_cards = request.POST["new_daily_limit_of_new_cards"]
            print(current_daily_limit_of_new_cards)
            change_the_limit = Vocabulary().update_current_daily_limit_of_new_cards(current_user, current_daily_limit_of_new_cards)

            return render(request, "options.html", {"current_daily_limit_of_new_cards": current_daily_limit_of_new_cards})

        current_daily_limit_of_new_cards = Vocabulary().current_daily_limit_of_new_cards(current_user)

        return render(request, "options.html", {"current_daily_limit_of_new_cards": current_daily_limit_of_new_cards})


@login_required
def add_cards(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name

        if request.method == "POST":
            polish = request.POST["polish"]
            english = request.POST["english"]
            deck = "vocabulary"
            add = Vocabulary().add_entry(current_user, deck, english, polish)

            messages.success(request, ("The card has been added!"))
            return redirect("add_cards.html")

        return render(request, "add_cards.html", {})


@login_required
def edit_card(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        current_user = first_name + " " + last_name
        x = 2
        if request.method == "POST":
            if request.POST["change"] == "edit":
                card_id = request.POST["card_id"]
                polish = request.POST["polish"]
                english = request.POST["english"]
                commit_change = Vocabulary().edit_card(card_id, polish, english)
                messages.success(request, ("The changes have been made!"))

                return redirect("vocabulary.html")

            elif request.POST["change"] == "delete":
                card_id = request.POST["card_id"]
                commit_change = Vocabulary().delete_card(card_id)
                messages.success(request, ("The card has been deleted!"))

                return redirect("vocabulary.html")

    return render(request, "edit_card.html", {"card_id": card_id, "polish": polish, "english": english})
