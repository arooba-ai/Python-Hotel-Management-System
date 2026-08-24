
rooms={}
def load_rooms():
    print("\nSystem initialization.")

    try:
        with open('room.txt', 'r') as file:
            next(file)           # remove header
            for line in file:
                if not line.strip():  #skips empty lines
                    continue

                content = line.strip().split('|')

                roomno=content[0].strip()
                room_type=content[1].strip()
                price=content[2].strip()

                rooms[roomno]={'Type':room_type,'Price':price}


            print("\nRooms loading        | [SUCCESS]")

        return rooms
    except FileNotFoundError:
        print("File not found")



dates=[]
data=[]
def load_data():
    try:
        with open('bookings.txt', 'r') as file:
            next(file)  # skip header

            for line in file:
                if not line.strip():
                    continue

                content = line.strip().split('|')

                # Make sure the booking has 9 fields
                if len(content) != 9:
                    print("Warning: Skipping invalid booking record.")
                    continue

                booking_id = content[0].strip()
                guest_id = content[1].strip()
                roomno = content[2].strip()
                date = content[3].strip()
                checkin = content[4].strip()
                checkout = content[5].strip()
                amount = content[6].strip()
                paidamount = content[7].strip()
                status = content[8].strip()

                a = (checkin, checkout, status)
                b = (date, amount)

                data.append(b)
                dates.append(a)

        print("Bookings loading     | [SUCCESS]")

    except FileNotFoundError:
        print("File not found")

    return data, dates2


def load():
    global rooms,data,dates      # have same values in all the room dictionary
    rooms=load_rooms()
    data,dates=load_data()


def addroom():

    ROOM_TYPES = ["Single Room","Twin Room","Family Room","Deluxe Room"]
    roomno = input("Enter room no: ").strip()

    # stops the function if the room already exists
    if roomno in rooms or roomno in ' ':
        print(f"Roomno:{roomno} already exists or invalid input entered!Please try again")
        return rooms

    print(f"SELECT THE ROOM TYPE:\n1.Single(1 Guest , 1 bed)\n2.Twin Room (2 guest , 2 single beds)\n3.Family Room (3-5 guest , 2 Master bed with one single one)\n4.Deluxe(2-3 guest , 1 queen bed + Sofa bed")
    try:
        choice = int(input("Enter your choice (1-4): "))
        roomtype = ROOM_TYPES[choice - 1]
        price = int(input("Enter the price: "))


        rooms[roomno] = {'Type': roomtype, 'Price': price} #adds the new entry to the dictionary rooms

        with open('room.txt', 'w') as file:
            file.write(f"{'Roomno':<9}|{'Type':<16}|{'Price':<10}\n")  # header & space allignment
            for no, details in rooms.items():
                file.write(
                    f"{no:<9}|{details['Type']:<16}|{details['Price']:<10}\n")  # write the dictionary to the text file room

            print(f"Room:{roomno} added successfully!")
    except (ValueError,IndexError):  # it returns an error message if non-numeric input or number outside valid range is added
        print("Invalid input. Room not added.")

    return rooms


def update():
    roomno=input("Enter the room number to update: ").strip()
    if roomno not in rooms or roomno in ' ' :
        print(f"Roomno: {roomno} NOT FOUND!")
        return rooms
    print(f"What do you want to update?\n1.Room Type\n2.Price\n3.Both")
    choice=int(input("enter your choice:")) # asks the users if they want to update room type or price
    match choice:
        case 1: # Room type
            ROOM_TYPES = ["Single Room","Twin Room", "Family Room", "Deluxe Room"]
            print(f"SELECT THE ROOM TYPE:\n1.Single(1 Guest , 1 bed)\n2.Twin Room (2 guest , 2 single beds)\n3.Family Room (3-5 guest , 2 Master bed with one single one)\n4.Deluxe(2-3 guest , 1 queen bed + Sofa bed")
            type=int(input("enter the new room type choice:"))
            if type in [1,2,3,4]:
                roomtype=ROOM_TYPES[type-1]
                rooms[roomno]['Type']=roomtype #updates the dictionary
            else:
                print("Invalid choice!Type not updated")

        case 2: # price
            price=int(input("enter the new price:"))
            rooms[roomno]['Price']=price #updates the dictionary

        case 3: #both
            ROOM_TYPES = ["Single Room", "Twin Room", "Family Room", "Deluxe Room"]
            print(f"SELECT THE ROOM TYPE:\n1.Single(1 Guest , 1 bed)\n2.Twin Room (2 guest , 2 single beds)\n3.Family Room (3-5 guest , 2 Master bed with one single one)\n4.Deluxe(2-3 guest , 1 queen bed + Sofa bed")
            type = int(input("enter the new room type choice:"))
            if type in [1, 2, 3, 4]:
                roomtype = ROOM_TYPES[type - 1]
                rooms[roomno]['Type'] = roomtype  # updates the dictionary
            price = int(input("enter the new price:"))
            rooms[roomno]['Price'] = price  # updates the dictionary

        case _:
            print("Invalid choice!")
            return


    with open('room.txt','w') as file:
        file.write(f"{'Roomno':<9}|{'Type':<16}|{'Price':<10}\n")
        for no,details in rooms.items():
            file.write(f"{no:<9}|{details['Type']:<16}|{details['Price']:<10}\n")
        print(f"Room {roomno} updated successfully!")

    return rooms

def delete():
    roomno=input("Enter the room number to delete: ").strip()

    if roomno in rooms or roomno not in ' ':
        p=input("Are you sure you want to delete the room?:").lower() #confirmation message
        if p == 'yes':
            del rooms[roomno]

            with open('room.txt', 'w') as file:
                file.write(f"{'Roomno':<9}|{'Type':<16}|{'Price':<10}\n")
                for no, details in rooms.items():

                    file.write(f"{no:<9}|{details['Type']:<18}|{details['Price']:<10}\n")
                print(f"Room {roomno} deleted successfully!")
        else:
            print("Deletion cancelled!")

    else:
        print("Room not found!")
    return rooms



def system_summary():
    total_rooms=len(rooms)
    y=[]
    amount2=[]
    m=[]
    amount1=[]
    occupied_nights=0 # stores occuppied rooms-night

    print(f"1.Yearly summary"
          f"\n2.Monthly summary")
    choice=int(input("enter your choice:"))
    match choice:
        case 1: #(year)
                                                                 #calculates if the year is leap year
            year=input("enter the year:")
            if int(year)%4==0:
                tot=366
                total_rooms1 = total_rooms * tot

            else:
                tot=365
                total_rooms1 = total_rooms * tot


           #calculate the total number of occupied nights (checkout is dec 31 if checkout isn't mentioned)


            for checkin,checkout,status in dates:
                status=status.strip().lower()

                if status not in ['checked-in','booked']:   #filter the data where checkin or checkout aren't mentioned
                    checkin1 = checkin[:4]
                    checkout1 = checkout[:4]
                elif status == 'checked-in':               #if there is no checkout date mentioned
                                                        #(the last day of the month is taken as checkout)
                    checkin1 = checkin[ :4]
                    checkout1 = year
                else:
                    continue


                if (checkin1 == year or checkout1==year) :
                    date1=checkin[8:10]            #year
                    date2 = checkout[8:10]
                    if status == 'checked-in':
                        date1=checkin[8:10]
                        date2=31                   #checkout not mentioned so day is the last day of the dec
                    if status == 'checked-in':
                        month1=checkin[5:7]
                        month2=12                 #and month is the last month - dec
                    else:
                        month1=checkin[5:7]
                        month2=checkout[5:7]


                    if month1 == month2:                  #checks if the months are same

                        nights=int(date2)-int(date1)     #subracts the dates
                        occupied_nights+=nights


                    elif checkout[5:7]!=checkin[5:7]:        #checks if the month aren't the same
                        if checkin[5:7] in ('01', '03', '05', '07', '08', '10', '12'):
                            total = 31
                        elif checkin[5:7] in ('04', '06', '09', '11'):
                            total = 30
                        else:
                            if tot==365:
                                total= 28
                            else:
                                total=29                    #occupied no is calculated for each month
                        night1=int(total)-int(date1)       #by subracting the last day of the month with the checkin (for the first month)
                        night2=int(date2)-1               # & the checkout is subracted with 1 to calculate the number of days in second month
                        night=night1+night2
                        occupied_nights+=night




            #calculate the total bookings based on the booking date

            for bookdate,amount in data:
                y1=bookdate[ :4].strip() #extracts the year part from the dates in dictionary
                if y1==year:
                    amount2.append(amount) # extracts and stores the amount if the year matches the input
                    y.append(y1)


              # calculates the estimated income based on the booking dates
            sum=0
            for i in range(len(amount2)):
                sum+=float(amount2[i])
            l = len(y) # counts the total bookings

            unoccupied=total_rooms1 - occupied_nights
            yoccupancy=(occupied_nights / total_rooms1) * 100


            w = 70
            border = "+" + "-" * (w - 2) + "+"
            print(border)
            print("|" + "YEARLY SUMMARY".center(w - 2) + "|")
            print(border)
            line7 = f"Year: {year}"
            print("| " + line7.ljust(w - 4) + " |")
            line1 = f"Total bookings: {l}"
            print("| " + line1.ljust(w - 4) + " |")
            line2 = f"Estimated income based on booking date:RM {sum}"
            print("| " + line2.ljust(w - 4) + " |")
            line3=f'Total available room-night: {total_rooms1}'
            print("| " + line3.ljust(w - 4) + " |")
            line4=f'Total occupied room-night: {occupied_nights}'
            print("| " + line4.ljust(w - 4) + " |")
            line5=f'Total unoccupied room-night: {unoccupied}'
            print("| " + line5.ljust(w - 4) + " |")
            line6 = f"Occupancy rate: {yoccupancy:.2f}%"
            print("| " + line6.ljust(w - 4) + " |")

            print(border)


        case 2: # (month)
            year=input("enter the year(YYYY):")
            month=input("enter the month(MM):")
            if len(year)!=4 and ((int(month)<=1) or (int(month)>12)):
                print("Invalid format! Please month & year in MM YYYY format.")
                year = input("enter the year:")
                month = input("enter the month:")

            if month in ('01','03','05','07','08','10','12'):
                tot=31
                total_rooms=total_rooms*tot
            elif month in ('04','06','09','11'):
                tot=30                                       #available rooms are calculated
                total_rooms=total_rooms*tot
            else:
                tot=28
                total_rooms=total_rooms*tot

         #calculate the total occupied (for the ones checkout isn't mentioned , checkout is last date of the month)
            for checkin, checkout, status in dates:
                status=status.strip()
                if status not in ['checked-in','booked']:   #filters the data for whose checkout date isn't mentioned
                    checkin1 = checkin[5:7]                  #month
                    checkin2 = checkin[ :4]                  #year
                    checkout1 = checkout[5:7]
                    checkout2 = checkout[ :4]
                elif status == 'checked-in':            #if date isn't mentioned the checkout date automatically becomes the last day of the month
                    checkin1 = checkin[5:7]
                    checkin2 = checkin[:4]
                    checkout1 = tot
                    checkout2 = year
                else:
                    continue

                if (checkin1 == month or checkout1 == month) and (checkin2 == year or checkout2 == year) : #checks if the month and year matches with the input)
                    date1 = checkin[8:10]
                    date2 = checkout[8:10]

                    if (checkin[5:7] == checkout[5:7]):         #if check and checkout fall in the same month
                        nights = int(date2) - int(date1)        #(date is directly subracted)
                        occupied_nights += nights


                    elif checkout[5:7] != checkin[5:7]:                                    #if checkin checkout dont fall in the same month
                        if checkin[5:7] in ('01', '03', '05', '07', '08', '10', '12'):
                            tot = 31
                        elif checkin[5:7] in ('04', '06', '09', '11'):
                            tot = 30
                        else:
                            tot = 28
                        if checkin[5:7] == month:                # the total of first month is calculated by subracting the checkin with total no of days in that month
                            nights = int(tot) - int(date1)
                            occupied_nights += nights

                        elif checkout[5:7] == month:           #the total of second one is calculated by subracting the checkout with 1
                            nights=int(checkout[8:10])-1
                            occupied_nights += nights






         #calculate the total bookings based on the booking date
            for bookdate,amount in data:
                m1=bookdate[5:7].strip() #extracts the month from dictionary
                m2=bookdate[ :4].strip() #extracts the year from dictionary
                if m1==month and m2==year: # checks if year & month in dictionary matches with the input
                    amount1.append(float(amount)) # extracts the amount
                    m.append(m1)
            l1 = len(m) # counts total bookings

            #calculates total bookings based on the booking date

            sum1=0
            for i in range(len(amount1)):
                sum1+=float(amount1[i])

            unoccupied=total_rooms - occupied_nights
            moccupancy=(occupied_nights / total_rooms) * 100
            w = 70
            border = "+" + "-" * (w - 2) + "+"

            print(f"\n{border}")
            print("|" + "MONTHLY SUMMARY".center(w - 2) + "|")
            print(border)
            print("| " + f"Month: {month}-{year}".ljust(w - 4) + " |")
            print("| " + f"Monthly bookings: {l1}".ljust(w - 4) + " |")
            print("| " + f"Estimated income based on booking date: RM {sum1:,.2f}".ljust(w - 4) + " |")
            print("| " + f"Total available room-night: {total_rooms}".ljust(w - 4) + " |")
            print("| " + f"Total occupied room-night: {occupied_nights}".ljust(w - 4) + " |")
            print("| " + f"Occupancy rate: {moccupancy:.2f}%".ljust(w - 4) + " |")


            print(border)
        case _:
            print("Invalid input. Please try again.")



def performance():
    print(f"1.Daily Performance Report"
          f"\n2.Monthly Performance Report")

    choice=int(input("enter your choice:"))

    match choice:

        case 1:
            totalrooms = len(rooms)

            occupied = 0
            date = input("enter the date(YYYY-MM-DD):")
            if len(date)!= 10 or date[4]!= '-' or date[7]!= '-':

                print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
                date=input("enter today's date(YYYY-MM-DD):")

            for checkin,checkout,status in dates:
                if status == 'checked-out':
                    if checkin <= date and checkout>=date:
                        occupied += 1
                elif status == 'checked-in':
                    if checkin <= date:
                        occupied += 1
                else:
                    continue

            unoccupied=totalrooms - occupied
            occupancyrate=(occupied / totalrooms) * 100
            if occupancyrate>70:
                remarks="Excellent performance with high room occupancy."
            elif occupancyrate<70:
                remarks="Room occupancy is lower than the targeted benchmark."
            else:
                remarks="Room occupancy met the targeted benchmark."
            w = 70

            border = "+" + "-" * (w - 2) + "+"
            print(f"\n{border}")
            print("|" + "DAILY PERFORMANCE REPORT".center(w - 2) + "|")
            print(border)
            print("| " + f"Date: {date}".ljust(w - 4) + " |")
            print("| " + f"Total rooms: {totalrooms}".ljust(w - 4) + " |")
            print("| " + f"Occupied: {occupied}".ljust(w - 4) + " |")
            print("| " + f"Unoccupied: {unoccupied}".ljust(w - 4) + " |")
            print("| " + f"Occupancy rate: {occupancyrate:.2f}%".ljust(w - 4) + " |")
            print("| " + f"Target rate: {70:.2f}%".ljust(w - 4) + " |")
            print("| " + f"Remarks: {remarks}".ljust(w - 4) + " |")
            print(border)

        case 2:

            amount1=[]
            totalrooms = len(rooms)

            occupied_nights = 0
            booking_count = 0
            booking_count1=0
            year=input("enter the year(YYYY):")
            month=input("enter the month(MM):")

            if len(year)==4 and len(month)==2 and (int(month)>=1 and int(month)<=12):
                pass

            else:
                print("Invalid format. Please enter the month and year in correct format.")
                year=input("enter the year:")
                month = input("enter the month:")

            if month in ('01','03','05','07','08','10','12'):
                days=31
                totalrooms1=totalrooms*days
            elif month in ('04','06','09','11'):
                days=30
                totalrooms1=totalrooms*days
            else:
                days=28
                totalrooms1=totalrooms*days

            if month=='01':
                month1='12'                          # year 1 & month1 are the prev years
                year1=str(int(year)-1)
            else:
                month1=f"{int(month)-1:02d}"
                year1=year


                 # calculates occupied
            for checkin, checkout, status in dates:
                if status not in ['checked-in','booked']:     #to filter checkouts without dates
                        checkin1 = checkin[5:7]                #slicing month
                        checkin2 = checkin[:4]                  #slicing year
                        checkout1 = checkout[5:7]
                        checkout2 = checkout[:4]
                elif status == 'checked-in':
                        checkin1 = checkin[5:7] #month
                        checkin2 = checkin[:4] #year
                        checkout1=str(days)                  #if checkout date not mentioned checkout becomes the last day of the month
                        checkout2=year
                else:
                    continue

                if (checkin1 == month or checkout1 == month) and (checkin2 == year or checkout2 == year):  #ensures if the month & year of the checkin checkout matches with input

                         if status.strip() == 'checked-in':
                             date1=checkin[8:10]     #days
                             date2=str(days)                # if checkout not mentioned day becomes the last day of the month

                         elif status.strip() == 'checked-out':
                             date1 = checkin[8:10]
                             date2 = checkout[8:10]

                         else:
                             continue


                         if (checkin1 == checkout1):             #if checkin and checkout are the same month , their dates are subracted
                             nights = int(date2) - int(date1)
                             occupied_nights += nights



                         elif checkout1 != checkin1:                #checks if checkin and checkout full in different month
                              if checkin[5:7] in ('01', '03', '05', '07', '08', '10', '12'):
                                  tot = 31
                              elif checkin[5:7] in ('04', '06', '09', '11'):
                                  tot = 30
                              else:
                                  tot = 28

                              if checkin[5:7] == month:                   # only the dates in the input month is calculated
                                                                        # (by subracting them with the total number of days in that particular month)
                                  nights = int(tot) - int(date1)
                                  occupied_nights += nights


                              elif checkout[5:7] == month:
                                  nights = int(checkout[8:10]) - 1
                                  occupied_nights += nights



                #calculate the bookings based on the booking date
            for bookdate,amount in data:
                m1 = bookdate[5:7].strip()
                m2=bookdate[ :4]
                if m1 == month and m2 == year :     # checks if the month & year matches with the current year
                    booking_count += 1   # counts the bookings for prev month
                    amount1.append(amount)
            for bookdate,amount in data:
                m3 = bookdate[5:7].strip()
                m4 = bookdate[:4]
                if m3 ==month1 and m4 == year1:
                    booking_count1+=1
            sum1 = 0
            for i in range(len(amount1)):
                sum1 += float(amount1[i])



            if booking_count1>booking_count:
                trend=booking_count1-booking_count
                word='lower than'
                remarks="Lower demand compared to the previous month."
            elif booking_count1<booking_count:
                trend=booking_count-booking_count1
                word='higher than'
                remarks="Positive growth in room sales."
            else:
                trend = booking_count - booking_count1
                word ='higher than'
                remarks='No significant change.'



            sold=occupied_nights
            unsold=totalrooms1-sold
            occupancyrate=(occupied_nights/totalrooms1)*100

            target=70
            w = 60  # Increased width slightly to fit longer labels
            border = "+" + "-" * (w - 2) + "+"

            print(f"\n{border}")
            print("|" + "MONTHLY PERFORMANCE REPORT".center(w - 2) + "|")
            print(border)

            # Data Rows
            print("| " + f"Month : {month}-{year}".ljust(w - 4) + " |")
            print("| " + f"Total rooms sold: {sold}".ljust(w - 4) + " |")
            print("| " + f"Total rooms unsold: {unsold}".ljust(w - 4) + " |")
            print("| " + f"Occupancy rate: {occupancyrate:.2f}%".ljust(w - 4) + " |")
            print("| " + f"Target Occupancy rate: {target}%".ljust(w - 4) + " |")
            print("| " + f"Total bookings: {booking_count}".ljust(w - 4) + " |")
            print("| " + f"Trend: {trend} bookings {word} previous month".ljust(w - 4) + " |")
            print("| " + f"Remarks: {remarks}".ljust(w - 4) + " |")

            print(border)


def manager_menu():
    border='_'*30
    while True:
        global rooms
        load()
        print(f"\n1.Add new room"
          f"\n2.Update existing room"
          f"\n3.Delete existing room"
          f"\n4.View system summary"
          f"\n5.View performance report"
          f"\n6.Return to main menu"
          f"\n7.Exit")
        choice = int(input("\nEnter your choice: "))
        match choice:
            case 1:
                print(border)
                print("MENU > ADD ROOM".center(30))
                print(border)
                rooms=addroom()
            case 2:
                print(border)
                print("MAIN MENU > UPDATE ROOM".center(30))
                print(border)
                rooms=update()
            case 3:
                print(border)
                print("MAIN MENU > DELETE ROOM".center(30))
                print(border)
                rooms=delete()
            case 4:
                print(border)
                print("MAIN MENU > SYSTEM SUMMARY".center(30))
                print(border)
                system_summary()
            case 5:
                print(border)
                print("MAIN MENU > PERFORMANCE REPORT".center(30))
                print(border)
                performance()
            case 6:
                return
            case 7:
                print("Thank you for using StayEase".center(30))
                exit()
            case _:
                print("Invalid choice!Please try again.")




def receptionist_menu():
    while True:
        print("Which department to access:")
        print(" 1.Guests \n 2.Bookings \n 3.Room Availability \n 4.Return to main menu \n 5.Exit")
        try:
            ch = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if ch == 1:
            while True:
                print("GUEST MENU")
                print(" 1. Add Guest \n 2. Update Guest information \n 3. Delete Guest \n 4. Exit")
                choice = input("Enter your choice: ")
                match choice:
                    case "1":
                        add_guest()
                    case "2":
                       update_guest()
                    case "3":
                        delete_guest()
                    case "4":
                        break

                    case _:
                        print("Invalid choice.")
        elif ch == 2:
            while True:
                print("BOOKING MENU")
                print(" 1.Create booking \n 2.Check-in \n 3.Check-out \n 4.Cancel booking \n 5.Exit")
                choice = input("Enter your choice: ")
                match choice:
                    case "1":
                        new_booking()
                    case "2":
                        check_in()
                    case "3":
                        check_out()
                    case "4":
                        cancel_booking()
                    case "5":
                        break
                    case _:
                        print("Invalid choice.")
        elif ch==3:
                print("ROOM AVAILABILITY")
                room_avb()

        elif ch==4:
            print("See you next time, receptionist.")
            return

        elif ch==5:
            print("Thank you for using StayEase".center(30))
            exit()

        else:
            print("Invalid choice. Please try again.")







def add_guest():
    guest_id = input("Enter guest id: ")
    name = input("Enter guest name: ")
    email = input("Enter guest email: ")
    phone = input("Enter phone number: ")

    guest = {'guestid': guest_id,'guestname': name,'guestemail': email,'guestphone': phone}

    with open("guests.txt", "a") as file:
        file.write(f"{guest['guestid']:<5}|{guest['guestname']:<7}|{guest['guestemail']:<22}|{guest['guestphone']:<12}\n")

    print("Guest added successfully!")

def update_guest():
    guest_id = input("Enter guest id to update: ")

    with open("guests.txt", "r") as file:
        lines = file.readlines()
    updated_lines = []
    found = False
    for line in lines:
        data = line.strip().split("|")
        if data[0].strip() == guest_id:
            name = input("Enter new name: ")
            email = input("Enter new email: ")
            phone = input("Enter new phone number: ")
            updated_lines.append(f"{guest_id:<5}|{name:<7}|{email:<22}|{phone:<12}\n")
            found = True
        else:
            updated_lines.append(line)

    with open("guests.txt", "w") as file:
        file.writelines(updated_lines)

    if found:
        print("Guest updated successfully!")
    else:
        print("Guest not found.")

def delete_guest():
    guest_id = input("Enter guest id to delete: ")
    updated_lines = []

    with open("guests.txt", "r") as file:
        lines = file.readlines()

    found = False
    for line in lines:
        data = line.strip().split("|")
        if data[0].strip() == guest_id:
            found = True
        else:
            updated_lines.append(line)
    with open("guests.txt", "w") as file:
        file.writelines(updated_lines)
    if found:
        print("Guest deleted successfully!")
    else:
        print("Guest not found.")

def new_booking():
    try:
        roomno = input("Enter room number: ")
        try:
            with open("bookings.txt", "r") as file:
                for line in file:
                    data=line.strip().split("|")
                    if data[2].strip() == roomno and data[8] in ("booked", "checked-in"):
                        print("This room is already booked. Try another.")
                        return
        except FileNotFoundError:
            pass

        booking = {"bookingid": input("Enter booking id: "),"guestid": input("Enter guest id: "),
                   "roomno": roomno,"bookingdate": input("Enter booking date(YYYY-MM-DD): "),
                   "checkindate": "YYYY-MM-DD","checkoutdate": "YYYY-MM-DD",
                   "totalprice": input("Enter total price: "),"paidamount" : "0.00", "status": "booked"}

        with open("bookings.txt", "a") as file:

            file.write(f"{booking['bookingid']:<5}|{booking['guestid']:<5}|{booking['roomno']:<5}|"
                       f"{booking['bookingdate']:<12}|{booking['checkindate']:<12}|{booking['checkoutdate']:<12}|"
                       f"{booking['totalprice']:<10}|{booking['paidamount']:<10}|{booking['status']:<10}\n")

        print("Booking added successfully!")

    except FileNotFoundError:
        print("Error: Booking file not found.")

def check_in():
    booking_id = input("Enter booking ID for check-in: ")
    updated_lines = []
    found = False

    with open("bookings.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split("|")
        if data[0].strip() == booking_id:
            if data[8] == "booked":
                data[8] = "checked-in"
                checkin=input("Enter checkin date: ")
                data[4] = checkin.ljust(12)
                print("Guest checked in!")
            else:
                print("Guest is already checked in or checked out!")
            found = True

        updated_lines.append("|".join(data) + "\n")

    with open("bookings.txt", "w") as file:
        file.writelines(updated_lines)

    if not found:
        print("Booking not found.")

def check_out():
    booking_id = input("Enter booking ID for check-out: ")
    updated_lines = []
    found = False

    with open("bookings.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split("|")
        if data[0].strip() == booking_id:
            if data[8] == "checked-in":
                data[8] = "checked-out"
                checkout=input("Enter checkout date (YYYY-MM-DD): ")
                data[5] = checkout.ljust(12)
                print("Guest checked out!")
            else:
                print("Guest isn't checked in or already checked out!")
            found = True

        updated_lines.append("|".join(data) + "\n")

    with open("bookings.txt", "w") as file:
        file.writelines(updated_lines)

    if not found:
        print("Booking not found.")

def cancel_booking():
    booking_id = input("Enter booking ID for cancel: ")
    found = False

    with open("bookings.txt", "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        data = line.strip().split("|")
        if data[0].strip() == booking_id:
            found = True
            continue
        updated_lines.append("|".join(data) + "\n")

    if found:
        with open("bookings.txt", "w") as file:
            file.writelines(updated_lines)
        print("Booking cancelled.")
    else:
        print("Booking not found.")

def room_avb():
    occupied_rooms = set()
    try:
        with open("bookings.txt", "r") as file:
            for line in file:
                if not line.strip():
                    continue
                data=line.strip().split("|")
                if len(data) < 9:
                    continue
                room_no = data[2].strip()
                status = data[8]
                if status in ("booked", "checked-in"):
                    occupied_rooms.add(room_no)

    except FileNotFoundError:
        print("Error: Booking file not found.")

    try:
        with open("room.txt", "r") as file:
            print("{:<10} {:<20} {:<10} {}".format("Room No", "Type", "Price", "Status"))
            print("-"*55)
            for line in file:
                if not line.strip():
                    continue
                data=line.strip().split("|")
                if len(data) != 3:
                    continue
                try:
                    room_no = data[0].strip()
                    room_type = data[1].strip()
                    room_price= data[2].strip()
                except IndexError:
                    continue

                if room_no in occupied_rooms:
                    status = "Occupied"
                else:
                    status = "Available"
                print(f"{room_no:<10} {room_type:<20} {room_price:<10} {status}")

    except FileNotFoundError:
        print('Error: Room file not found.')





def booking_line(line):
    parts = line.strip().split("|")

    if len(parts) == 9:
        return {
            "booking_id": parts[0],
            "guest_id": parts[1],
            "room_no": parts[2],
            "booking_date": parts[3],
            "checkin_date": parts[4],
            "checkout_date": parts[5],
            "total_amount": parts[6],
            "paid_amount": parts[7],
            "status": parts[8]
        }

    elif len(parts) == 8:
        return {
            "booking_id": parts[0],
            "guest_id": parts[1],
            "room_no": parts[2],
            "booking_date": "",
            "checkin_date": parts[3],
            "checkout_date": parts[4],
            "total_amount": parts[5],
            "paid_amount": parts[6],
            "status": parts[7]
        }

    return None


def build_booking_line(b):
    return "|".join([
        b["booking_id"],
        b["guest_id"],
        b["room_no"],
        b.get("booking_date", ""),
        b["checkin_date"],
        b["checkout_date"],
        f"{float(b['total_amount']):<10.2f}",
        f"{float(b['paid_amount']):<10.2f}",
        b["status"]])

def accountant_menu():
    while True:
        print("\n===== Accountant Menu =====")
        print("1. View outstanding payments")
        print("2. Record new payment")
        print("3. Income summary monthly")
        print("4. Monthly financial summary")
        print("5. Return to main menu")
        print("0. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_outstanding_payments()
        elif choice == "2":
            record_payment()
        elif choice == "3":
            income_summary_monthly()
        elif choice == "4":
            monthly_financial_summary()
        elif choice == "5":
            print("Returning to main menu.")
            return
        elif choice == "0":
            print("Thank you for using this program!")
            exit()
        else:
            print("Invalid choice. Try again.")





def view_outstanding_payments():
    print("\n--- Outstanding Payments ---")

    try:
        with open("bookings.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        print("Error: bookings.txt not found.")
        return

    any_outstanding = False

    for line in lines:
        b = booking_line(line)
        if b is None:
            continue

        # Skip cancelled bookings
        if b["status"].lower() == "cancelled":
            continue

        try:
            total_amount = float(b["total_amount"])
            amount_paid = float(b["paid_amount"])
        except ValueError:
            continue

        balance = total_amount - amount_paid

        if balance > 0:
            any_outstanding = True
            print(
                f"Booking ID: {b['booking_id']} | "
                f"Room: {b['room_no']} | "
                f"Booking Date: {b['booking_date']} | "
                f"Balance: RM {balance:.2f}"
            )

    if not any_outstanding:
        print("No outstanding payments found.")

def record_payment():
    # Calculate remaining balance based on booking total amount
    # This allows different room prices automatically
    print("\n--- Record New Payment ---")

    booking_id = input("Enter booking ID: ").strip()

    try:
        with open("bookings.txt", "r", encoding="utf-8") as f:
            bookings = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: bookings.txt not found.")
        return

    updated_bookings = []
    booking_found = False

    for line in bookings:
        b = booking_line(line)

        # If line is invalid, keep it unchanged
        if b is None:
            updated_bookings.append(line)
            continue

        if b["booking_id"].strip() != booking_id:
            updated_bookings.append(line)
            continue

        booking_found = True

        if b["status"].lower() == "cancelled":
            print("Payment not allowed. Booking is cancelled.")
            return

        try:
            total_amount = float(b["total_amount"])
            amount_paid = float(b["paid_amount"])
        except ValueError:
            print("Corrupted booking data.")
            return

        balance = total_amount - amount_paid
        if balance <= 0:
            print("This booking is already fully paid.")
            return

        try:
            payment_amount = float(input("Enter payment amount: ").strip())
        except ValueError:
            print("Invalid amount.")
            return

        if payment_amount <= 0:
            print("Payment must be greater than zero.")
            return

        if payment_amount > balance:
            print(f"Payment exceeds balance. Remaining: RM {balance:07.2f}")
            return

        method = input("Payment method (Cash/Card/Online): ").strip().capitalize()
        if method not in ["Cash", "Card", "Online"]:
            print("Invalid payment method.")
            return

        # Update paid amount in booking (keep booking_date & room_no intact)
        new_paid = amount_paid + payment_amount
        b["paid_amount"] = f"{new_paid:<10.2f}"
        b["total_amount"] = f"{total_amount:<10.2f}"

        # Write back in NEW 9-field format always
        updated_bookings.append(build_booking_line(b))

        # Generate payment record
        payment_id = generate_payment_id()

        from datetime import date
        payment_date = date.today().isoformat()

        with open("payments.txt", "a", encoding="utf-8") as pf:
            pf.write(f"{payment_id:<6}|{booking_id:<5}|{payment_date:<12}|{payment_amount:<12.2f}|{method:<10}\n")

        print("Payment recorded successfully.")

    if not booking_found:
        print("Booking ID not found.")
        return

    with open("bookings.txt", "w", encoding="utf-8") as f:
        for line in updated_bookings:
            f.write(line + "\n")

def generate_payment_id():
    try:
        with open("payments.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return "P1001"

    if not lines:
        return "P1001"

    last_id = lines[-1].split("|")[0]
    try:
        number = int(last_id[1:]) + 1
    except ValueError:
        number = 1001

    return f"P{number}"

def income_summary_monthly():
    print("\n--- Income Summary (Monthly) ---")

    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip()

    # Basic validation
    if not (year.isdigit() and len(year) == 4):
        print("Invalid year format.")
        return
    if not (month.isdigit() and 1 <= int(month) <= 12):
        print("Invalid month format.")
        return

    month = month.zfill(2)  # ensures 1 becomes 01, etc.
    target_prefix = f"{year}-{month}"  # matches YYYY-MM

    total_income = 0.0
    payment_count = 0

    try:
        with open("payments.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                # Expected: P1001|B001|2025-12-10|120.00|Card
                if len(parts) != 5:
                    continue

                payment_id, booking_id, pay_date, amount_str, method = parts

                if pay_date.startswith(target_prefix):
                    try:
                        amount = float(amount_str)
                        total_income += amount
                        payment_count += 1
                    except ValueError:
                        continue

    except FileNotFoundError:
        print("Error: payments.txt not found.")
        return

    print(f"\nMonth: {year}-{month}")
    print(f"Number of payments: {payment_count}")
    print(f"Total income collected: RM {total_income:.2f}")
def monthly_financial_summary():
    print("\n--- Monthly Financial Summary ---")

    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip()

    if not (year.isdigit() and len(year) == 4):
        print("Invalid year format.")
        return
    if not (month.isdigit() and 1 <= int(month) <= 12):
        print("Invalid month format.")
        return

    month = month.zfill(2)
    target_prefix = f"{year}-{month}"

    expected_revenue = 0.0
    booking_count = 0
    active_bookings = 0

    # Expected revenue from bookings (check-in month)
    try:
        with open("bookings.txt", "r", encoding="utf-8") as bf:
            for line in bf:
                if not line.strip():
                    continue
                b = booking_line(line)
                if b is None:
                    continue

                checkin = b["checkin_date"]
                status = b["status"].lower()

                if checkin.startswith(target_prefix):
                    booking_count += 1
                    if status != "cancelled":
                        active_bookings += 1
                        try:
                            expected_revenue += float(b["total_amount"])
                        except ValueError:
                            pass
    except FileNotFoundError:
        print("Error: bookings.txt not found.")
        return

    collected = 0.0
    payment_count = 0

    # Collected revenue from payments (payment month)
    try:
        with open("payments.txt", "r", encoding="utf-8") as pf:
            for line in pf:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 5:
                    continue

                _, _, pay_date, amount_str, _ = parts
                if pay_date.startswith(target_prefix):
                    try:
                        collected += float(amount_str)
                        payment_count += 1
                    except ValueError:
                        continue
    except FileNotFoundError:
        print("Error: payments.txt not found.")
        return

    outstanding = expected_revenue - collected
    if outstanding < 0:
        outstanding = 0.0

    print(f"\nMonth: {year}-{month}")
    print(f"Bookings (check-in in month): {booking_count}")
    print(f"Active (not cancelled): {active_bookings}")
    print(f"Payments recorded in month: {payment_count}")
    print(f"Expected revenue: RM {expected_revenue:.2f}")
    print(f"Collected revenue: RM {collected:.2f}")
    print(f"Outstanding (expected - collected): RM {outstanding:.2f}")

def main_menu():
    while True:
        print("\nWelcome to Stay Ease!")

        w = 50
        border = "+" + "-" * (w - 2) + "+"

        # Header Section
        print(f'\n{border}')
        print("|" + "STAYEASE".center(w - 2) + "|")
        print(border)


        print(f"| " + "1. System Administration".ljust(w - 4) + " |")
        print(border)
        print("| " + "2. Front desk management".ljust(w - 4) + " |")
        print(border)
        print("| " + "3. Accounts management".ljust(w - 4) + " |")
        print(border)
        print("| " + "4. Exit".ljust(w - 4) + " |")
        print(border)
        try:
            choice = int(input("Enter your choice: "))
            match choice:
                case 1:
                    manager_menu()


                case 2:
                    receptionist_menu()


                case 3:
                    accountant_menu()

                case 4:
                    print("EXITING THE PROGRAM")
                    print("\nThank you for using Stay Ease!")
                    exit()

        except (ValueError,IndexError):
            print("Invalid input.")




main_menu()






