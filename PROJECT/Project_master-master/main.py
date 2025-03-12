from datetime import datetime
from fasthtml.common import *
from create_instance import company
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app, rt = fast_app()
session = {}
app.mount("/static", StaticFiles(directory="./static"), name="static")

@rt("/")
def home():
    user_name = session.get("user_name")
    if user_name:
        return Html(
            Head(
                Link(rel="stylesheet", href="/static/styles.css")
            ),
            Body(
                Main(
                    Header(
                        H1(f"Welcome, {user_name} 🚌"),
                        H2("Available Bus Schedules")
                    ),
                    Table(
                        Thead(
                            Tr(
                                Th("Schedule ID"),
                                Th("Route"),
                                Th("Price"),
                                Th("Actions")
                            )
                        ),
                        Tbody(
                            *[
                                Tr(
                                    Td(s.schedule_id),
                                    Td(s.route),
                                    Td(f"{s.ticket_price} Baht"),
                                    Td(Button("Select", onclick=f"window.location.href='/select_bus?schedule_id={s.schedule_id}'"))
                                ) for s in company.schedules
                            ]
                        )
                    ),
                    Footer(
                        Button("Logout", onclick="window.location.href='/logout'", class_="contrast")
                    )
                )
            )
        )
    else:
        return Html(
            Head(
                Link(rel="stylesheet", href="/static/styles.css")
            ),
            Body(
                Main(
                    Header(
                        H1("ยินดีต้อนสู่บริษัท เห้อ บขสของเรา 🚌")
                    ),
                    Section(
                        Button("HOME"),
                        Button("LOGIN", onclick="window.location.href='/login'"),
                        Button("REGISTER", onclick="window.location.href='/register'"),
                    )
                )
            )
        )

@rt("/register")
def register():
    return Html(
        Head(Link(rel="stylesheet", href="/static/styles.css")),
        Body(
            Main(
                H2("Register"),
                Form(
                    Input(type="text", name="user_name", placeholder="Full Name", required=True),
                    Input(type="password", name="password", placeholder="Password", required=True),
                    Button("Sign Up", type="submit"),
                    method="post", action="/process_register"
                )
            )
        )
    )


@rt("/process_register")
def process_register(user_name: str = None, password: str = None):
    if not user_name or not password:
        return Html(Body(P("❌ ไม่เจอชื่อผู้ใช้หรือรหัสผ่าน"), A("Try Again", href="/register")))
    
    existing_user = company.get_customer_by_name(user_name)
    if existing_user:
        return Html(Body(P("ชื่อนี้มีคนใช้ไปแล้ว"), A("Try Again", href="/register")))
    
    user_id = company.add_customer(user_name, password)
    return Html(Body(P(f"✅ สมัครสำเร็จ ID: {user_id}"), A("Go to Login", href="/login")))

@rt("/login")
def login():
    return Html(
        Body(
            H2("Login"),
            Form(
                Input(type="text", name="user_name", placeholder="User Name", required=True),
                Input(type="password", name="password", placeholder="Password", required=True),
                Button("Login", type="submit"),
                method="post", action="/process_login"
            )
        )
    )

@rt("/process_login")
def process_login(user_name: str = None, password: str = None):
    if not user_name or not password:
        return Html(Body(P("❌ ไม่เจอชื่อผู้ใช้หรือรหัสผ่าน"), A("Try Again", href="/login")))
    
    user = company.authenticate(user_name, password)
    if user:
        session["user_name"] = user.user_name
        session["user_id"] = user.user_id
        return Html(Body(P(f"✅ Login Successful! Welcome {user.user_name}"), A("Go to Home", href="/")))
    else:
        return Html(Body(P("❌ ไม่มีชื่อและรหัสในระบบ"), A("Try Again", href="/login")))

@rt("/login")
def login():
    return Html(
        Head(Link(rel="stylesheet", href="/static/styles.css")),
        Body(
            Main(
                H2("Login"),
                Form(
                    Input(type="text", name="user_name", placeholder="User Name", required=True),
                    Input(type="password", name="password", placeholder="Password", required=True),
                    Button("Login", type="submit"),
                    method="post", action="/process_login"
                )
            )
        )
    )

@rt("/select_bus")
def select_bus(schedule_id: str = None):
    schedule = company.schedule_select(schedule_id)
    if not schedule:
        return Html(Body(P("❌ ไม่พบตารางเดินรถ!"), A("กลับหน้าหลัก", href="/")))

    return Html(
        Head(Link(rel="stylesheet", href="/static/styles.css")),
        Body(
            Main(
                H2(f"เลือกรถสำหรับเส้นทาง {schedule.route}"),
                Table(
                    Tr(Th("ชื่อรถ"), Th("นั่งว่าง"), Th("เลือก")),
                    *[
                        Tr(
                            Td(b.bus_name),
                            Td(f"{b.available_seat} seats"),
                            Td(Button("Select", onclick=f"window.location.href='/select_seat?schedule_id={schedule_id}&bus_plate={b.license_plate}'"))
                        )
                        for b in schedule.buses
                    ]
                ),
                A("ย้อนกลับ", href="/")
            )
        )
    )


@rt("/select_seat")
def select_seat(schedule_id: str = None, bus_plate: str = None):
    if "user_name" not in session:
        return Html(
            Head(Link(rel="stylesheet", href="/static/styles.css")),
            Body(P("⚠️ กรุณาล็อคอินก่อนนะ"), A("กลับหน้า Login", href="/login"))
        )

    bus = company.get_bus(schedule_id, bus_plate)
    if not bus:
        return Html(
            Head(Link(rel="stylesheet", href="/static/styles.css")),
            Body(P("❌ ไม่พบรถบัสที่คุณเลือก"), A("กลับหน้าหลัก", href="/"))
        )

    return Html(
        Head(Link(rel="stylesheet", href="/static/styles.css")),
        Body(
            Main(
                H2(f"เลือกที่นั่งสำหรับ {bus.bus_name}"),
                Table(
                    Tr(*[
                        Td(Button(str(seat), onclick=f"window.location.href='/book_seat?schedule_id={schedule_id}&bus_plate={bus_plate}&seat_number={seat}'"))
                        for seat in bus.seat_list
                    ]),
                ),
                A("ย้อนกลับ", href=f"/select_bus?schedule_id={schedule_id}")
            )
        )
    )


@rt("/book_seat")
def book_seat(schedule_id: str = None, bus_plate: str = None, seat_number: int = None):
    if "user_name" not in session:
        return Html(Body(P("⚠️ ต้องล็อคอินก่อนนะ"), A("Go to Login", href="/login")))

    customer_id = session.get("user_id")
    booking_message = company.book_seat(customer_id, schedule_id, bus_plate, seat_number)

    return Html(Body(
        P(booking_message),
        Div(A("Go to Home", href="/")),
        Div(A("Payment", href="/pay_booking"), style="margin-top: 20px;")
    ))
@rt("/pay_booking")
def pay_booking():
    """ Display payment details """
    if "user_name" not in session:
        return Html(Body(P("⚠️ กรุณาล็อคอินก่อนนะ"), A("กลับหน้า Login", href="/login")))

    customer = company.get_customer_by_name(session.get("user_name"))

    if not customer or not customer.bookings:
        return Html(Body(P("❌ ไม่มีรายการที่ต้องชำระเงิน"), A("กลับหน้าหลัก", href="/")))

    return Html(
        Body(
            H2("💰 รายการที่ต้องชำระ"),
            Table(
                Tr(Th("Bus Name"), Th("Seat Number"), Th("Amount"), Th("Action")),
                *[
                    Tr(
                        Td(booking.bus.bus_name),
                        Td(booking.seat_number),
                        Td(f"{company.schedule_select(bus_plate=booking.bus.license_plate).ticket_price} Baht"),
                        Td(Button("🛒 ชำระเงิน", onclick=f"window.location.href='/process_payment?seat_number={booking.seat_number}'"))
                    ) for booking in customer.bookings
                ]
            ),
            A("ย้อนกลับ", href="/")
        )
    )

@rt("/process_payment")
def process_payment(seat_number: int = None):
    """ ดำเนินการชำระเงิน และออกตั๋ว """
    if "user_name" not in session:
        return Html(Body(P("⚠️ กรุณาล็อคอินก่อนนะ"), A("Go to Login", href="/login")))

    customer_id = session.get("user_id")
    ticket, message = company.process_payment(customer_id, seat_number)

    if not ticket:
        return Html(Body(P(message), A("Go Back", href="/pay_booking")))

    return Html(
        Body(
            H2("✅ ชำระเงินสำเร็จ!"),
            P(f"ที่นั่ง {ticket.booking.seat_number} ได้รับการจองเรียบร้อยแล้ว"),
            P(f"🎟️ Ticket ID: {ticket.ticket_id}"),
            P(f"📅 ออกตั๋วเมื่อ: {ticket.issued_date}"),
            A("📄 ดูตั๋วของฉัน", href="/view_tickets"),
            A("🏠 กลับหน้าหลัก", href="/")
        )
    )

@rt("/refund_ticket")
def refund_ticket(ticket_id: str = None):
    """ ดำเนินการขอคืนเงิน """
    if "user_name" not in session:
        return Html(Body(P("⚠️ กรุณาล็อคอินก่อนนะ"), A("Go to Login", href="/login")))

    customer_id = session.get("user_id")
    ticket, message = company.refund_ticket(customer_id, ticket_id)

    if not ticket:
        return Html(Body(P(message), A("Go Back", href="/view_tickets")))
    remaining_tickets = company.view_ticket()
    if not remaining_tickets:
        return Html(Body(
            H2("🎟️ รายการตั๋วของฉัน"),
            P("❌ ไม่มีตั๋วที่ออกในระบบ"),
            A("🏠 กลับหน้าหลัก", href="/")
        ))

    return Html(
        Body(
            H2("✅ คืนเงินสำเร็จ!"),
            P(f"🎟️ Ticket ID: {ticket.ticket_id} ถูกยกเลิกแล้ว"),
            A("📄 ดูตั๋วของฉัน", href="/view_tickets"),
            A("🏠 กลับหน้าหลัก", href="/")
        )
    )

@rt("/view_tickets")
def view_tickets():
    """ แสดงรายการตั๋วของลูกค้า """
    if "user_name" not in session:
        return Html(Body(P("⚠️ กรุณาล็อคอินก่อนนะ"), A("Go to Login", href="/login")))

    tickets = company.view_ticket()

    if not tickets:
        return Html(Body(
            H2("🎟️ รายการตั๋วของฉัน"),
            P("❌ ไม่มีตั๋วที่ออกในระบบ"),
            A("🏠 กลับหน้าหลัก", href="/")
        ))

    return Html(
        Body(
            H2("🎟️ รายการตั๋วของฉัน"),
            Table(
                Tr(Th("Ticket ID"), Th("Seat Number"), Th("Issued Date"), Th("Action")),
                *[
                    Tr(
                        Td(ticket.split(", ")[0]),  
                        Td(ticket.split(", ")[1]), 
                        Td(ticket.split(", ")[2]),  
                        Td(Button("🔄 ขอคืนเงิน", onclick=f"window.location.href='/refund_ticket?ticket_id={ticket.split(', ')[0]}'"))
                    ) for ticket in tickets
                ]
            ),
            A("🏠 กลับหน้าหลัก", href="/")
        )
    )

serve()