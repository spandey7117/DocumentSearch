import psycopg2


def get_user_detail(id):
    conn = psycopg2.connect(
        dbname="template1",
        user="naardic",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(
        "Select c.id, c.email, c.created_at, c.first_name, c.last_name, c.phone, c.gender, c.dob, c.height, c.weight from customers c WHERE c.id = "+str(id))
    rows = cur.fetchone()
    if rows[6] == 2:
        sex = "female"
    else:
        sex = "male"
    data1 = "name of the customer is " + str(rows[3]) + " " + str(
        rows[4]) + ", customer id for this customer is " + str(
        rows[0]) + ". Customer is a " + sex + " , customer weight is " + str(rows[9]) + " KG and height is " + str(
        rows[8]) + " CM. Customer date of Birth is :" + str(rows[7]) + ". Customer Joined Naardic on " + str(
        rows[2]) + ". Customer Email Id and Phone number are : " + str(rows[1]) + " and " + str(rows[5]) + "."
    cur.execute(
        "Select b.klass_id,b.customer_id, b.attendance, k.id, k.name_nb, k.start_at, k.trainer_id, k.duration from customers c JOIN bookings b ON c.id = b.customer_id JOIN klasses k ON b.klass_id = k.id WHERE c.id = "+str(id)+" ORDER BY k.start_at LIMIT 3")
    # cur.execute("Select c.id, c.email, c.created_at, c.first_name, c.last_name, c.phone, c.gender, c.dob, c.height, c.weight, b.status, b.klass_id,b.customer_id, b.attendance, k.id, k.start_at, k.trainer_id, k.duration  FROM customers c JOIN bookings b ON c.id = b.customer_id JOIN klasses k ON b.klass_id = k.id WHERE c.email = 'lise.ellis@gmail.com' ORDER BY k.start_at DESC LIMIT 3")
    rows = cur.fetchall()
    data1 = data1 + "Last 3 classes of this customers are as follows.\n"
    for row in rows:
        if row[2] == "False":
            attendance_status = "did not "
        else:
            attendance_status = ""
        data2 = "Class is having class id: " + str(row[0]) + ", class name " + str(
            row[4]) + ", class start time " + str(
            row[5]) + ", class trainer id  " + str(row[6]) + " Customer " + attendance_status + "attented this class. \n"
        data1 = data1 + data2
    return data1
