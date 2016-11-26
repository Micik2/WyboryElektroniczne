-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tas` DEFAULT CHARACTER SET utf8 ;
USE `tas` ;

-- -----------------------------------------------------
-- Table `mydb`.`OBYWATELE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tas`.`OBYWATELE` (
  `PESEL` VARCHAR(11) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `haslo` VARCHAR(45) NULL,
  PRIMARY KEY (`PESEL`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WYBORCY`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tas`.`WYBORCY` (
  `imie` NVARCHAR(45) NULL,
  `nazwisko` NVARCHAR(45) NULL,
  `nr_dowodu` VARCHAR(9) NULL,
  `ulica` NVARCHAR(45) NULL,
  `nr_lokalu` VARCHAR(45) NULL,
  `kod_pocztowy` VARCHAR(6) NULL,
  `miejscowosc` NVARCHAR(45) NULL,
  `czy_glosowal` TINYINT(1) NULL,
  `wyksztalcenie` NVARCHAR(45) NULL,
  `kraj_pochodzenia` VARCHAR(45) NULL,
  `wiek` INT NULL,obywatele
  `czy_ubezwlasnowolniony` TINYINT(1) NULL,
  `haslo_tymczasowe` VARCHAR(45) NOT NULL,
  `nr_telefonu` INT NULL,
  `OBYWATELE_PESEL` VARCHAR(11) NOT NULL,
  INDEX `fk_WYBORCY_OBYWATELE_idx` (`OBYWATELE_PESEL` ASC),
  UNIQUE INDEX `nr_dowodu_UNIQUE` (`nr_dowodu` ASC),
  UNIQUE INDEX `nr_telefonu_UNIQUE` (`nr_telefonu` ASC),
  CONSTRAINT `fk_WYBORCY_OBYWATELE`
    FOREIGN KEY (`OBYWATELE_PESEL`)
    REFERENCES `tas`.`OBYWATELE` (`PESEL`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

/*fffffffffffffffffffffffffffffffffffffffffffffffffffffff*/
SELECT * from Obywatele