
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
);

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
);

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
  KEY `SupplierCode_idx` (`SupplierCode`),
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

/* OLD VERSION 


CREATE TABLE `Admin` (
  `FullName` VARCHAR(255) NOT NULL,
  `Username` VARCHAR(255) NOT NULL,
  `AdminPW` VARCHAR(255) NOT NULL,
  `AdminPhone` VARCHAR(255) NOT NULL,
  `AdminAddress` VARCHAR(255) NOT NULL,
  `AdminEmail` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`Username`));

CREATE TABLE `Supervisor` (
  `Username` VARCHAR(255) NOT NULL,
  `FullName` VARCHAR(255) NOT NULL,
  `SupervisorPW` VARCHAR(255) NOT NULL,
  `SupervisorPhone` VARCHAR(255) NOT NULL,
  `SupervisorAddress` VARCHAR(255) NOT NULL,
  `SupervisorEmail` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`Username`));

CREATE TABLE `Store` (
  `StoreCode` VARCHAR(255) NOT NULL,
  `Location` VARCHAR(255) NOT NULL,
  `Address` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`StoreCode`));

CREATE TABLE `Supplier` (
  `SupplierCode` VARCHAR(255) NOT NULL,
  `SupplierName` VARCHAR(255) NOT NULL,
  `SupplierPhone` VARCHAR(255) NOT NULL,
  `SupplierAddress` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`SupplierCode`));

CREATE TABLE `Product` (
  `ProductSKU` VARCHAR(255) NOT NULL,
  `ProductName` VARCHAR(255) NOT NULL,
  `Description` VARCHAR(255) NOT NULL,
  `ProductType` VARCHAR(255) NULL,
  PRIMARY KEY (`ProductSKU`),
  CONSTRAINT `SupCode`
    FOREIGN KEY (`ProductSKU`)
    REFERENCES `Supplier` (`SupplierCode`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `Inventory` (
  `InventorySKU` VARCHAR(255) NOT NULL,
  `InventoryName` VARCHAR(255) NOT NULL,
  `Reason` VARCHAR(255) NOT NULL,
  `Quantity` VARCHAR(255) NOT NULL,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`InventorySKU`),
  CONSTRAINT `StoreCode`
    FOREIGN KEY (`InventorySKU`)
    REFERENCES `Store` (`StoreCode`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `Stock` (
  `StockSKU` VARCHAR(255) NOT NULL,
  `StockName` VARCHAR(255) NOT NULL,
  `Reason` VARCHAR(255) NOT NULL,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`StockSKU`),
  CONSTRAINT `SupplyCode`
    FOREIGN KEY (`StockSKU`)
    REFERENCES `Supplier` (`SupplierCode`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `Report` (
  `ReportCode` VARCHAR(255) NOT NULL,
  `Start-Date` DATE NOT NULL,
  `End-Date` DATE NOT NULL,
  PRIMARY KEY (`ReportCode`));

  */