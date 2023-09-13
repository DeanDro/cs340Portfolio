# File to handle Rooms, Credit Cards, Discounts and Reservations entities

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


def return_credit_cards(cursor):
    """
    Helper method that collects all the information for the credit cards entity and returns them
    in the form of a dictionary
    """
    cc_query = "SELECT Credit_Cards.Credit_Card_ID, Customers.Customer_ID, Customers.Customer_First_Name, Customers.Customer_Last_Name, "
    cc_query2 = "Credit_Cards.Credit_Card_Number, Credit_Cards.Credit_Card_Security_Number FROM Credit_Cards "
    cc_query3 = "LEFT JOIN Customers ON Credit_Cards.Credit_Card_ID = Customers.Credit_Card_ID;"
    final_query = cc_query + cc_query2 + cc_query3

    cursor.execute(final_query)
    final_data = cursor.fetchall()

    return final_data


def create_credit_card(cursor, cc_number, cc_security_number):
    """
    Helper method to create a credit card entity in the database
    """
    cc_create = "INSERT INTO Credit_Cards (Credit_Card_Number, Credit_Card_Security_Number) VALUES (%s, %s);"
    cursor.execute(cc_create, (cc_number, cc_security_number,))


def delete_credit_card(cursor, id):
    """
    Helper method that handles the deletion of a credit card record from the database. It doesn't return
    any values.
    """

    query = "DELETE FROM Credit_Cards WHERE Credit_Cards.Credit_Card_ID = '%s';"
    cursor.execute(query, (id,))

def get_requested_credit_card(cursor, id):
    """
    Helper method that returns all the details for a particular credit card
    """
    query = "SELECT * FROM Credit_Cards WHERE Credit_Cards.Credit_Card_ID = '%s';"
    cursor.execute(query, (id,))
    credit_card = cursor.fetchall()

    return credit_card


def get_all_credit_cards(cursor):
    """
    Helper method that returns all credit cards from the Credit Cards entity for the
    edit credit card.
    """

    query = "SELECT * FROM Credit_Cards;"
    cursor.execute(query)
    all_credit_cards = cursor.fetchall()

    return all_credit_cards

def update_credit_card(cursor, credit_id, credit_number, credit_security):
    """
    Helper method that updates the values of a credit card.
    """

    query = "UPDATE Credit_Cards SET Credit_Cards.Credit_Card_Number =%s, Credit_Cards.Credit_Card_Security_Number =%s "
    query2 = "WHERE Credit_Cards.Credit_Card_ID = %s;"
    final_query = query + query2

    cursor.execute(final_query, (credit_number, credit_security, credit_id, ))

def get_all_rooms(cursor):
    """
    Helper method that returns all the instances of Rooms in the database.
    """

    query = "SELECT * FROM Rooms;"
    cursor.execute(query)
    all_rooms = cursor.fetchall()

    return all_rooms

def insert_new_room(cursor, room_size, room_type, room_number, room_availability, room_floor, room_rate):
    """
    Helper method to insert a new instance of a room in the database.
    """
    query = "INSERT INTO Rooms (Room_Size, Room_Type, Number_Room, Room_Availability, Room_Floor, Flat_Rate_per_Night) "
    query2 = "VALUES (%s, %s, %s, %s, %s, %s);"
    final_query = query+query2
    cursor.execute(final_query, (room_size, room_type, room_number, room_availability, room_floor, room_rate,))

def get_room_details(cursor, id):
    """
    Method to return the data in the form of a dictionary for a room with Room_ID equal to the given parameter.
    """

    query = "SELECT * FROM Rooms WHERE Rooms.Room_ID = '%s';" % (id)
    cursor.execute(query)
    room_data = cursor.fetchall()

    return room_data

def update_room(cursor, room_id, room_size, room_type, room_number, room_availability, room_floor, room_rate):
    """
    Helper method to update the information for a Room record in the Rooms entity.
    """

    query1 = "UPDATE Rooms SET Rooms.Room_Size = %s, Rooms.Room_Type = %s, Rooms.Number_Room = %s, Rooms.Room_Availability = %s, "
    query2 = "Rooms.Room_Floor = %s, Rooms.Flat_Rate_Per_Night = %s WHERE Rooms.Room_ID = %s;"
    final_query = query1 + query2
    cursor.execute(final_query, (room_size, room_type, room_number, room_availability, room_floor, room_rate, room_id,))

def delete_room(cursor, id):
    """
    Helper method for deleting a room record from the Rooms entity.
    """
    query = "DELETE FROM Rooms WHERE Rooms.Room_ID = '%s';" % (id)
    cursor.execute(query)

def get_all_reservations(cursor):
    """
    Helper method to return all the reservations from the Reservations table.
    """

    query = "SELECT * FROM Reservations;"
    cursor.execute(query)
    all_reservations = cursor.fetchall()

    return all_reservations

def get_reservation_details(cursor, id):
    """
    Helper method that takes an id and returns the details for the reservation with the representative id.
    """
    query = "SELECT * FROM Reservations WHERE Reservations.Reservation_ID = %s;" % (id)
    cursor.execute(query)
    reservation_details = cursor.fetchall()

    return reservation_details

def get_all_customers(cursor):
    """
    Helper method to return all customers in the Customer database
    """

    query = "SELECT * FROM Customers;"
    cursor.execute(query)
    all_customers = cursor.fetchall()

    return all_customers

def insert_reservation(cursor, customer_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the insert of a new reservation in the reservations table.
    """
    query = "INSERT INTO Reservations (Reservations.Customer_ID, Reservations.Room_ID, Reservations.Date_Reservation_Starts, "
    query2 = "Reservations.Date_Reservation_Ends, Reservations.Total_Nights_Cost, Reservations.Pending_Payment) VALUES "
    query3 = "(%s, %s, %s, %s, %s, %s);"
    final_query = query + query2 + query3
    cursor.execute(final_query, (customer_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment, ))

def insert_reservation_null_customer(cursor, room_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the insert of a new reservation in the reservations table.
    """
    query = "INSERT INTO Reservations (Reservations.Customer_ID, Reservations.Room_ID, Reservations.Date_Reservation_Starts, "
    query2 = "Reservations.Date_Reservation_Ends, Reservations.Total_Nights_Cost, Reservations.Pending_Payment) VALUES "
    query3 = "(NULL, %s, %s, %s, %s, %s);"
    final_query = query + query2 + query3
    cursor.execute(final_query, (room_id, reservation_starts, reservation_ends, total_cost, pending_payment, ))

def insert_reservation_null_room(cursor, customer_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the insert of a new reservation in the reservations table.
    """
    query = "INSERT INTO Reservations (Reservations.Customer_ID, Reservations.Room_ID, Reservations.Date_Reservation_Starts, "
    query2 = "Reservations.Date_Reservation_Ends, Reservations.Total_Nights_Cost, Reservations.Pending_Payment) VALUES "
    query3 = "(%s, NULL, %s, %s, %s, %s);"
    final_query = query + query2 + query3
    cursor.execute(final_query, (customer_id, reservation_starts, reservation_ends, total_cost, pending_payment, ))

def insert_reservation_null_customer_room(cursor, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the insert of a new reservation in the reservations table.
    """
    query = "INSERT INTO Reservations (Reservations.Customer_ID, Reservations.Room_ID, Reservations.Date_Reservation_Starts, "
    query2 = "Reservations.Date_Reservation_Ends, Reservations.Total_Nights_Cost, Reservations.Pending_Payment) VALUES "
    query3 = "(NULL, NULL, %s, %s, %s, %s);"
    final_query = query + query2 + query3
    cursor.execute(final_query, (reservation_starts, reservation_ends, total_cost, pending_payment, ))


def update_reservation(cursor, reservation_id, customer_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the update of an existing reservation in the reservations entity.
    """
    query1 = "UPDATE Reservations SET Reservations.Customer_ID = %s, Reservations.Room_ID = %s, Reservations.Date_Reservation_Starts =%s, "
    query2 = "Reservations.Date_Reservation_Ends= %s, Reservations.Total_Nights_Cost= %s, Reservations.Pending_Payment=%s "
    query3 = "WHERE Reservations.Reservation_ID = %s;"
    final_query = query1 + query2 + query3
    cursor.execute(final_query, (customer_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment, reservation_id, ))

def update_reservation_null_customer(cursor, reservation_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the update of an existing reservation in the reservations entity.
    """
    query1 = "UPDATE Reservations SET Reservations.Customer_ID = NULL, Reservations.Room_ID = %s, Reservations.Date_Reservation_Starts =%s, "
    query2 = "Reservations.Date_Reservation_Ends= %s, Reservations.Total_Nights_Cost= %s, Reservations.Pending_Payment=%s "
    query3 = "WHERE Reservations.Reservation_ID = %s;"
    final_query = query1 + query2 + query3
    cursor.execute(final_query, (room_id, reservation_starts, reservation_ends, total_cost, pending_payment, reservation_id, ))

def update_reservation_null_room(cursor, reservation_id, customer_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the update of an existing reservation in the reservations entity.
    """
    query1 = "UPDATE Reservations SET Reservations.Customer_ID = %s, Reservations.Room_ID = NULL, Reservations.Date_Reservation_Starts =%s, "
    query2 = "Reservations.Date_Reservation_Ends= %s, Reservations.Total_Nights_Cost= %s, Reservations.Pending_Payment=%s "
    query3 = "WHERE Reservations.Reservation_ID = %s;"
    final_query = query1 + query2 + query3
    cursor.execute(final_query, (customer_id, reservation_starts, reservation_ends, total_cost, pending_payment, reservation_id, ))

def update_reservation_null_room_customer(cursor, reservation_id, reservation_starts, reservation_ends, total_cost, pending_payment):
    """
    Helper method to handle the update of an existing reservation in the reservations entity.
    """
    query1 = "UPDATE Reservations SET Reservations.Customer_ID = NULL, Reservations.Room_ID = NULL, Reservations.Date_Reservation_Starts =%s, "
    query2 = "Reservations.Date_Reservation_Ends= %s, Reservations.Total_Nights_Cost= %s, Reservations.Pending_Payment=%s "
    query3 = "WHERE Reservations.Reservation_ID = %s;"
    final_query = query1 + query2 + query3
    cursor.execute(final_query, (reservation_starts, reservation_ends, total_cost, pending_payment, reservation_id, ))


def delete_reservation(cursor, id):
    """
    Helper method to handle the delete of a reservation record from the database.
    """
    query = "DELETE FROM Reservations WHERE Reservations.Reservation_ID= '%s';" %(id)
    cursor.execute(query)

def return_all_discounts(cursor):
    """
    Helper method to retrieve and return all the Discounts data
    """
    query = "SELECT * FROM Discounts;"
    cursor.execute(query)
    all_discounts = cursor.fetchall()

    return all_discounts

def insert_discount(cur, discount_rate, combined_with_other, active_discount):
    """
    Helper method to insert a new discount in the entity Discounts.
    """
    query = "INSERT INTO Discounts (Discounts.Discount_Rate, Discounts.Combined_With_Other_Discounts, Discounts.Active) "
    query2 = "VALUES (%s, %s, %s);"
    final_query = query + query2
    cur.execute(final_query, (discount_rate, combined_with_other, active_discount, ))

def get_discount_details(cur, id):
    """
    Helper method to return all the details for a particular discount record.
    """
    query = "SELECT * FROM Discounts WHERE Discounts.Discount_ID= '%s';" % (id)
    cur.execute(query)
    discount_details = cur.fetchall()

    return discount_details

def update_discount(cur, discount_id, discount_rate, combined_with_other, active_discount):
    """
    Helper method to handle updating an existing discount.
    """
    query1 = "UPDATE Discounts SET Discounts.Discount_Rate = %s, Discounts.Combined_With_Other_Discounts= %s, "
    query2 = "Discounts.Active= %s WHERE Discounts.Discount_ID = %s"
    final_query = query1 + query2
    cur.execute(final_query, (discount_rate, combined_with_other, active_discount, discount_id, ))

def delete_discount(cursor, id):
    """
    Helper method to delete a record of discounts from the Discount entity
    """
    query = "DELETE FROM Discounts WHERE Discounts.Discount_ID= '%s';" %(id)
    cursor.execute(query)

def full_reservation_details(cursor):
    """
    Helper method to return all reservation details with customer information.
    """
    query1 = "SELECT Reservations.Reservation_ID, Reservations.Customer_ID, Customers.Customer_First_Name, Customers.Customer_Last_Name, "
    query2 = "Reservations.Room_ID, Rooms.Number_Room, Rooms.Room_Floor, Reservations.Date_Reservation_Starts, Reservations.Date_Reservation_Ends, "
    query3 = "Reservations.Total_Nights_Cost, Reservations.Pending_Payment FROM Reservations "
    query4 = "LEFT JOIN Customers ON Reservations.Customer_ID = Customers.Customer_ID LEFT JOIN Rooms ON Reservations.Room_ID = Rooms.Room_ID;"
    final_query = query1 + query2 + query3 + query4
    cursor.execute(final_query)
    full_reservations = cursor.fetchall()

    return full_reservations
