# -*- coding: utf-8 -*-
def login():
    print("\nLog in here")
    username = input("Username >>> ")
    password = input("Password >>> ")

    file = open("users.txt", "r")
    for line in file.readlines():
        u, p = line.split(",")
        if username == u and password == p[:-1]:
            logged = True
            break
        else:
            logged = False

    file.close()
    return logged
