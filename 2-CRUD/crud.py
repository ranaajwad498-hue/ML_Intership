children_list=[]

class child:
    def __init__(self,id, name, age, gender, parent_name, contact_number, address ):
        self.id=id
        self.name=name
        self.age= age
        self.gender= gender
        self.parent_name=parent_name
        self.contact_number= contact_number
        self.address= address

    #===== Add Children 
def add_children():
    print("Please Fill All the Fields Correctly")
    id= int(input("Enter Child ID: "))
    name=input("Enter Child Name: ")
    age=input("Enter Child Age: ")
    gender=input("Enter Child Gender: ")
    parent_name=input("Enter Child's Parent Name:")
    contact_number=input("Enter Child Contact Number: ")
    address=input("Enter Child Address: ")

    c=child(id, name, age, gender, parent_name, contact_number, address)
    children_list.append(c)
    print(f"\n--- {name} is added successfully ---\n")


    #===== View Children 
def view_children():
    if not children_list:
        print("Children List is Empty")
    else:
        print("List of ALL The Children That is added Successfully in Our Database")
        for c in children_list:
            print(f"Child ID: {c.id}")
            print(f"Child Name {c.name}")
            print(f"Age: {c.age}")
            print(f"Gender: {c.gender}")
            print(f"Parent Name: {c.parent_name}")
            print(f"Contact: {c.contact_number}")
            print(f"Address: {c.address}")
            print("-----------------------------------------------")


    #==== Search Chidren 
def search_child():
    search_id = int(input("Enter the ID You Want to Search: "))
    found=False

    for c in children_list:
        if c.id == search_id:
            print("-----ID found------")
            print(f"Child ID: {c.id}")
            print(f"Child Name {c.name}")
            print(f"Age: {c.age}")
            print(f"Gender: {c.gender}")
            print(f"Parent Name: {c.parent_name}")
            print(f"Contact: {c.contact_number}")
            print(f"Address: {c.address}")
            found=True
            break
        
    if not found:
        print(f"\n--- No records available to for This ID!:{search_id} ---\n")

    
     #=== Update Children
def update_child():
    update_id= int(input("Enter the ID You want to Update: "))
    found = False
    for c in children_list:
        if(c.id == update_id):
            c.name = int(input("Enter New Name: "))
            c.age = input("Enter New Age: ")
            c.gender = input("Enter New Gender: ")
            c.parent_name = input("Enter New Parent Name: ")
            c.contact_number = input("Enter New Contact Number: ")
            c.address = input("Enter New Address: ")
            print(f"\nSuccess: Record for ID {update_id} has been updated!\n")
            found=True
            break
           
    if not found:
        print(f"\n---No Record for this ID: {update_id} ---\n")
            
    
    #---Delete Child
def del_child():
    del_id=int(input("Enter the ID You want to Delete: "))
    found=False
    for c in children_list:
        if c.id == del_id:
            children_list.remove(c)
            print(f"{id} is Deleted Successfully")
            found=True
            break

    if not found:
        print(f"\n---No records found for ID: {del_id} ---\n")
        


while True:
    print("===== Child Information Management System =====")

    print("Press 1 to Add Child")
    print("Press 2 to View All the Children")
    print("Press 3 to Search the Children")
    print("Press 4 to Update Child Information")
    print("Press 5 to Delete the Children")
    print("Press 6 to Exit")   

    choice = int(input("Enter Your Choice: "))     
    if(choice==1):
         add_children()

    elif(choice==2):
        view_children()

    elif(choice==3):
        search_child()

    elif(choice == 4):
        update_child()

    elif (choice == 5):
        del_child()

    elif(choice==6):
        print("Exiting system. Goodbye!")
        break
    else:
        print("Please Enter the Correct Choice")


