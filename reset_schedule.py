import json
with open("weeks_time.json", "r", encoding="utf-8") as json2_file:
    week_select = json.load(json2_file)
with open("schedule.json", "r", encoding="utf-8") as json2_file:
    data = json.load(json2_file)

days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"] #Mảng thứ
time_slots = ["7h-8h", "8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h", "17h-18h", "18h-19h", "19h-20h", "20h-21h"] # Mảng khung giờ học

for i in range(17) :
    week = "Tuần " + str(i+1)
    for day in days_of_week :
        for time_slot in time_slots :
            data[week][day][time_slot]["Môn học"] = ""
            data[week][day][time_slot]["Phòng học"] = ""
            data[week][day][time_slot]["Giáo viên"] = ""
            data[week][day][time_slot]["Ghi chú"] = ""
# Bước 3: Lưu tệp JSON
with open('schedule.json', 'w', encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)