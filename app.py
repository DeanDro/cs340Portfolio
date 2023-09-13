

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Importing file with additional methods
import helper_functions.cards_rooms_reservations as helpers
import helper_functions.customers_discounts_reser as support_functions


app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_drososk"
app.config["MYSQL_PASSWORD"] = "OSUCODE"
app.config["MYSQL_DB"] = "cs340_drososk"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# have homepage route to the homepage with description about each entity.
@app.route("/")
def home():
    return render_template('home.j2')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# route for customers page
@app.route("/customers", methods=["POST", "GET"])
def customers():

    # separate function for a POST
    # insert a customer into the customers entity
    if request.method == "POST":

        # fire off if user presses the Add Person button
        if request.form.get("input_customer"):
            # grab user form inputs
            customer_first_name = request.form["first_name"]
            customer_last_name = request.form["last_name"]
            address = request.form["address"]
            country = request.form["country"]
            zip_code = request.form["zip_code"]
            phone = request.form["phone"]
            credit_card_number= request.form["credit_card"]
            credit_card_security = request.form["security_number"]
            days_stayed = request.form["total_days"]
            total_spent = request.form["total_spent"]
            special_request = request.form["special_request"]

            if credit_card_number != '' and credit_card_security != '':

                # First the account has to create an instance of credit card.
                cc_ins = "INSERT INTO Credit_Cards (Credit_Card_Number, Credit_Card_Security_Number) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(cc_ins, (credit_card_number, credit_card_security,))
                mysql.connection.commit()

                # mySQL query to insert a new customer into Customers with our form inputs
                ins_1 = "INSERT INTO Customers (Credit_Card_ID, Customer_First_Name, Customer_Last_Name, Address, Country, Zip_Code, Phone, "
                ins_2 = "Total_Days_Stayed, Total_Spent, Special_Request) VALUES ( (SELECT Credit_Card_ID FROM Credit_Cards WHERE Credit_Card_Number= %s), %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                final_insert = ins_1 + ins_2
                cur = mysql.connection.cursor()
                cur.execute(final_insert, (credit_card_number, customer_first_name, customer_last_name, address, country, zip_code,
                            phone, days_stayed, total_spent, special_request,))
                mysql.connection.commit()

            else:
                 # mySQL query to insert a new customer into Customers with our form inputs
                ins_1 = "INSERT INTO Customers (Customer_First_Name, Customer_Last_Name, Address, Country, Zip_Code, Phone, "
                ins_2 = "Total_Days_Stayed, Total_Spent, Special_Request) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                final_insert = ins_1 + ins_2
                cur = mysql.connection.cursor()
                cur.execute(final_insert, (customer_first_name, customer_last_name, address, country, zip_code,
                            phone, days_stayed, total_spent, special_request))
                mysql.connection.commit()

            # redirect back to customers page
            return redirect('/customers')

    # Grab all customers data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the customers
        query = "SELECT Customers.Customer_ID, Customers.Credit_Card_ID, Credit_Cards.Credit_Card_Number, Credit_Cards.Credit_Card_Security_Number, Customers.Customer_First_Name, Customers.Customer_Last_Name, "
        query2 = "Customers.Address, Customers.Country, Customers.Zip_Code, Customers.Phone, Customers.Total_Days_Stayed, Customers.Total_Spent, Customers.Special_Request "
        query3 = "FROM Customers LEFT JOIN Credit_Cards ON Customers.Credit_Card_ID = Credit_Cards.Credit_Card_ID;"
        final_query = query + query2 + query3
        cur = mysql.connection.cursor()
        cur.execute(final_query)
        data = cur.fetchall()

        # mySQL query to grab customers ids for our dropdown
        query2 = "SELECT Customers.Customer_ID FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customer_ids = cur.fetchall()


        return render_template("customers.j2", customer_ids=customer_ids, customers_data=data)

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# route for delete functionality, deleting a customer from Customers table,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_customers/<int:id>", methods=['GET', 'POST'])
def delete_customers(id):

    if request.method == 'POST':
        # mySQL query to delete the customer with our passed id
        query = "DELETE FROM Customers WHERE Customer_ID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

        # redirect back to customers page
        return redirect("/customers")

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# route for edit functionality, updating the attributes of a customer in Customers
# similar to our delete route, we want to the pass the 'id' value of that person on button click via the route
@app.route("/edit_customers/<int:id>", methods=["POST", "GET"])
def edit_customers(id):

    if request.method == "GET":

        # mySQL query to grab the info of the customer with our passed id
        query = "SELECT * FROM Customers WHERE Customer_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Get all Credit Cards foreign keys and add null so you can set the foreign key value for credit cards to null
        query = "SELECT * FROM Credit_Cards"
        cur = mysql.connection.cursor()
        cur.execute(query)
        cc_keys = cur.fetchall()

        # Converts tuples to list
        credit_cards_list = []
        credit_cards_list.append('Null')
        for card in cc_keys:
            credit_cards_list.append(card)

        # render edit_customers page passing our query data
        return render_template("edit_customers.j2", data=data, cc_ids=credit_cards_list)

    # Update Value
    if request.method == "POST":

        if request.form.get("edit_form"):

            # grab user form inputs
            customer_id = request.form["customer_id_edit"]
            customer_first_name = request.form["customer_first_name"]
            customer_last_name = request.form["customer_last_name"]
            address = request.form["address"]
            country = request.form["country"]
            zip_code = request.form["zip_code"]
            phone = request.form["phone"]
            credit_card_id = request.form["credit_card_id"]
            days_stayed = request.form["total_days"]
            total_spent = request.form["total_spent"]
            special_request = request.form["special_request"]

            # Update Customer if credit card is not null
            if credit_card_id != '':
                customer_update1 = "UPDATE Customers SET Customers.Credit_Card_ID = %s, Customers.Customer_First_Name = %s, Customers.Customer_Last_Name = %s, Customers.Address = %s, "
                customer_update2 = "Customers.Country = %s, Customers.Zip_Code = %s, Customers.Phone = %s, Customers.Total_Days_Stayed = %s, Customers.Total_Spent = %s, Customers.Special_Request = %s "
                customer_update3 = "WHERE Customers.Customer_ID = %s;"
                final_update_query = customer_update1 + customer_update2 + customer_update3
                cur = mysql.connection.cursor()
                cur.execute(final_update_query, (credit_card_id, customer_first_name, customer_last_name, address, country, zip_code,
                            phone, days_stayed, total_spent, special_request, customer_id))
                mysql.connection.commit()

            else:
                customer_update1 = "UPDATE Customers SET Customers.Credit_Card_ID = NULL, Customers.Customer_First_Name = %s, Customers.Customer_Last_Name = %s, Customers.Address = %s, "
                customer_update2 = "Customers.Country = %s, Customers.Zip_Code = %s, Customers.Phone = %s, Customers.Total_Days_Stayed = %s, Customers.Total_Spent = %s, Customers.Special_Request = %s "
                customer_update3 = "WHERE Customers.Customer_ID = %s;"
                final_update_query = customer_update1 + customer_update2 + customer_update3
                cur = mysql.connection.cursor()
                cur.execute(final_update_query, (customer_first_name, customer_last_name, address, country, zip_code,
                            phone, days_stayed, total_spent, special_request, customer_id))
                mysql.connection.commit()


            # Return to the customers page
            return redirect('/customers')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
@app.route("/search_customers", methods=['GET', 'POST'])
def search_customers():
    # It is used in dynamic search to look for a customer
    if request.method == "POST":

        if request.form.get('start_search'):

            cust_search_id = request.form['customer_id_search']

            # Check if it comes from the dynamic search request
            search_query = "SELECT * FROM Customers WHERE Customers.Customer_ID = %s" % (cust_search_id)
            cur = mysql.connection.cursor()
            cur.execute(search_query)
            data = cur.fetchall()

            return render_template('search_customers.j2', data=data)

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
@app.route("/discounts_has_reservations", methods=["GET", "POST"])
def discounts_has_reservations():
    # Route to the intersection table for discounts has reservations

    if request.method == "GET":

        # mySQL query to grab all the data from discounts_has_reservations
        query = "SELECT Discounts_has_Reservations.Discounts_has_Reservations_ID, Reservations.Reservation_ID, Reservations.Date_Reservation_Starts, "
        query2 = "Reservations.Date_Reservation_Ends, Reservations.Total_Nights_Cost, Discounts.Discount_ID, Discounts.Discount_Rate, Discounts.Active "
        query3 = "FROM Discounts_has_Reservations LEFT JOIN Reservations ON Discounts_has_Reservations.Reservation_ID = Reservations.Reservation_ID "
        query4 = "LEFT JOIN Discounts ON Discounts_has_Reservations.Discount_ID = Discounts.Discount_ID;"
        final_query = query + query2 + query3 + query4
        cur = mysql.connection.cursor()
        cur.execute(final_query)
        data = cur.fetchall()

        # mysql query to collect all existing reservation_ids and discounts_ids to prepopulate the
        # values in the add statement
        discounts_query = "SELECT Discounts.Discount_ID FROM Discounts"
        cur = mysql.connection.cursor()
        cur.execute(discounts_query)
        discount_ids = cur.fetchall()

        reservations_query = "SELECT Reservations.Reservation_ID FROM Reservations"
        cur = mysql.connection.cursor()
        cur.execute(reservations_query)
        reservation_ids = cur.fetchall()

        # render reservations_has_discounts page to pass all data
        return render_template("discounts_has_reservations.j2", data=data, discounts=discount_ids, reservations=reservation_ids)

    # POST method for add new discounts_has_reservations
    if request.method == "POST":

        # fire off if user presses the Add Discount - Reservation button
        if request.form.get("input_disc_reserv"):
            # grab user form inputs
            discount_id = request.form["discount_id"]
            reservation_id = request.form["reservation_id"]

            # If all inputs have a value
            if discount_id != '' and reservation_id != '':

                cc_ins = "INSERT INTO Discounts_has_Reservations (Discount_ID, Reservation_ID) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(cc_ins, (discount_id, reservation_id,))
                mysql.connection.commit()

            # In case we don't have a Reservation_ID
            if discount_id != '' and reservation_id == '':
                cc_ins = "INSERT INTO Discounts_has_Reservations (Discount_ID) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(cc_ins, (discount_id,))
                mysql.connection.commit()

            # In case we don't have a Discount_ID
            if discount_id == '' and reservation_id !='':
                cc_ins = "INSERT INTO Discounts_has_Reservations (Reservation_ID) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(cc_ins, (reservation_id,))
                mysql.connection.commit()

        # redirect back to discounts_has_reservations
        return redirect('/discounts_has_reservations')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
@app.route("/edit_discounts_reservations/<int:id>", methods=["GET", "POST"])
def edit_discounts_reservations(id):

    # Method to complete the Update functionality of the CRUD operation for M:M relationship

    if request.method == "GET":

        # mySQL query to grab the info of the Discounts_has_Reservations records
        query = "SELECT * FROM Discounts_has_Reservations WHERE Discounts_has_Reservations_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to populate dropdown for discount ids
        discounts_query = "SELECT Discounts.Discount_ID FROM Discounts;"
        cur = mysql.connection.cursor()
        cur.execute(discounts_query)
        discounts = cur.fetchall()

        # Query to populate dropdown for Reservation ids
        reservations_query = "SELECT Reservations.Reservation_ID FROM Reservations;"
        cur = mysql.connection.cursor()
        cur.execute(reservations_query)
        reservations = cur.fetchall()

        # render the edit page
        return render_template("edit_discounts_reservations.j2", data=data, discounts=discounts, reservations=reservations)

    # Update Value
    if request.method == "POST":

        if request.form.get("edit_form"):

            # grab user form inputs
            discount_reservation_id = request.form["discount_reservation_id"]
            discount_id = request.form["Discount_id"]
            reservation_id = request.form["Reservation_id"]

            # Update discounts_has_reservations if discount_id is null
            if discount_id == '' and reservation_id != '':
                cur = mysql.connection.cursor()
                support_functions.update_discount_reservation_null_discount(cur, discount_reservation_id, reservation_id)
                mysql.connection.commit()

            # if reservation_id is null
            if discount_id != '' and reservation_id == '':
                cur = mysql.connection.cursor()
                support_functions.update_discount_reservation_null_reservation(cur, discount_reservation_id, discount_id)
                mysql.connection.commit()

            # if both reservation id and discount id are null
            if discount_id == '' and reservation_id == '':
                cur = mysql.connection.cursor()
                support_functions.update_discount_reservation_null_reservation_discount(cur, discount_reservation_id)
                mysql.connection.commit()

            # If no information are missing
            if discount_id != '' and reservation_id != '':
                cur = mysql.connection.cursor()
                support_functions.update_discounts_reservations_full_details(cur, discount_reservation_id, discount_id, reservation_id)
                mysql.connection.commit()

        # Return to the customers page
        return redirect('/discounts_has_reservations')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Method for deleting a discounts_has_reservations instance
@app.route("/delete_discount_reservation/<int:id>", methods=['GET', 'POST'])
def delete_discount_reservation(id):

    if request.method == 'POST':
        # mySQL query to delete the discount_reservation with our passed id
        query = "DELETE FROM Discounts_has_Reservations WHERE Discounts_has_Reservations_ID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

        # redirect back to discounts_has_reservations page
        return redirect("/discounts_has_reservations")

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Method to get the Credit Cards entity
@app.route('/credit_cards', methods=["GET", "POST"])
def credit_cards():
    # Route to the Credit Cards table

    if request.method == "GET":

        # Create connection with the database and pass it as an argument
        cur = mysql.connection.cursor()
        credit_cards_data = helpers.return_credit_cards(cur)
        return render_template('/credit_cards.j2', credit_cards_data=credit_cards_data)

    if request.method == "POST":

        # If it is an insert request
        if request.form.get('input_credit_card'):

            credit_card_number = request.form["credit_number"]
            credit_card_security_number = request.form["credit_security_number"]

            # Call helper method to handle the insert
            cur = mysql.connection.cursor()
            helpers.create_credit_card(cur, credit_card_number, credit_card_security_number)
            mysql.connection.commit()

            return redirect('/credit_cards')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route for handling the delete of a credit card record
@app.route('/delete_credit_card/<int:id>', methods=["GET", "POST"])
def delete_credit_card(id):
    """
    Gets the id of the credit card from the request and deletes it from the database. Uses helper method
    delete_credit_card that exists in the /helper_functions/cards_rooms_reservations.py
    """

    if request.method == "POST":

        cur = mysql.connection.cursor()
        helpers.delete_credit_card(cur, id)
        mysql.connection.commit()

        return redirect('/credit_cards')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route for handling edit credit cards
@app.route('/edit_credit_card/<int:id>', methods=["GET", "POST"])
def edit_credit_card(id):
    """
    Handles the edit credit card request from the database.
    """
    if request.method == "GET":

        # Get all the information for the edited credit card
        cur = mysql.connection.cursor()
        credit_card_details = helpers.get_requested_credit_card(cur, id)

        return render_template('edit_credit_card.j2', data=credit_card_details)

    if request.method == "POST":

        credit_card_number = request.form["credit_number"]
        credit_security_number = request.form["credit_security"]

        cur = mysql.connection.cursor()
        helpers.update_credit_card(cur, id, credit_card_number, credit_security_number)
        mysql.connection.commit()

        return redirect('/credit_cards')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route for the Rooms entity
@app.route('/rooms', methods=["GET", "POST"])
def rooms():
    """
    Method that returns the rooms page.
    """

    if request.method == "GET":

        cur = mysql.connection.cursor()
        all_rooms = helpers.get_all_rooms(cur)
        return render_template('rooms.j2', rooms=all_rooms)

    if request.method == "POST":

        if request.form.get("input_room"):

            room_size = request.form["room_size"]
            room_type = request.form["room_type"]
            room_number = request.form["room_number"]
            room_availability = request.form["room_availability"]
            room_floor = request.form["room_floor"]
            room_rate = request.form["room_rate"]

            # Calling the helper methods to input the new room instance
            cur = mysql.connection.cursor()
            helpers.insert_new_room(cur, room_size, room_type, room_number, room_availability, room_floor, room_rate)
            mysql.connection.commit()

            return redirect('/rooms')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route for handlng the edit room path
@app.route('/edit_room/<int:id>', methods=["GET", "POST"])
def edit_room(id):
    """
    Method to handle the edit request for a room.
    """
    if request.method == "GET":

        # Handle the edit page when the page is first loaded
        cur = mysql.connection.cursor()
        room_data = helpers.get_room_details(cur, id)

        return render_template('edit_room.j2', data=room_data)

    if request.method == "POST":

        # Handle when the user updates the information for a room
        room_id = request.form["room_id"]
        room_size = request.form["room_size"]
        room_type = request.form["room_type"]
        room_number = request.form["room_number"]
        room_availability = request.form["room_availability"]
        room_floor = request.form["room_floor"]
        room_rate = request.form["room_rate"]

        cur = mysql.connection.cursor()
        helpers.update_room(cur, room_id, room_size, room_type, room_number, room_availability, room_floor, room_rate)
        mysql.connection.commit()

        return redirect('/rooms')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route for delete edit_room
@app.route('/delete_room/<int:id>', methods=["GET", "POST"])
def delete_room(id):
    """
    Delete the room that is selected by the user.
    """
    if request.method == "POST":

        cur = mysql.connection.cursor()
        helpers.delete_room(cur, id)
        mysql.connection.commit()

        return redirect('/rooms')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route for the Reservations entity
@app.route('/reservations', methods=["GET", "POST"])
def reservations():
    """
    Method to return the resevations entity and to handle the new entry of a reservation.
    """

    if request.method == "GET":

        # Load all reservations
        cur = mysql.connection.cursor()
        all_reservations = helpers.full_reservation_details(cur)

        # Load all customer ids and a Null value for setting foreign key to null
        cur2 = mysql.connection.cursor()
        all_customers = helpers.get_all_customers(cur2)
        all_customers_list = ['Null']
        for customer in all_customers:
            all_customers_list.append(customer)

        # Load all room ids and add a null value for setting the foreign key value to null
        cur3 = mysql.connection.cursor()
        all_rooms = helpers.get_all_rooms(cur3)
        all_rooms_list = ['Null']
        for room in all_rooms:
            all_rooms_list.append(room)

        return render_template('reservations.j2', reservations=all_reservations, customers=all_customers_list, rooms=all_rooms_list)

    if request.method == "POST":

        # Collect data
        customer_id = request.form["customer_id"]
        room_id = request.form["room_id"]
        reservation_start = request.form["reservation_start"]
        reservation_end = request.form["reservation_ends"]
        total_cost = request.form["total_cost"]
        pending_payment = request.form["pending_payment"]

        # add the null option for foreign keys for room id and customer id in the insert query
        cur = mysql.connection.cursor()
        if room_id != '' and customer_id != '':
            helpers.insert_reservation(cur, customer_id, room_id, reservation_start, reservation_end, total_cost, pending_payment)
        elif room_id != '' and customer_id == '':
            helpers.insert_reservation_null_customer(cur, room_id, reservation_start, reservation_end, total_cost, pending_payment)
        elif room_id == '' and customer_id != '':
            helpers.insert_reservation_null_room(cur, customer_id, reservation_start, reservation_end, total_cost, pending_payment)
        elif room_id == '' and customer_id == '':
            helpers.insert_reservation_null_customer_room(cur, reservation_start, reservation_end, total_cost, pending_payment)
        mysql.connection.commit()

        return redirect('/reservations')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route to handle the edit of reservations
@app.route('/edit_reservation/<int:id>', methods=["GET", "POST"])
def edit_reservation(id):
    """
    Handle the edit of a reservation.
    """

    if request.method == "GET":

        # get reservation, customer and rooms
        cur = mysql.connection.cursor()
        reservation_details = helpers.get_reservation_details(cur, id)

        # Get all customer ids and also add the null value for eding the nullable relationship of a foreign key
        cur2 = mysql.connection.cursor()
        customers = helpers.get_all_customers(cur2)
        customers_list = []
        customers_list.append('Null')
        for customer in customers:
            customers_list.append(customer)

        # Get all rooms and add the null value for the room_id foreign key
        cur3 = mysql.connection.cursor()
        rooms = helpers.get_all_rooms(cur3)
        rooms_list = ['Null']
        for room in rooms:
            rooms_list.append(room)

        return render_template('edit_reservation.j2', data=reservation_details, customers=customers_list, rooms=rooms_list)

    if request.method == "POST":

        # collect data and execute update
        reservation_id = request.form["reservation_id"]
        customer_id = request.form["customer_id"]
        room_id = request.form["room_id"]
        reservation_starts = request.form["reservation_starts"]
        reservation_ends = request.form["reservation_ends"]
        total_cost = request.form["total_cost"]
        pending_payment = request.form["pending_payment"]
        cur = mysql.connection.cursor()

        # Update reservation if no foreign keys are null or if any of them is null
        if customer_id != '' and room_id != '':
            helpers.update_reservation(cur, reservation_id, customer_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment)
        elif customer_id == '' and room_id != '':
            helpers.update_reservation_null_customer(cur, reservation_id, room_id, reservation_starts, reservation_ends, total_cost, pending_payment)
        elif customer_id != '' and room_id == '':
            helpers.update_reservation_null_room(cur, reservation_id, customer_id, reservation_starts, reservation_ends, total_cost, pending_payment)
        elif customer_id == '' and room_id == '':
            helpers.update_reservation_null_room_customer(cur, reservation_id, reservation_starts, reservation_ends, total_cost, pending_payment)

        mysql.connection.commit()

        return redirect('/reservations')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route to handle the Delete of a reservation
@app.route('/delete_reservation/<int:id>', methods=["GET", "POST"])
def delete_reservation(id):
    """
    Handle the delete function of a reservation
    """

    if request.method == "POST":
        cur = mysql.connection.cursor()
        helpers.delete_reservation(cur, id)
        mysql.connection.commit()

        return redirect('/reservations')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route to return the Discounts entity and to handle the Insert
@app.route('/discounts', methods=["GET", "POST"])
def discounts():
    """
    Method to handle the return of discounts entity and the creation of a new discounts record.
    """

    if request.method == "GET":

        # Make a connection to database and retrieve all discounts data.
        cur = mysql.connection.cursor()
        discounts = helpers.return_all_discounts(cur)

        return render_template('discounts.j2', discounts=discounts)

    if request.method == "POST":

        # Make a connection to the database, collect data and handle the insert of a new record in the database
        discount_rate = request.form["discount_rate"]
        combined_with_other = request.form["combined_with_other"]
        active = request.form["active_discount"]

        cur = mysql.connection.cursor()
        helpers.insert_discount(cur, discount_rate, combined_with_other, active)
        mysql.connection.commit()

        return redirect('/discounts')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route to handle the edit of an existing discount
@app.route('/edit_discount/<int:id>', methods=["GET", "POST"])
def edit_discount(id):
    """
    Handles the route for updating an existing discount record.
    """

    if request.method == "GET":

        cur = mysql.connection.cursor()
        discount_details = helpers.get_discount_details(cur, id)

        return render_template('edit_discount.j2', data=discount_details)

    if request.method == "POST":
        # Retrive the data, set connection with database and update record

        discount_rate = request.form["discount_rate"]
        combined = request.form["combined_with_other"]
        active_discount = request.form["active_discount"]

        cur = mysql.connection.cursor()
        helpers.update_discount(cur, id, discount_rate, combined, active_discount)
        mysql.connection.commit()

        return redirect('/discounts')

# Citation for the following function:
# Date: 6/6/2022
# Based on code from Dr. Michael Curry
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# Route to handle the delete_discount path
@app.route('/delete_discount/<int:id>', methods=["GET", "POST"])
def delete_discount(id):
    """
    Handles the delete discount request
    """
    if request.method == "POST":

        cur = mysql.connection.cursor()
        helpers.delete_discount(cur, id)
        mysql.connection.commit()

        return redirect('/discounts')

# Listener
if __name__ == "__main__":
    app.run(port=9532, debug=True)
