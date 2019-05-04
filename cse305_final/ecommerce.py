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

connection.execute('''INSERT INTO Item VALUES ("Laptop", 0001, "Electronic", 800.00, 0001, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Balloon", 0002, "Misc", 2.00, 0003, "");
''')
connection.execute('''INSERT INTO Item VALUES ("IPhone X", 0003, "Electronic", 799.00, 0001, "");
''')
connection.execute('''INSERT INTO Item VALUES ("Television", 0004, "Electronic", 300.00, 0005, "");
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

connection.execute('''CREATE TABLE Payment (
  OrderID INT  ,
  PaymentType VARCHAR(45),
  CardNumber INT  ,
  CardExpirationDate DATE,
  PRIMARY KEY (OrderID, CardNumber));
''')

connection.execute('''INSERT INTO Payment VALUES(0001, "Credit Card", 1234567890, '2019-11-11');
''')
connection.execute('''INSERT INTO Payment VALUES(0002, "VISA", 4567890, '2020-12-12');
''')
connection.execute('''INSERT INTO Payment VALUES(0003, "Debit Card", 1237890, '2021-1-11');
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

connection.execute('''INSERT INTO Shipment VALUES(0001, "Expedited", "123 Main Str", 11.99, "Please knock before dropping off shipment.", 0001);
''')
connection.execute('''INSERT INTO Shipment VALUES(0002, "Regular", "123 Main Str", 6.99, "Please knock before dropping off shipment.", 0002);
''')

connection.execute('''CREATE TABLE Orders (
  OrderID INT  ,
  TotalPrice DOUBLE NULL,
  PlacedOn DATE NULL,
  PRIMARY KEY (OrderID));

''')

connection.execute('''INSERT INTO Orders VALUES(0001, 802, '2019-04-14');
''')
connection.execute('''INSERT INTO Orders VALUES(0002, 802, '2019-04-14');
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

connection.execute('''INSERT INTO Reviews VALUES(0001, 0001, 0003, 3, 'Faulty keyboard');
''')
connection.execute('''INSERT INTO Reviews VALUES(0002, 0003, 0002, 5, 'No issues');
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
  ShoppingCartID INT,
  TotalPrice DOUBLE,
  PricePerItem VARCHAR(100),
  QuantityOfItems VARCHAR(100),
  ItemsBought VARCHAR(100),
  PRIMARY KEY (CustomerID, ArticleID),
  FOREIGN KEY (CustomerID)
    REFERENCES Customer(CustomerID),
  FOREIGN KEY (ArticleID)
    REFERENCES Item(ArticleID));
''')

connection.execute('''INSERT INTO ShoppingCart VALUES(0001, 802, '800 2', '1 1', '0001 0002');
''')
connection.execute('''INSERT INTO ShoppingCart VALUES(0002, 1642, '800 2', '2 21', '0001 0002');
''')

connection.execute('''CREATE TABLE Inventory(
  ItemID INT,
  ItemName VARCHAR(45),
  Quantity INT,
  Price DOUBLE,
  SellerID INT ,
  PRIMARY KEY (ItemID));
''')

connection.execute('''INSERT INTO Inventory VALUES(0001, 'Laptop', 30, 800, 0001);
''')
connection.execute('''INSERT INTO Inventory VALUES(0002, 'Balloon', 100, 2, 0001);
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