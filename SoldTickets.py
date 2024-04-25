# -*- coding: utf-8 -*-

# Loads the sold tickets data for each film
def load_sold_tickets():
    sold_tickets = {}
    with open("soldtickets.txt", "r") as f:
        for line in f:
            film, k2D, k3D, k4D, k6D = line.split(",")
            sold_tickets[film] = {"2D": int(k2D), "3D": int(k3D), "4D": int(k4D), "6D": int(k6D)}
    return sold_tickets

# Updates the count of sold tickets for a specific film and ticket type
def update_sold_tickets(film, num_tickets, ticket_type):
    sold_tickets = load_sold_tickets()
    if film in sold_tickets:
        sold_tickets[film][ticket_type] += num_tickets
    else:
        sold_tickets[film] = {"2D": 0, "3D": 0, "4D": 0, "6D": 0}
        sold_tickets[film][ticket_type] = num_tickets

    with open("soldtickets.txt", "w") as f:
        for film, ticket_info in sold_tickets.items():
            line = f"{film},{ticket_info['2D']},{ticket_info['3D']},{ticket_info['4D']},{ticket_info['6D']}\n"
            f.write(line)
