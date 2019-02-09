-- MySQL Script generated by MySQL Workbench
-- Sat Feb  9 18:46:00 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema ece1779a1
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `ece1779a1` ;

-- -----------------------------------------------------
-- Schema ece1779a1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ece1779a1` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `ece1779a1` ;

-- -----------------------------------------------------
-- Table `ece1779a1`.`images`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1779a1`.`images` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `ece1779a1`.`images` (
  `id` INT NOT NULL,
  `filepath` VARCHAR(200) NOT NULL,
  `description` VARCHAR(100) NULL,
  PRIMARY KEY (`id`));

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `ece1779a1`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1779a1`.`user` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `ece1779a1`.`user` (
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `id` INT NOT NULL,
  PRIMARY KEY (`id`));

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `ece1779a1`.`user_has_images`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1779a1`.`user_has_images` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `ece1779a1`.`user_has_images` (
  `user_id` INT NOT NULL,
  `images_id` INT NOT NULL,
  CONSTRAINT `fk_user_has_images_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `ece1779a1`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_images_images1`
    FOREIGN KEY (`images_id`)
    REFERENCES `ece1779a1`.`images` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

SHOW WARNINGS;
CREATE INDEX `fk_user_has_images_user_idx` ON `ece1779a1`.`user_has_images` (`user_id` ASC);

SHOW WARNINGS;
CREATE INDEX `fk_user_has_images_images1_idx` ON `ece1779a1`.`user_has_images` (`images_id` ASC);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
