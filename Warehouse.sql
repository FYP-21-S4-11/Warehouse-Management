
/*UPDATED VERSION*/

CREATE TABLE `Admin` (
  `Username` varchar(255) NOT NULL,
  `FullName` varchar(255) DEFAULT NULL,
  `AdminPW` varchar(255) DEFAULT NULL,
  `AdminPhone` varchar(255) DEFAULT NULL,
  `AdminAddress` varchar(255) DEFAULT NULL,
  `AdminEmail` varchar(255) DEFAULT NULL,
  `Type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Username`)
);

CREATE TABLE `Supervisor` (
  `Username` varchar(255) NOT NULL,
  `FullName` varchar(255) DEFAULT NULL,
  `SupervisorPW` varchar(255) DEFAULT NULL,
  `SupervisorPhone` varchar(255) DEFAULT NULL,
  `SupervisorAddress` varchar(255) DEFAULT NULL,
  `SupervisorEmail` varchar(255) DEFAULT NULL,
  `Type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Username`)
)

CREATE TABLE `Supplier` (
  `SupplierCode` varchar(255) NOT NULL,
  `SupplierName` varchar(255) DEFAULT NULL,
  `SupplierPhone` varchar(255) DEFAULT NULL,
  `SupplierAddress` varchar(255) DEFAULT NULL,
  `SupplierPassword` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SupplierCode`)
);

CREATE TABLE `Product` (
  `ProductSKU` varchar(255) NOT NULL,
  `ProductName` varchar(255) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `ProductType` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ProductSKU`)
);

CREATE TABLE `Store` (
  `StoreCode` varchar(255) NOT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`StoreCode`)
);

CREATE TABLE `Inventory` (
  `InventoryID` varchar(255) NOT NULL,
  `StoreCode` varchar(255) NOT NULL,
  `ProductSKU` varchar(255) NOT NULL,
  `ProductName` varchar(255) DEFAULT NULL,
  `QuantityCurrent` int DEFAULT NULL,
  `DateIn` date DEFAULT NULL,
  `TimeIn` time DEFAULT NULL,
  `QuantityOutgoing` int DEFAULT NULL,
  `DateOut` date DEFAULT NULL,
  `TimeOut` time DEFAULT NULL,
  `Reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`InventoryID`),
  KEY `ProductSKU` (`ProductSKU`),
  KEY `StoreCode` (`StoreCode`),
  KEY `ProductName` (`ProductName`),
  CONSTRAINT `ProductSKU` FOREIGN KEY (`ProductSKU`) REFERENCES `Product` (`ProductSKU`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `StoreCode` FOREIGN KEY (`StoreCode`) REFERENCES `Store` (`StoreCode`) ON DELETE CASCADE ON UPDATE CASCADE
) ;

CREATE TABLE `Stock` (
  `StockSKU` varchar(255) NOT NULL,
  `StockName` varchar(255) DEFAULT NULL,
  `SupplierCode` varchar(255) DEFAULT NULL,
  `QuantityCurrent` int DEFAULT NULL,
  `DateIn` date DEFAULT NULL,
  `TimeIn` time DEFAULT NULL,
  `QuantityOutgoing` int DEFAULT NULL,
  `DateOut` date DEFAULT NULL,
  `TimeOut` time DEFAULT NULL,
  `Reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`StockSKU`),
  KEY `SupplierCode` (`SupplierCode`),
  CONSTRAINT `SupplierCode` FOREIGN KEY (`SupplierCode`) REFERENCES `Supplier` (`SupplierCode`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `Report` (
  `ReportID` int NOT NULL,
  `ReportName` varchar(255) NOT NULL,
  `InventoryID` varchar(255) NOT NULL,
  `DateStart` date DEFAULT NULL,
  `DateEnd` date DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ReportID`),
  KEY `InventoryID` (`InventoryID`),
  CONSTRAINT `InventoryID` FOREIGN KEY (`InventoryID`) REFERENCES `Inventory` (`InventoryID`) ON DELETE CASCADE ON UPDATE CASCADE
);


/*
CREATE TABLE `User` (
  `Username` varchar(255) NOT NULL,
  `FullName` varchar(255) DEFAULT NULL,
  `UserPW` varchar(255) DEFAULT NULL,
  `UserPhone` varchar(255) DEFAULT NULL,
  `UserAddress` varchar(255) DEFAULT NULL,
  `UserEmail` varchar(255) DEFAULT NULL,
  `UserType` varchar(255) DEFAULT NULL
  PRIMARY KEY (`Username`));

*/
