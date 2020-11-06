# # Creating table
# import sqlite3

# #Connecting to sqlite
# conn = sqlite3.connect('database.db')

# #Creating a cursor object using the cursor() method
# cursor = conn.cursor()

# # Droping EMPLOYEE table if already exists.
# cursor.execute("DROP TABLE IF EXISTS product")

# # Creating table as per requirement
# sql ="""CREATE TABLE product(
#    NAME CHAR(20) NOT NULL,
#    WHOLESALE_COST FLOAT,
#    LOCAL_COST FLOAT,
#    QUANTITY INT,
#    FACTOR FLOAT,
#    SELLING_COST FLOAT
# )"""
# cursor.execute(sql)
# print("Table created successfully........")

# sql = """INSERT INTO product VALUES('Onion', 20.0, 0.0, 15, 1, 25)"""
# cursor.execute(sql)
# sql = """INSERT INTO product VALUES('Banana', 45.0, 0.0, 15, 1, 25)"""
# cursor.execute(sql)
# sql = """INSERT INTO product VALUES('Apple', 20.0, 0.0, 15, 1, 10)"""
# cursor.execute(sql)
# sql = """INSERT INTO product VALUES('Cabbage', 54.0, 0.0, 15, 1, 25)"""
# cursor.execute(sql)
# sql = """INSERT INTO product VALUES('Tomato', 544.0, 0.0, 4, 1, 456)"""
# cursor.execute(sql)
# sql = """INSERT INTO product VALUES('ABC', 235.0, 123.0, 23, 1, 363)"""
# cursor.execute(sql)
# sql = """INSERT INTO product VALUES('XYZ', 36.0, 0.0, 34, 1, 26)"""
# cursor.execute(sql)


from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('AAHO Items')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Add new Product')
        frame.grid(row = 0, column = 0, columnspan = 7, pady = 20)

        # NAME Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # WHOLESALE_COST Input
        Label(frame, text = 'Wholesale Cost: ').grid(row = 2, column = 0)
        self.wholesale_cost = Entry(frame)
        self.wholesale_cost.grid(row = 2, column = 1)

        # LOCAL_COST Input
        Label(frame, text = 'Local Cost: ').grid(row = 3, column = 0)
        self.local_cost = Entry(frame)
        self.local_cost.grid(row = 3, column = 1)

        # QUANTITY Input
        Label(frame, text = 'Quantity: ').grid(row = 4, column = 0)
        self.quantity = Entry(frame)
        self.quantity.grid(row = 4, column = 1)

        # FACTOR Input
        Label(frame, text = 'Factor: ').grid(row = 5, column = 0)
        self.factor = Entry(frame)
        self.factor.grid(row = 5, column = 1)

        # SELLING_COST Input
        Label(frame, text = 'Selling Cost: ').grid(row = 6, column = 0)
        self.selling_cost = Entry(frame)
        self.selling_cost.grid(row = 6, column = 1)


        # Button Add Product 
        ttk.Button(frame, text = 'Add Product', command = self.add_product).grid(row = 8, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = 'Welcome to store', fg = 'red')
        self.message.grid(row = 11, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 20, columns = ("#0","#1","#2","#3","#4","#5","#6"))
        self.tree.grid(row = 15, column = 0, columnspan = 1)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Wholesale Cost', anchor = CENTER)
        self.tree.heading('#2', text = 'Local Cost', anchor = CENTER)
        self.tree.heading('#3', text = 'Quantity', anchor = CENTER)
        self.tree.heading('#4', text = 'Factor', anchor = CENTER)
        self.tree.heading('#5', text = 'Selling Cost', anchor = CENTER)
        self.tree.heading('#6', text = 'Profit', anchor = CENTER)
        # self.tree.heading('#2', text = 'Nachiket', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_product).grid(row = 22, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT', command = self.edit_product).grid(row = 24, column = 0, sticky = W + E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        # query = 'SELECT * FROM product ORDER BY name DESC'
        query = 'SELECT * FROM product'
        db_rows = self.run_query(query)
        # filling data
        def get_profit(wholesale_cost, local_cost, quantity, selling_cost):
            # return -1
            # print(wholesale_cost, local_cost, quantity, selling_cost)
            wholesale_cost  = int(wholesale_cost)
            local_cost      = int(local_cost)
            quantity        = int(quantity)
            selling_cost    = int(selling_cost)
            if wholesale_cost == 0.0:
                return (selling_cost - local_cost) * quantity
            if local_cost == 0.0:
                return (selling_cost - wholesale_cost) * quantity
            best = (local_cost + wholesale_cost) / 2
            return (selling_cost - best) * quantity

        for row in db_rows:
            # print(row)
            profit = get_profit(row[1], row[2], row[3], row[5])
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4], row[5], profit))

    # User Input Validation
    def validation(self):
        parameters =  [self.name.get(), self.wholesale_cost.get(), self.local_cost.get(),
                           self.quantity.get(), self.factor.get(), self.selling_cost.get()]

        def check_string(s):
            if len(s) == 0:
                return False
            nums = [str(x) for x in range(10)]
            for ch in s:
                if ch in nums:
                    return False
            return True

        def check_number(s):
            if len(s) == 0:
                return False
            nums = [str(x) for x in range(10)] + ['.']
            for ch in s:
                if ch not in nums:
                    return False
            return True

        ok = True
        for p in parameters:
            ok = ok and len(p)
            # print(type(p))

        for i in range(len(parameters)):
            if i == 0:
                ok = ok and check_string(parameters[i])
            else:
                ok = ok and check_number(parameters[i])

        return ok

        # return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(?, ?, ?, ?, ?, ?)'
            parameters =  (self.name.get(), self.wholesale_cost.get(), self.local_cost.get(),
                           self.quantity.get(), self.factor.get(), self.selling_cost.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.wholesale_cost.delete(0, END)
            self.local_cost.delete(0, END)
            self.quantity.delete(0, END)
            self.factor.delete(0, END)
            self.selling_cost.delete(0, END)
        else:
            self.message['text'] = 'Invalid data types used'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        name             = self.tree.item(self.tree.selection())['text']
        wholesale_cost   = self.tree.item(self.tree.selection())['values'][0]
        local_cost       = self.tree.item(self.tree.selection())['values'][1]
        quantity         = self.tree.item(self.tree.selection())['values'][2]
        factor           = self.tree.item(self.tree.selection())['values'][3]
        selling_cost     = self.tree.item(self.tree.selection())['values'][4]

        # print(name, wholesale_cost, local_cost, quantity, factor, selling_cost)

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product new'

        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old wholesale_cost 
        Label(self.edit_wind, text = 'Old wholesale_cost:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = wholesale_cost), state = 'readonly').grid(row = 2, column = 2)
        # New wholesale_cost
        Label(self.edit_wind, text = 'New wholesale_cost:').grid(row = 3, column = 1)
        new_wholesale_cost = Entry(self.edit_wind)
        new_wholesale_cost.grid(row = 3, column = 2)

        # Old local_cost 
        Label(self.edit_wind, text = 'Old local_cost:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = local_cost), state = 'readonly').grid(row = 4, column = 2)
        # New local_cost
        Label(self.edit_wind, text = 'New local_cost:').grid(row = 5, column = 1)
        new_local_cost = Entry(self.edit_wind)
        new_local_cost.grid(row = 5, column = 2)

        # Old quantity 
        Label(self.edit_wind, text = 'Old quantity:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = quantity), state = 'readonly').grid(row = 6, column = 2)
        # New quantity
        Label(self.edit_wind, text = 'New quantity:').grid(row = 7, column = 1)
        new_quantity = Entry(self.edit_wind)
        new_quantity.grid(row = 7, column = 2)

        # Old factor 
        Label(self.edit_wind, text = 'Old factor:').grid(row = 8, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = factor), state = 'readonly').grid(row = 8, column = 2)
        # New factor
        Label(self.edit_wind, text = 'New factor:').grid(row = 9, column = 1)
        new_factor = Entry(self.edit_wind)
        new_factor.grid(row = 9, column = 2)

        # Old selling_cost 
        Label(self.edit_wind, text = 'Old selling_cost:').grid(row = 10, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = selling_cost), state = 'readonly').grid(row = 10, column = 2)
        # New selling_cost
        Label(self.edit_wind, text = 'New selling_cost:').grid(row = 11, column = 1)
        new_selling_cost = Entry(self.edit_wind)
        new_selling_cost.grid(row = 11, column = 2)

        # print(new_name, new_wholesale_cost, new_local_cost, new_quantity, new_factor, new_selling_cost)
        old_values = [name, wholesale_cost, local_cost, quantity, factor, selling_cost]
        new_values = [new_name.get(), new_wholesale_cost.get(), new_local_cost.get(), new_quantity.get(), new_factor.get(), new_selling_cost.get()]


        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(old_values, tuple([new_name.get(), new_wholesale_cost.get(), new_local_cost.get(), new_quantity.get(), new_factor.get(), new_selling_cost.get()]))).grid(row = 20, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def valid(self, new_values):
        def check_string(s):
            if len(s) == 0:
                return False
            nums = [str(x) for x in range(10)]
            for ch in s:
                if ch in nums:
                    return False
            return True

        def check_number(s):
            if len(s) == 0:
                return False
            nums = [str(x) for x in range(10)] + ['.']
            for ch in s:
                if ch not in nums:
                    return False
            return True

        ok = True
        for i in range(len(new_values)):
            if i == 0:
                ok = ok and check_string(new_values[i])
            else:
                ok = ok and check_number(new_values[i])
        return ok


    def edit_records(self, old_values, new_values):

        print(old_values)
        print(new_values)

        if not self.valid(new_values):
            self.message['text'] = 'Invalid data entered'
            return

        query = """UPDATE product SET name = ?, wholesale_cost = ?, local_cost = ?, quantity = ?, factor = ?, selling_cost = ?
                   WHERE name = ? AND wholesale_cost = ? AND local_cost = ? AND quantity = ? AND factor = ? AND selling_cost = ?"""
        parameters = tuple(new_values) + tuple(old_values)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfully'.format(old_values[0])
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
