# -*- coding: utf-8 -*-
import sys  # used for program exit
from Login import login  # used for user login
from SoldTickets import update_sold_tickets  # used to update the number of sold tickets
from SoldTickets import load_sold_tickets  # used to load the number of sold tickets
import matplotlib.pyplot as plt  # used for graphical display

def main():
    print(
        """
    \t\t=== CINEMA ===
    
    
    Choose how you want to log in?
    
    (0) Exit
    (1) Customer
    (2) Manager (login required)
    """)

    option = input("Choice >> ")

    # exit
    if option == "0":
        print("Exiting the system...")
        sys.exit()

    # customer menu entry
    elif option == "1":
        customer_menu()
    # manager menu entry
    elif option == "2":
        if login():
            print()
            manager_menu()
        else:
            print("\nIncorrect username or password" \
                  "\nExiting the system...\n\n")
            sys.exit()
    else:
        print(option, "is not a valid option!\n")
        sys.exit()

# display customer menu
def customer_menu():
    option = None
    while option != "0":
        print("""
        \t=== Customer Menu ===
        (0) Exit
        (1) View all movies
        (2) View ticket prices
        (3) Search movies
        (4) Reserve tickets
        (X) Logout""")
        print()

        option = input(" >>> ")
        if option == "0":
            print("Exiting the system...\n")
        elif option == "1":
            all_movies()
            input("\nPress enter to continue.")
        elif option == "2":
            ticket_prices()
            input("\nPress enter to continue.")
        elif option == "3":
            search()
            input("\nPress enter to continue.")
        elif option == "4":
            reserve_tickets()
            input("\nPress enter to continue.")
        elif option.upper() == "X":
            main()

# display manager menu
def manager_menu():
    option = None
    while option != "0":
        print("""
        \t=== Manager Menu ===
        (0) Exit
        (1) View movie details
        (2) Add/Remove movie
        (3) Add/Remove projection
        (4) Change ticket prices
        (5) Show profit
        (X) Logout""")
        print()

        option = input(" >>> ")
        if option == "0":
            print("Exiting the system...\n")
        elif option == "1":
            all_movies()
            input("\nPress enter to continue.")
        elif option == "2":
            print("(1) Add movie")
            print("(2) Remove movie")
            choice = input("Choose what you want to do: ")
            if choice == "1":
                add_movie()
            elif choice == "2":
                movie = input("Enter the name of the movie you want to remove >> ")
                remove("movies.txt", movie)
                input("\nPress enter to continue.")
        elif option == "3":
            print("(1) Add projection")
            print("(2) Remove projection")
            choice = input("Choose what you want to do: ")
            if choice == "1":
                add_projection()
            elif choice == "2":
                projection = input("Enter the name of the movie you no longer want to show >> ")
                remove("schedule.txt", projection)
                input("\nPress enter to continue.")
        elif option == "4":
            change_ticket_prices()
        elif option == "5":
            show_profit()
        elif option.upper() == "X":
            main()

# load movies from file and store them in a dictionary
def load_movies():
    movies = {}
    file = open("movies.txt", "r")
    for line in file.readlines():
        movie_data = {}
        name, rating, duration, genre, description = line.split("|")
        movie_data["rating"] = rating
        movie_data["duration"] = duration
        movie_data["genre"] = genre
        movie_data["description"] = description
        movies[name] = movie_data

    file.close()
    return movies

# display all movies
def all_movies():
    movies = load_movies()

    print("\nCurrently showing movies:\n".upper())
    for key in movies:
        print(key)

        print(f"Rating: {movies[key]['rating']}")
        print(f"Duration: {movies[key]['duration']}")
        print(f"Genre: {movies[key]['genre']}")
        print(f"Description: {movies[key]['description']}")
        print()

# load ticket prices from file and store them in a dictionary
def load_ticket_prices():
    prices = {}
    with open("ticketprices.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            movie_type, price = line.split("|")
            prices[movie_type] = price

    return prices

# display ticket prices
def ticket_prices():
    prices = load_ticket_prices()

    print("\nTicket prices:\n".upper())
    for key in prices.keys():
        print(f"{key} movies >> {prices[key]}", end="")

    print()

# load schedule from file and store data in a dictionary
def load_schedule():
    schedule = {}

    file = open("schedule.txt", "r")
    for line in file:
        line = line.strip()
        movie, date_time_str = line.split(",")
        date_str, time_str = date_time_str.split(": ")

        if movie not in schedule:
            schedule[movie] = {}
        if date_str not in schedule[movie]:
            schedule[movie][date_str] = []
        schedule[movie][date_str].append(time_str)

    file.close()
    return schedule

# display the schedule
def display_schedule():
    schedule = load_schedule()
    print("==== Schedule ====".upper())

    for movie, date in schedule.items():
        print(f" {movie}")
        print(" Date:  ", "    Time:  ")
        print("-----------------------------------------")
        for d, t in date.items():
            result_string = ', '.join(t)
            print(d + "  ", result_string)

        print()

# reserve tickets/display reservation data/update number of sold tickets in file
def reserve_tickets():
    display_schedule()
    print()
    print("\n\nFill in with the appropriate data to reserve tickets.")
    movie_to_reserve = str(input("\nEnter the movie name >> "))
    reservation_date = str(input("Enter the show date (DD.MM.YY) >> "))
    reservation_time = str(input("Enter the show time (HH:MM) >> "))
    movie_type = input("Enter how you want to watch the movie (2D, 3D, 4D, 6D) >> ")
    number_of_tickets = int(input("Enter how many tickets you want to reserve >> "))

    ticket_prices = load_ticket_prices()
    bill = 0
    bill += number_of_tickets * int(ticket_prices[movie_type.upper()])

    print("\nYou have successfully reserved tickets!\nYour reservation details:\n",
          "\nMovie: ", movie_to_reserve, " -->  showing on ", reservation_date, "at", reservation_time, "h "
          "\nNumber of tickets: ", number_of_tickets,
          "\nMovie type: ", movie_type,
          "\nTotal to pay: ", bill, "din.")

    update_sold_tickets(movie_to_reserve, number_of_tickets, movie_type)

# movie search/display movie data
def search():
    movies = load_movies()
    input_text = input("Enter the movie name >> ")
    print()
    for movie in movies:
        if movie == input_text:
            print(f"{movie}")
            print(f"Rating: {movies[movie]['rating']}")
            print(f"Duration: {movies[movie]['duration']}")
            print(f"Genre: {movies[movie]['genre']}")
            print(f"Description: {movies[movie]['description']}")

# add movie to file
def add_movie():
    file = open("movies.txt", "a")
    more = "yes"
    while more != "":
        name = input("Enter the movie name >> ")
        rating = input("Enter the movie rating (1-10) >> ")
        duration = input("Enter the movie duration >> ")
        genre = input("Enter the movie genre >> ")
        description = input("Enter a short movie description >> ")
        line = name + "|" + rating + "|" + duration + "|" + genre + "|" + description + "\n"
        file.write(line)
        more = input("Do you want to enter more movies? Press enter to finish.")

    file.close()

# remove from file/parameters which file and what to remove
def remove(file, keyword):
    with open(file, "r") as f:
        lines = f.readlines()

    with open(file, "w") as f:
        for line in lines:
            if keyword in line:
                pass
            else:
                f.write(line)

# add projection to file
def add_projection():
    file = open("schedule.txt", "a")
    more = "yes"
    while more != "":
        movie_name = input("Enter the movie name >> ")
        date = input("Enter the projection date >> ")
        time = input("Enter the projection time >> ")
        line = movie_name + ", " + date + ": " + time + "|" + "\n"
        file.write(line)
        more = input("Do you want to enter more movies? Press enter to finish. ")

    file.close()

# change ticket prices
def change_ticket_prices():
    print("Change ticket prices".upper())
    more = "yes"
    while more != "":
        ticket_type = input("Enter the ticket type for which you want to change the price >> ")
        new_price = input("Enter the new price >>  ")

        with open("ticketprices.txt", "r") as f:
            lines = f.readlines()
        prices = load_ticket_prices()
        with open("ticketprices.txt", "w") as f:
            for line in lines:
                if ticket_type in line:
                    f.write(line.replace(prices[ticket_type], str(new_price)) + "\n")
                else:
                    f.write(line)
        more = input("Do you want to change more prices (yes / press enter to exit)?\n")

# display movie name/ticket type, how many sold for each type, and price per type
# also display total earnings for each movie
def show_profit():
    total_earnings = {}  # movie list and earnings per movie
    ticket_prices = load_ticket_prices()
    sold_tickets = load_sold_tickets()
    print("\nEarnings for sold tickets per movie\n".upper())
    for key in sold_tickets.keys():
        profit_2D = 0
        profit_2D += int(sold_tickets[key]["2D"]) * int(ticket_prices["2D"])
        profit_3D = 0
        profit_3D += int(sold_tickets[key]["3D"]) * int(ticket_prices["3D"])
        profit_4D = 0
        profit_4D += int(sold_tickets[key]["4D"]) * int(ticket_prices["4D"])
        profit_6D = 0
        profit_6D += int(sold_tickets[key]["6D"]) * int(ticket_prices["6D"])
        total = profit_2D + profit_3D + profit_4D + profit_6D
        print(f"Movie: {key}")
        print("Number of tickets sold: ")
        print(f"2D - {sold_tickets[key]['2D']}| {profit_2D} din.")
        print(f"3D - {sold_tickets[key]['3D']}| {profit_3D} din.")
        print(f"4D - {sold_tickets[key]['4D']}| {profit_4D} din.")
        print(f"6D - {sold_tickets[key]['6D']}| {profit_6D} din.\n")
        total_earnings[key] = total

    print("Total earnings per movie\n".upper())
    for key, value in total_earnings.items():
        print(key, " >> ", value, "din.")
    print()

    labels = list(total_earnings.keys())
    values = list(total_earnings.values())

    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Earnings per movie")
    plt.show()
    print()

if __name__ == "__main__":
    main()
