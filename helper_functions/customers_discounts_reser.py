# Helper function to handle customers and discounts_has_reservations entities


from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


def update_discount_reservation_null_discount(cursor, discount_reservation_id, reservation_id):
    """
    Helper method that updates intersection table discounts has reservation if discount is null.
    """
    update_query1 = "UPDATE Discounts_has_Reservations SET Discounts_has_Reservations.Discount_ID = NULL, Discounts_has_Reservations.Reservation_ID = %s "
    update_query2 = "WHERE Discounts_has_Reservations.Discounts_has_Reservations_ID = %s;"
    final_update_query = update_query1 + update_query2
    cursor = mysql.connection.cursor()
    cursor.execute(final_update_query, (reservation_id, discount_reservation_id))

def update_discount_reservation_null_reservation(cursor, discount_reservation_id, discount_id):
    """
    Helper method to update intersection table discounts has reservations if reservation is null.
    """
    update_query1 = "UPDATE Discounts_has_Reservations SET Discounts_has_Reservations.Discount_ID = %s, Discounts_has_Reservations.Reservation_ID = NULL "
    update_query2 = "WHERE Discounts_has_Reservations.Discounts_has_Reservations_ID = %s;"
    final_update_query = update_query1 + update_query2
    cursor.execute(final_update_query, (discount_id, discount_reservation_id))

def update_discount_reservation_null_reservation_discount(cursor, discount_reservation_id):
    """
    Helper method to update intersection table discounts has reservations with both reservation and discount are null.
    """
    update_query = "UPDATE Discounts_has_Reservations SET Discounts_has_Reservations.Discount_ID = NULL, Discounts_has_Reservations.Reservation_ID = NULL "
    update_query2 = "WHERE Discounts_has_Reservations.Discounts_has_Reservations_ID = %s;"
    final_update_query = update_query + update_query2
    cursor.execute(final_update_query, (discount_reservation_id))

def update_discounts_reservations_full_details(cursor, discount_reservation_id, discount_id, reservation_id):
    """
    Helper method to update intersection table discount has reservations with all information included.
    """
    update_query1 = "UPDATE Discounts_has_Reservations SET Discounts_has_Reservations.Discount_ID = %s, Discounts_has_Reservations.Reservation_ID = %s "
    update_query2 = "WHERE Discounts_has_Reservations.Discounts_has_Reservations_ID = %s;"
    final_update_query = update_query1 + update_query2
    cursor.execute(final_update_query, (discount_id, reservation_id, discount_reservation_id))
