DELIMITER //

CREATE PROCEDURE GetUserHabitsWithCompletion(IN userIDParam INT)
BEGIN

    DECLARE habitID INT;
    DECLARE habitTitle VARCHAR(255);
    DECLARE habitDescription VARCHAR(255);
    DECLARE habitStreak INT;
    DECLARE habitMaxStreak INT;
    DECLARE goalTitle VARCHAR(255);
    DECLARE goalCompleted INT;


    CREATE TEMPORARY TABLE TempUserHabitsWithCompletion (
        HabitID INT,
        HabitTitle VARCHAR(255),
        HabitDescription VARCHAR(255),
        HabitStreak INT,
        HabitMaxStreak INT,
        GoalTitle VARCHAR(255),
        GoalCompleted INT
    );

    INSERT INTO TempUserHabitsWithCompletion
    SELECT
        H.HabitID,
        H.Title AS HabitTitle,
        H.Description AS HabitDescription,
        H.Streak,
        H.MaxStreak,
        G.Title AS GoalTitle,
        G.Completed
    FROM
        Habits H
    LEFT JOIN
        Goals G ON H.HabitID = G.HabitID
    WHERE
        H.UserID = userIDParam;

    SELECT * FROM TempUserHabitsWithCompletion;

    DROP TEMPORARY TABLE IF EXISTS TempUserHabitsWithCompletion;
END //

DELIMITER ;



DELIMITER //

CREATE FUNCTION CalculateCompletionPercentage(habitIDParam INT) RETURNS FLOAT READS SQL DATA
BEGIN
    DECLARE totalGoals INT;
    DECLARE completedGoals INT;
    SELECT COUNT(*) INTO totalGoals FROM Goals WHERE HabitID = habitIDParam;
    SELECT COUNT(*) INTO completedGoals FROM Goals WHERE HabitID = habitIDParam AND Completed = 1;
    IF totalGoals > 0 THEN
        RETURN (completedGoals / totalGoals) * 100;
    ELSE
        RETURN 0;
    END IF;
END //

DELIMITER ;
  


DELIMITER //

CREATE TRIGGER BeforeGoalInsert
BEFORE INSERT ON Goals
FOR EACH ROW
BEGIN
  DECLARE habitStreak INT;
  SELECT Streak INTO habitStreak FROM Habits WHERE HabitID = NEW.HabitID;
  IF NEW.Completed = 1 THEN
    SET habitStreak = habitStreak + 1;
  ELSE
    SET habitStreak = 0;
  END IF;
  UPDATE Habits SET Streak = habitStreak WHERE HabitID = NEW.HabitID;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER update_completed_status
BEFORE UPDATE ON goals
FOR EACH ROW
BEGIN
    IF NEW.Counter = NEW.Target THEN
        SET NEW.Completed = 1;
    END IF;
END;
//

DELIMITER ;

