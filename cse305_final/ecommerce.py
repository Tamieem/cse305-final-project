import sqlite3

connection = sqlite3.connect("ecommerce.db")

connection.execute('''CREATE TABLE Item (
  Name VARCHAR(45),
  ArticleID INT,
  ItemType VARCHAR(45),
  Price DOUBLE,
  SellerID INT,
  Image TEXT,
  PRIMARY KEY (ArticleID))
''')

connection.execute('''INSERT INTO Item VALUES ("Dell Laptop", 354134, "Electronic", 800.00, 789853, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Red Balloon", 135413, "Misc", 2.00, 783123, "");
''')
connection.execute('''INSERT INTO Item VALUES ("IPhone X", 316895, "Electronic", 799.00, 789853, "");
''')
connection.execute('''INSERT INTO Item VALUES ("LG Television", 486135, "Electronic", 300.00, 789853, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Gucci Shirt", 987312, "Clothing", 500.00, 619619, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Amiri Jeans", 453135, "Clothing", 1000.00, 619619, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Burberry Headband", 786652, "Clothing", 200.00, 619619, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Samsung Television", 456321, "Electronic", 400.00, 789853, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Brown Chair", 789543, "Furniture", 40.00, 326421, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Black Table", 643192, "Furniture", 45.00, 326421, "");
''')
connection.execute('''INSERT INTO Item VALUES ("White Bed", 782152, "Furniture", 250.00, 326421, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Persian Rug", 786333, "Furniture", 75.00, 326421, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Avengers Blueray Movie", 996511, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Lord of the Rings Blueray Movie", 996512, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Star Wars Blueray Movie", 996513, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Lion King Blueray Movie", 996514, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Frozen Blueray Movie", 996515, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Get Out Blueray Movie", 996516, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Aquaman Blueray Movie", 996517, "Entertainment", 25.00, 778966, "");
''')
connection.execute('''INSERT INTO Item VALUES ("The Dark Knight Blueray Movie", 996518, "Entertainment", 25.00, 778966, "");
''')


connection.execute('''CREATE TABLE Customer (
  CustomerID INT,
  PhoneNumber VARCHAR(45),
  FirstName VARCHAR(45),
  LastName VARCHAR(45),
  EmailID VARCHAR(45),
  Password TEXT,
  Address VARCHAR(100),
  PRIMARY KEY (CustomerID));
''')

connection.execute('''INSERT INTO Customer VALUES (987542, 3476586391, "Mo", "Jahan", "mohammed.jahan@stonybrook.edu", "123", "123 Main St");
''')
connection.execute('''INSERT INTO Customer VALUES (987543, 1234567890, "Tamieem", "Jaffary", "tamieem.jaffary@stonybrook.edu" , "123", "456 Stony Book");
''')
connection.execute('''INSERT INTO Customer VALUES (987544, 0987654321, "Rahim", "Ahamed", "rahim.ahamed@stonybrook.edu", "123", "789 New York");
''')

connection.execute('''CREATE TABLE Payment (
  CustomerID INT  ,
  PaymentType VARCHAR(45),
  CardNumber INT  ,
  CardExpirationDate DATE,
  PRIMARY KEY (CustomerID, CardNumber));
''')

connection.execute('''INSERT INTO Payment VALUES(987542, "Credit Card", 1234567890, '2019-11-11');
''')
connection.execute('''INSERT INTO Payment VALUES(987543, "VISA", 4567890, '2020-12-12');
''')
connection.execute('''INSERT INTO Payment VALUES(987544, "Debit Card", 1237890, '2021-1-11');
''')

connection.execute('''CREATE TABLE Shipment(
  ShipmentID INT  ,
  ShipmentType VARCHAR(45),
  PhysicalAddress VARCHAR(45),
  ShipmentCharge DOUBLE,
  ShipmentDetails VARCHAR(100),
  OrderID INT UNIQUE ,
  PRIMARY KEY (ShipmentID));

''')

connection.execute('''INSERT INTO Shipment VALUES(654255, "Expedited", "123 Main Str", 11.99, "Please knock before dropping off shipment.", 0001);
''')
connection.execute('''INSERT INTO Shipment VALUES(654256, "Regular", "123 Main Str", 6.99, "Please knock before dropping off shipment.", 0002);
''')

connection.execute('''CREATE TABLE Orders (
  OrderID INT  ,
  TotalPrice DOUBLE NULL,
  PlacedOn DATE NULL,
  PRIMARY KEY (OrderID));

''')

connection.execute('''INSERT INTO Orders VALUES(000001, 802, '2019-04-14');
''')
connection.execute('''INSERT INTO Orders VALUES(000002, 802, '2019-04-14');
''')

connection.execute('''CREATE TABLE Reviews (
  ArticleID INT,
  SellerID INT,
  CustomerID INT,
  Ratings INT,
  DetailedReview VARCHAR(100),
  PRIMARY KEY (ArticleID, SellerID, CustomerID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer(CustomerID),
  FOREIGN KEY (ArticleID)
    REFERENCES Item(ArticleID),
 FOREIGN KEY (SellerID)
    REFERENCES Item(SellerID));
''')

connection.execute('''INSERT INTO Reviews VALUES(354134, 789853, 987544, 3, 'Faulty keyboard');
''')
connection.execute('''INSERT INTO Reviews VALUES(135413, 783123, 987543, 5, 'No issues');
''')

connection.execute('''CREATE TABLE Employee(
  EmployeeID INT,
  Role VARCHAR(45) ,
  DateJoined DATE,
  SupervisorID INT,
  PRIMARY KEY (EmployeeID));
''')

connection.execute('''INSERT INTO Employee VALUES(0002, 'Supervisor', '2010-12-25', NULL);
''')
connection.execute('''INSERT INTO Employee VALUES(0001, 'Employee', '2012-03-09', 0002);
''')

connection.execute('''CREATE TABLE ShoppingCart(
  ArticleID INT,
  CustomerID INT,
  TotalPrice DOUBLE,
  PricePerItem DOUBLE,
  QuantityOfItems DOUBLE,
  ItemsBought DOUBLE,
  PRIMARY KEY (CustomerID, ArticleID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer(CustomerID),
  FOREIGN KEY (ArticleID)
    REFERENCES Item(ArticleID));
''')



connection.execute('''CREATE TABLE Inventory(
  ItemID INT,
  ItemName VARCHAR(45),
  Quantity INT,
  Price DOUBLE,
  SellerID INT ,
  PRIMARY KEY (ItemID));
''')

connection.execute('''INSERT INTO Inventory VALUES(354134, 'Dell Laptop', 30, 800.00, 789853);
''')
connection.execute('''INSERT INTO Inventory VALUES(135413, 'Red Balloon', 100, 2.00, 783123);
''')
connection.execute('''INSERT INTO Inventory VALUES(316895, 'IPhone X', 100, 799.00, 789853);
''')
connection.execute('''INSERT INTO Inventory VALUES(486135, 'LG Television', 100, 300.00, 789853);
''')
connection.execute('''INSERT INTO Inventory VALUES(987312, 'Gucci Shirt', 100, 500.00, 619619);
''')
connection.execute('''INSERT INTO Inventory VALUES(453135, 'Amiri Jeans', 100, 1000.00, 619619);
''')
connection.execute('''INSERT INTO Inventory VALUES(786652, 'Burberry Headband', 100, 200.00, 619619);
''')
connection.execute('''INSERT INTO Inventory VALUES(456321, 'Samsung Television', 100, 400.00, 789853);
''')
connection.execute('''INSERT INTO Inventory VALUES(789543, 'Brown Chair', 100, 40.00, 326421);
''')
connection.execute('''INSERT INTO Inventory VALUES(643192, 'Black Table', 100, 45.00, 326421);
''')
connection.execute('''INSERT INTO Inventory VALUES(782152, 'White Bed', 100, 250.00, 326421);
''')
connection.execute('''INSERT INTO Inventory VALUES(786333, 'Persian Rug', 100, 75.00, 326421);
''')
connection.execute('''INSERT INTO Inventory VALUES(996511, 'Avengers Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996512, 'Lord of the Rings Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996513, 'Star Wars Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996514, 'Lion King Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996515, 'Frozen Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996516, 'Get Out Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996517, 'Aquaman Blueray Movie', 100, 25.00, 778966);
''')
connection.execute('''INSERT INTO Inventory VALUES(996518, 'The Dark Knight Blueray Movie', 100, 25.00, 778966);
''')

connection.execute('''CREATE TABLE _adds_item_to_cart_ (
  Quantity INT,
  CustomerID INT,
  ShoppingCartID INT,
  ArticleID INT,
  SellerID INT,
  PRIMARY KEY (ArticleID, ShoppingCartID, CustomerID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer(CustomerID),
  FOREIGN KEY (ArticleID)
    REFERENCES Item(ArticleID),
  FOREIGN KEY (ShoppingCartID)
    REFERENCES ShoppingCart(ShoppingCartID),
  FOREIGN KEY (SellerID)
    REFERENCES Item(SellerID));
''')

connection.execute('''INSERT INTO _adds_item_to_cart_ VALUES(2, 0001, 0001, 0001, 0001);
''')
connection.execute('''INSERT INTO _adds_item_to_cart_ VALUES(2, 0002, 0002, 0002, 0002);
''')

connection.execute('''CREATE TABLE _has_ (
  ArticleID INT ,
  SellerID INT,
  CustomerID INT,
  PRIMARY KEY (ArticleID, SellerID, CustomerID),
  FOREIGN KEY (ArticleID)
    REFERENCES Item(ArticleID),
  FOREIGN KEY (SellerID)
    REFERENCES Item(SellerID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer(CustomerID));
''')

connection.execute('''INSERT INTO _has_ VALUES(0001, 0001, 0001);
''')
connection.execute('''INSERT INTO _has_ VALUES(0002, 0002, 0002);
''')

connection.execute('''CREATE TABLE  _contains_(
  ArticleID INT,
  ShoppingCartID INT,
  PRIMARY KEY (ArticleID, ShoppingCartID),
  FOREIGN KEY (ArticleID)
    REFERENCES Item(ArticleID),
  FOREIGN KEY (ShoppingCartID)
    REFERENCES ShoppingCart(ShoppingCartID));
''')

connection.execute('''INSERT INTO _contains_ VALUES(0001, 0001);
''')
connection.execute('''INSERT INTO _contains_ VALUES(0002, 0002);
''')

connection.execute('''CREATE TABLE _maintains_(
  EmployeeID INT,
  ItemID INT,
  PRIMARY KEY (EmployeeID, ItemID),
    FOREIGN KEY (EmployeeID)
    REFERENCES Employee(EmployeeID),
    FOREIGN KEY (ItemID)
    REFERENCES Inventory(ItemID));
''')

connection.execute('''INSERT INTO _maintains_ VALUES(0001, 0001);
''')
connection.execute('''INSERT INTO _maintains_ VALUES(0002, 0002);
''')

connection.execute('''CREATE TABLE _creates_ (
  CustomerID INT,
  OrderID INT,
  PRIMARY KEY (CustomerID, OrderID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer (CustomerID),
  FOREIGN KEY (OrderID)
    REFERENCES Orders (OrderID));
''')

connection.execute('''INSERT INTO _creates_ VALUES(0001, 0001);
''')
connection.execute('''INSERT INTO _creates_ VALUES(0002, 0002);
''')

connection.execute('''CREATE TABLE _payed_by_ (
  CustomerID INT,
  OrderID INT,
  CardNumber INT,
  PRIMARY KEY (CustomerID, CardNumber, OrderID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer (CustomerID),
  FOREIGN KEY (OrderID)
    REFERENCES Orders (OrderID),
  FOREIGN KEY (CardNumber)
    REFERENCES Payment (CardNumber)
   );
''')

connection.execute('''INSERT INTO _payed_by_ VALUES(0001, 1234567890, 0001);
''')
connection.execute('''INSERT INTO _payed_by_ VALUES(0002, 4567890, 0002);
''')

connection.execute('''CREATE TABLE _shipped_ (
  ShipmentID INT ,
  OrderID INT,
  PRIMARY KEY (ShipmentID),
  FOREIGN KEY (ShipmentID)
    REFERENCES Shipment(ShipmentID),
  FOREIGN KEY (OrderID)
    REFERENCES Orders(OrderID)
   );
''')

connection.execute('''INSERT INTO _shipped_ VALUES(0001, 0001);
''')
connection.execute('''INSERT INTO _shipped_ VALUES(0002, 0002);
''')

connection.execute('''CREATE TABLE _carries_ (
  OrderID INT,
  ShoppingCartID INT,
  PRIMARY KEY (OrderID),
  FOREIGN KEY (OrderID)
    REFERENCES Orders (OrderID),
  FOREIGN KEY (ShoppingCartID)
    REFERENCES ShoppingCart (ShoppingCartID)
   );
''')

connection.execute('''INSERT INTO _carries_ VALUES(0001, 0001);
''')
connection.execute('''INSERT INTO _carries_ VALUES(0002, 0002);
''')

connection.execute('''CREATE TABLE _verifies_ (
  EmployeeID INT,
  CardNumber INT,
  ShipmentID INT,
  PRIMARY KEY (EmployeeID, CardNumber, ShipmentID),
  FOREIGN KEY (EmployeeID)
    REFERENCES Employee(EmployeeID),
  FOREIGN KEY (CardNumber)
    REFERENCES Payment (CardNumber),
  FOREIGN KEY (ShipmentID)
    REFERENCES Shipment(ShipmentID)
   );
''')

connection.execute('''INSERT INTO _verifies_ VALUES(0001, 1234567890, 0001);
''')
connection.execute('''INSERT INTO _verifies_ VALUES(0002, 4567890, 0002);
''')

crsr = connection.cursor()

connection.commit()

connection.close()