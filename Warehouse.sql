
/*UPDATED VERSION*/

CREATE TABLE `Supplier` (
  `SupplierCode` VARCHAR(255) NOT NULL,
  `SupplierName` VARCHAR(255) DEFAULT NULL,
  `SupplierPhone` VARCHAR(255) DEFAULT NULL,
  `SupplierAddress` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`SupplierCode`));

CREATE TABLE `Admin` (
  `Username` VARCHAR(255) NOT NULL,
  `FullName` VARCHAR(255) DEFAULT NULL,
  `AdminPW` VARCHAR(255) DEFAULT NULL,
  `AdminPhone` VARCHAR(255) DEFAULT NULL,
  `AdminAddress` VARCHAR(255) DEFAULT NULL,
  `AdminEmail` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`Username`));

CREATE TABLE `Supervisor` (
  `Username` VARCHAR(255) NOT NULL,
  `FullName` VARCHAR(255) DEFAULT NULL,
  `SupervisorPW` VARCHAR(255) DEFAULT NULL,
  `SupervisorPhone` VARCHAR(255) DEFAULT NULL,
  `SupervisorAddress` VARCHAR(255) DEFAULT NULL,
  `SupervisorEmail` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`Username`));

CREATE TABLE `Product` (
  `ProductSKU` VARCHAR(255) NOT NULL,
  `ProductName` VARCHAR(255) DEFAULT NULL,
  `Description` VARCHAR(255) DEFAULT NULL,
  `ProductType` VARCHAR(255) DEFAULT NULL,
  `ReturnReason` VARCHAR(255) DEFAULT NULL,
  `Quantity` INT DEFAULT NULL,
  `Date` DATE DEFAULT NULL,
  PRIMARY KEY (`ProductSKU`));

CREATE TABLE `Store` (
  `StoreCode` VARCHAR(255) NOT NULL,
  `Location` VARCHAR(255) DEFAULT NULL,
  `Address` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`StoreCode`));

CREATE TABLE `Inventory` (
  `InventoryID` varchar(255) NOT NULL,
  `StoreCode` varchar(255) NOT NULL,
  `ProductSKU` varchar(255) NOT NULL,
  `ProductName` varchar(255) DEFAULT NULL,
  `Reason` varchar(255) DEFAULT NULL,
  `QuantityCurrent` int DEFAULT NULL,
  `DateIn` date DEFAULT NULL,
  `TimeIn` time DEFAULT NULL,
  `QuantityOutgoing` varchar(255) DEFAULT NULL,
  `DateOut` date DEFAULT NULL,
  `TimeOut` time DEFAULT NULL,
  PRIMARY KEY (`InventoryID`),
  KEY `ProductSKU` (`ProductSKU`),
  KEY `StoreCode` (`StoreCode`),
  KEY `ProductName` (`ProductName`),
  CONSTRAINT `ProductSKU` FOREIGN KEY (`ProductSKU`) REFERENCES `Product` (`ProductSKU`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `StoreCode` FOREIGN KEY (`StoreCode`) REFERENCES `Store` (`StoreCode`) ON DELETE CASCADE ON UPDATE CASCADE
));

CREATE TABLE `Stock` (
  `StockSKU` varchar(255) NOT NULL,
  `StockName` varchar(255) DEFAULT NULL,
  `SupplierCode` varchar(255) DEFAULT NULL,
  `Reason` varchar(255) DEFAULT NULL,
  `QuantityCurrent` int DEFAULT NULL,
  `DateIn` date DEFAULT NULL,
  `TimeIn` time DEFAULT NULL,
  `QuantityOutgoing` int DEFAULT NULL,
  `DateOut` date DEFAULT NULL,
  `TimeOut` time DEFAULT NULL,
  PRIMARY KEY (`StockSKU`)
));

CREATE TABLE `Report` (
  `ReportCode` VARCHAR(255) NOT NULL,
  `Start-Date` DATE DEFAULT NULL,
  `End-Date` DATE DEFAULT NULL,
  PRIMARY KEY (`ReportCode`));

/*
CREATE TABLE `User` (
  `FullName` VARCHAR(255) NOT NULL,
  `Username` VARCHAR(255) NOT NULL,
  `UserPW` VARCHAR(255) NOT NULL,
  `UserPhone` VARCHAR(255) NOT NULL,
  `UserAddress` VARCHAR(255) NOT NULL,
  `UserEmail` VARCHAR(255) NOT NULL,
  `UserType` VARCHAR(255) NOT NULL,
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