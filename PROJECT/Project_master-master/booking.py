from datetime import datetime

class Bus:
    def __init__(self, license_plate, bus_name, capacity):
        self.__license_plate = license_plate
        self.__bus_name = bus_name
        self.__capacity = capacity
        self.__available_seat = capacity
        self.__seat_list = list(range(1, capacity + 1))  

    @property
    def license_plate(self):
        return self.__license_plate

    @property
    def bus_name(self):
        return self.__bus_name

    @property
    def available_seat(self):
        return self.__available_seat

    @property
    def seat_list(self):
        return self.__seat_list

    def book_seat_by_number(self, seat_number):
        if seat_number in self.__seat_list:
            self.__seat_list.remove(seat_number)
            self.__available_seat -= 1
            return True
        return False

    def is_available(self):
        return self.__available_seat > 0

class Schedule:
    def __init__(self, schedule_id, route, ticket_price):
        self.__schedule_id = schedule_id
        self.__route = route
        self.__ticket_price = ticket_price
        self.__buses = []

    @property
    def schedule_id(self):
        return self.__schedule_id

    @property
    def route(self):
        return self.__route

    @property
    def ticket_price(self):
        return self.__ticket_price

    @property
    def buses(self):
        return self.__buses

    def add_bus(self, bus):
        self.__buses.append(bus)

    def has_available_bus(self):
        return any(bus.is_available() for bus in self.__buses)

class Account:
    user_id_counter = 1

    def __init__(self, user_id, user_name, password):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__password = password
        self.__bookings = []

    @property
    def user_id(self):
        return self.__user_id

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def bookings(self):
        return self.__bookings

class Customer(Account):
    def __init__(self, user_name, password):
        user_id = f"U{Account.user_id_counter}"
        super().__init__(user_id, user_name, password)
        Account.user_id_counter += 1

class Booking:
    def __init__(self, customer, bus, seat_number):
        self.__customer = customer
        self.__bus = bus
        self.__seat_number = seat_number
        self.__status = "Pending"

    @property
    def customer(self):
        return self.__customer

    @property
    def bus(self):
        return self.__bus

    @property
    def seat_number(self):
        return self.__seat_number

    @property
    def status(self):
        return self.__status

    def confirm_booking(self):
        if self.__bus.book_seat_by_number(self.__seat_number):
            self.__status = "Confirmed"
            return True
        return False

class Ticket:
    def __init__(self, booking):
        self.__booking = booking
        self.__ticket_id = f"T-{booking.customer.user_id}-{booking.seat_number}"
        self.__issued_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def booking(self):
        return self.__booking

    @property
    def ticket_id(self):
        return self.__ticket_id

    @property
    def issued_date(self):
        return self.__issued_date

class Payment:
    def __init__(self, booking, amount):
        self.__booking = booking
        self.__amount = amount
        self.__status = "กำลังดำเนินการ"

    @property
    def booking(self):
        return self.__booking

    @property
    def amount(self):
        return self.__amount

    @property
    def status(self):
        return self.__status

    def process_payment(self):
        self.__status = "ดำเนินการเสณ้จสิ้นแล้วค่ะ"
        return Ticket(self.__booking)
class Company:
    def __init__(self):
        self.__schedules = []
        self.__customers = []
        self.__ticket = []
    def view_ticket(self):
        if not self.__ticket:
            return ["❌ ไม่มีตั๋วที่ออกในระบบ"]

        ticket_list = []
        for ticket in self.__ticket:
            ticket_list.append(f"{ticket.ticket_id}, {ticket.booking.seat_number}, {ticket.issued_date}")
        return ticket_list

    def refund_ticket(self, customer_id, ticket_id):
        customer = next((c for c in self.__customers if c.user_id == customer_id), None)
        if not customer:
            return None, "❌ ไม่พบบัญชีลูกค้า"

        ticket = next((t for t in self.__ticket if t.ticket_id == ticket_id), None)
        if not ticket:
            return None, "❌ ไม่พบตั๋วในระบบ"
        self.__ticket.remove(ticket)
        ticket.booking.bus.seat_list.append(ticket.booking.seat_number)
        ticket.booking.bus.seat_list.sort() 
        ticket.booking._Booking__status = "Refunded"

        print(f"🔄 Refund successful! Ticket ID: {ticket.ticket_id}")
        return ticket, f"✅ คืนเงินสำเร็จ! Ticket ID: {ticket.ticket_id} ได้รับการยกเลิก"
    @property
    def schedules(self):
        return self.__schedules
    def add_ticket(self, ticket):
        existing_ticket = next((t for t in self.__ticket if t.ticket_id == ticket.ticket_id), None)
        if not existing_ticket:
            self.__ticket.append(ticket)
    def get_bus(self, schedule_id, bus_plate):
        schedule = next((s for s in self.__schedules if s.schedule_id == schedule_id), None)
        if not schedule:
            return None
        cleaned_bus_plate = bus_plate.replace("%20", " ").strip()
        return next((b for b in schedule.buses if b.license_plate == cleaned_bus_plate), None)

    def add_schedule(self, schedule):
        existing_schedule = next((s for s in self.__schedules if s.schedule_id == schedule.schedule_id), None)
        if not existing_schedule:
            self.__schedules.append(schedule)

    def add_bus_to_schedule(self, schedule_id, license_plate, bus_name, capacity):
        schedule = self.schedule_select(schedule_id)
        if schedule:
            bus = Bus(license_plate, bus_name, capacity)
            schedule.add_bus(bus)

    def book_seat(self, customer_id, schedule_id, bus_plate, seat_number):
        customer = next((c for c in self.__customers if c.user_id == customer_id), None)
        bus = self.get_bus(schedule_id, bus_plate)

        if not customer or not bus:
            return "❌ Booking failed"

        if bus.book_seat_by_number(seat_number):
            booking = Booking(customer, bus, seat_number)
            ticket = Ticket(booking)
            customer.bookings.append(booking)
            return f"✅ Seat {seat_number} booked successfully! Ticket ID: {ticket.ticket_id}"
        else:
            return "❌ Seat already booked"

    def get_customer_by_name(self, user_name):
        return next((c for c in self.__customers if c.user_name == user_name), None)

    def authenticate(self, user_name, password):
        return next((c for c in self.__customers if c.user_name == user_name and c.password == password), None)

    def add_customer(self, user_name, password):
        if self.get_customer_by_name(user_name):
            return None  
        new_customer = Customer(user_name, password)
        self.__customers.append(new_customer)
        return new_customer.user_id

    def schedule_select(self, schedule_id=None, bus_plate=None):
        if schedule_id:
            return next((s for s in self.__schedules if s.schedule_id == schedule_id), None)
        elif bus_plate:
            return next((s for s in self.__schedules if any(b.license_plate == bus_plate for b in s.buses)), None)
        return None
    def process_payment(self, customer_id, seat_number):
        customer = next((c for c in self.__customers if c.user_id == customer_id), None)
        if not customer:
            return None, "❌ ไม่พบบัญชีลูกค้า"
        booking = next((b for b in customer.bookings if b.seat_number == int(seat_number)), None)
        if not booking:
            return None, "❌ ไม่พบการจอง"
        existing_ticket = next((t for t in self.__ticket if t.booking.seat_number == int(seat_number)), None)
        if existing_ticket:
            return None, f"❌ ตั๋วนี้ถูกชำระเงินไปแล้ว (Ticket ID: {existing_ticket.ticket_id})"
        schedule = self.schedule_select(bus_plate=booking.bus.license_plate)
        if not schedule:
            return None, "❌ ไม่พบตารางเดินรถ"
        amount = schedule.ticket_price
        payment = Payment(booking, amount)
        ticket = payment.process_payment()
        if not ticket:
            return None, "❌ ไม่สามารถออกตั๋วได้"
        self.add_ticket(ticket)  

        return ticket, f"✅ การชำระเงินเสร็จสิ้น! Ticket ID: {ticket.ticket_id}"
    