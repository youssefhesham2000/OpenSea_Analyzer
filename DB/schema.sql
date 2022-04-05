-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nft_openSea
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema nft_openSea
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nft_openSea` ;
USE `nft_openSea` ;

-- -----------------------------------------------------
-- Table `nft_openSea`.`URL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nft_openSea`.`URL` (
  `ID` INT NOT NULL,
  `URL` VARCHAR(1000) NOT NULL,
  `version` INT NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nft_openSea`.`EVENT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nft_openSea`.`EVENT` (
  `ID` INT NOT NULL,
  `event_name` VARCHAR(45) NOT NULL,
  `event_date` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`),
   INDEX `EVENT_URL_FK_idx` (`ID` ASC) VISIBLE,
  CONSTRAINT `EVENT_URL_FK`
    FOREIGN KEY (`ID`)
    REFERENCES `nft_openSea`.`URL` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nft_openSea`.`OFFER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nft_openSea`.`OFFER` (
  `ID` INT NOT NULL,
  `offer_price` DECIMAL NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `OFFER_URL_FK_idx` (`ID` ASC) VISIBLE,
   CONSTRAINT `OFFER_URL_FK`
    FOREIGN KEY (`ID`)
    REFERENCES `nft_openSea`.`URL` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nft_openSea`.`NFT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nft_openSea`.`NFT` (
  `ID` INT NOT NULL,
  `nft_name` VARCHAR(45) NOT NULL,
  `faviorites_num` INT NOT NULL,
  `highest_bid` DECIMAL NOT NULL,
  PRIMARY KEY (`ID`),
 INDEX `NFT_URL_FK_idx` (`ID` ASC) VISIBLE,
  CONSTRAINT `NFT_URL_FK`
    FOREIGN KEY (`ID`)
    REFERENCES `nft_openSea`.`URL` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
