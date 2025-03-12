from booking import Company,Bus,Schedule
company = Company()
schedules_data = [
    ("S1", "Bangkok - Phuket", 600),
    ("S2", "Phuket - Bangkok", 786),
    ("S3", "Bangkok - Krabi", 767),
    ("S4", "Krabi - Bangkok", 767),
    ("S5", "Bangkok - Mae Sot", 459),
    ("S6", "Mae Sot - Bangkok", 459),
    ("S7", "Bangkok - Chiang Mai", 651),
    ("S8", "Chiang Mai - Bangkok", 651),
    ("S9", "Bangkok - Sukhothai", 400),
    ("S10", "Sukhothai - Bangkok", 400),
    ("S11", "Bangkok - Phetchabun", 372),
    ("S12", "Phetchabun - Bangkok", 372),
    ("S13", "Bangkok - Trat", 315),
    ("S14", "Trat - Bangkok", 315),
    ("S15", "Bangkok - Chiang Rai", 712),
    ("S16", "Chiang Rai - Bangkok", 712),
    ("S17", "Bangkok - Surat Thani", 611),
    ("S18", "Surat Thani - Bangkok", 611),
    ("S19", "Bangkok - Ranong", 538),
    ("S20", "Ranong - Bangkok", 538),
]
buses_data = [
    ("กพ 289 กรุงเทพ", "รถธรรมดา", 10),
    ("กท 123 กรุงเทพ", "รถวีไอพี", 20),
    ("นค 456 นครราชสีมา", "รถปรับอากาศ", 15),
]
for schedule_id, route, price in schedules_data:
    schedule = Schedule(schedule_id, route, price)  #

    for plate, name, cap in buses_data:
        bus = Bus(plate, name, cap)  
        schedule.add_bus(bus)  

    company.add_schedule(schedule)  

# ตรวจสอบว่ารถบัสถูกเพิ่มจริงหรือไม่
print(f"📌 Total schedules: {len(company.schedules)}")  
for s in company.schedules:
    print(f"🚌 {s.schedule_id}: {s.route} (Price: {s.ticket_price} Baht, Buses: {len(s.buses)})")
