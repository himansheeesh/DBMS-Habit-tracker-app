CREATE DATABASE  IF NOT EXISTS `habit_tracker_app`
DROP TABLE IF EXISTS `goals`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `CreatedAt` date NOT NULL,
  `UpdatedAt` date NOT NULL,
  `Name` varchar(255) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `habits`;
CREATE TABLE `habits` (
  `HabitID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `CreatedAt` date NOT NULL,
  `UpdatedAt` date NOT NULL,
  `Streak` int NOT NULL,
  `MaxStreak` int NOT NULL,
  `UserID` int NOT NULL,
  PRIMARY KEY (`HabitID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `habits_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `goals` (
  `GoalID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `CreatedAt` date NOT NULL,
  `UpdatedAt` date NOT NULL,
  `Counter` int NOT NULL,
  `Target` int NOT NULL,
  `Completed` int NOT NULL,
  `HabitID` int NOT NULL,
  UNIQUE KEY `GoalID` (`GoalID`),
  KEY `HabitID` (`HabitID`),
  CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`HabitID`) REFERENCES `habits` (`HabitID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `rooms`;
CREATE TABLE `rooms` (
  `RoomID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `CreatedAt` date NOT NULL,
  `UpdatedAt` date NOT NULL,
  PRIMARY KEY (`RoomID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `leaderboards`;
CREATE TABLE `leaderboards` (
  `LeaderboardID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) NOT NULL,
  `CreatedAt` date NOT NULL,
  `UpdatedAt` date NOT NULL,
  `Description` varchar(255) NOT NULL,
  `Privacy` int NOT NULL,
  `RoomID` int NOT NULL,
  PRIMARY KEY (`LeaderboardID`),
  KEY `RoomID` (`RoomID`),
  CONSTRAINT `leaderboards_ibfk_1` FOREIGN KEY (`RoomID`) REFERENCES `rooms` (`RoomID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `reminders`;
CREATE TABLE `reminders` (
  `CreatedAt` date NOT NULL,
  `TimePeriod` date NOT NULL,
  `HabitID` int NOT NULL,
  `TimeLength` int NOT NULL,
  `TimeUnit` varchar(20) NOT NULL,
  KEY `FK_HabitID` (`HabitID`),
  CONSTRAINT `FK_HabitID` FOREIGN KEY (`HabitID`) REFERENCES `habits` (`HabitID`),
  CONSTRAINT `reminders_ibfk_1` FOREIGN KEY (`HabitID`) REFERENCES `habits` (`HabitID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `userrooms`;
CREATE TABLE `userrooms` (
  `UserID` int NOT NULL,
  `RoomID` int NOT NULL,
  PRIMARY KEY (`UserID`,`RoomID`),
  KEY `RoomID` (`RoomID`),
  CONSTRAINT `userrooms_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  CONSTRAINT `userrooms_ibfk_2` FOREIGN KEY (`RoomID`) REFERENCES `rooms` (`RoomID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

