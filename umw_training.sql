-- use "\i /umw_training/umw_training.sql" to reset all changes and reload this database. 
-- This is after logging in to postgres as "localhost" like normal. 
      --sudo service postgresql start
      --psql -U postgres -h localhost
      --password : cats123
-- After all of the create table and grant thing, doing this insert the password for the website user "umw16p91V2Hkl8m9"

DROP DATABASE IF EXISTS umw_training;
CREATE DATABASE umw_training;
DROP ROLE IF EXISTS website;
CREATE ROLE website with login; 
\c umw_training;


CREATE TABLE IF NOT EXISTS users (
  user_name text NOT NULL,
  password text NOT NULL,
  PRIMARY KEY (user_name)
);

create extension pgcrypto;

INSERT INTO users (user_name, password) VALUES
('mpokorny', crypt('p00d13', gen_salt('bf'))),
('ggreene', crypt('p00d13', gen_salt('bf'))),
('aperkins', crypt('changeme', gen_salt('bf'))),
('mdesorme', crypt('derp', gen_salt('bf'))),
('lass', crypt('qwerty', gen_salt('bf'))),
('1student', crypt('p00d13', gen_salt('bf'))),
('2student', crypt('changeme', gen_salt('bf'))),
('3student', crypt('qwerty', gen_salt('bf')));

CREATE TABLE IF NOT EXISTS admin (
  admin_id SERIAL NOT NULL,
  user_name text NOT NULL references users(user_name),
  first_name text NOT NULL,
  last_name text NOT NULL,
  email text NOT NULL,
  PRIMARY KEY (admin_id)
);

INSERT INTO admin (user_name, first_name, last_name, email) VALUES
('mpokorny', 'Michael', 'Pokorny', 'mpokorny@mail.umw.edu'),
('ggreene', 'George', 'Greene', 'ggreene@mail.umw.edu'),
('mdesorme', 'Michelle', 'Desormeaux', 'mdesorme@mail.umw.edu'),
('aperkins', 'Ann', 'Perkins', 'aperkins@mail.umw.edu'),
('lass', 'Lazy', 'Ass', 'lass@mail.umw.edu');

CREATE TABLE IF NOT EXISTS coaches (
  coach_id SERIAL NOT NULL,
  user_name text NOT NULL references users(user_name),
  first_name text NOT NULL,
  last_name text NOT NULL,
  sport text NOT NULL,
  email text NOT NULL,
  PRIMARY KEY (coach_id)
);

INSERT INTO coaches (user_name, first_name, last_name, sport, email) VALUES
('1coach', 'blah', 'blah', 'soccer', 'blah@mail.umw.edu'),
('2coach', 'blah', 'blah', 'basketball', 'blah@mail.umw.edu'),
('3coach', 'blah', 'blah', 'lacross', 'blah@mail.umw.edu');

CREATE TABLE IF NOT EXISTS trainers (
  trainer_id SERIAL NOT NULL,
  user_name text NOT NULL references users(user_name),
  first_name text NOT NULL,
  last_name text NOT NULL,
  email text NOT NULL,
  PRIMARY KEY (trainer_id)
);

INSERT INTO trainers (user_name, first_name, last_name, email) VALUES
('1trainer', 'blah', 'blah', 'blah@mail.umw.edu'),
('2trainer', 'blah', 'blah', 'blah@mail.umw.edu'),
('3trainer', 'blah', 'blah', 'blah@mail.umw.edu');

CREATE TABLE IF NOT EXISTS students (
  student_id SERIAL NOT NULL,
  user_name text NOT NULL references users(user_name),
  first_name text NOT NULL,
  last_name text NOT NULL,
  sport text NOT NULL,
  year INT NOT NULL,
  email text NOT NULL,
  one_rep_max INT,
  PRIMARY KEY (student_id)
);

INSERT INTO students (user_name, first_name, last_name, sport, year, email, one_rep_max) VALUES
('1student', 'blah', 'blah', 'soccer', 2016,'blah@mail.umw.edu', 150),
('2student', 'blah', 'blah', 'basketball', 2016,'blah@mail.umw.edu', NULL),
('3student', 'blah', 'blah', 'lacross', 2016,'blah@mail.umw.edu', 200);

CREATE TABLE IF NOT EXISTS admin_events (
  event_id SERIAL NOT NULL,
  admin_id INT NOT NULL references admin(admin_id),
  event_name text NOT NULL,
  date_start DATE NOT NULL,
  date_end DATE NOT NULL,
  color text NOT NULL,
  description text,
  PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS coach_events (
  event_id SERIAL NOT NULL,
  coach_id INT NOT NULL references coaches(coach_id),
  event_name text NOT NULL,
  date_start DATE NOT NULL,
  date_end DATE NOT NULL,
  color text NOT NULL,
  description text,
  PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS injury_reports (
  injury_report_id SERIAL NOT NULL,
  trainer_id INT NOT NULL references trainers(trainer_id),
  report_date DATE NOT NULL,
  PRIMARY KEY (injury_report_id)
);

CREATE TABLE IF NOT EXISTS injury_report_rows (
  row_id SERIAL NOT NULL,
  injury_report_id INT NOT NULL references injury_reports(injury_report_id),
  row_number INT NOT NULL,
  last_name text,
  first_name text,
  body_part text,
  nature_of_injury text,
  date_of_injury text,
  comments text,
  status text,
  lifting_restrictions text,
  sport text,
  PRIMARY KEY (row_id)
);

CREATE TABLE IF NOT EXISTS training_stats (
  stat_id SERIAL NOT NULL,
  stat_date DATE NOT NULL,
  stat_order INT NOT NULL,
  stat INT NOT NULL,
  PRIMARY KEY (stat_id)
);

CREATE TABLE IF NOT EXISTS student_to_stats (
  stat_id INT NOT NULL references training_stats(stat_id),
  student_id INT NOT NULL references students(student_id)
);

CREATE TABLE IF NOT EXISTS question_answers (
  answer_id SERIAL NOT NULL,
  answer_date DATE NOT NULL,
  answer_order INT NOT NULL,
  answer text NOT NULL,
  PRIMARY KEY (answer_id)
);

CREATE TABLE IF NOT EXISTS student_to_answers (
  answer_id INT NOT NULL references question_answers(answer_id),
  student_id INT NOT NULL references students(student_id)
);

CREATE TABLE IF NOT EXISTS exercises (
  exercise_id SERIAL NOT NULL,
  admin_id INT NOT NULL references admin(admin_id),
  exercise_name text NOT NULL,
  description text,
  muscle_group text NOT NULL,
  youtube_link text,
  PRIMARY KEY (exercise_id)
);

CREATE TABLE IF NOT EXISTS workouts (
  workout_id SERIAL NOT NULL,
  admin_id INT NOT NULL references admin(admin_id),
  workout_name text NOT NULL,
  PRIMARY KEY (workout_id)
);

INSERT INTO workouts (admin_id, workout_name) VALUES
(1, 'LOWER'),
(1, 'UPPER');

CREATE TABLE IF NOT EXISTS workout_exercises (
  exercise_id INT NOT NULL references exercises(exercise_id),
  workout_id INT NOT NULL references workouts(workout_id),
  row_1 text,
  row_2 text,
  row_3 text,
  row_4 text,
  row_5 text,
  comments text
);

--INSERT INTO workouts (exercise_id, workout_id, row_1, row_2, row3, comments) VALUES
--(24, 2,'50/5','60/3','4x70/2','(5s on the way down)'),
--(47, 2,'50/8','60/5','4x70/2','(5s on the way down)'),
--(47, 3,'50/8','60/5','4x70/2','(5s on the way up)');

CREATE TABLE IF NOT EXISTS training_programs (
  training_program_id SERIAL NOT NULL,
  admin_id INT NOT NULL references admin(admin_id),
  training_program_name text NOT NULL,
  sport text,
  student text,
  PRIMARY KEY (training_program_id)
);

CREATE TABLE IF NOT EXISTS training_program_workouts (
  workout_id INT NOT NULL references workouts(workout_id),
  training_program_id INT NOT NULL references training_programs(training_program_id),
  day_number INT,
  day_type text, -- this is going to be the muscle group for the day (see appendix in SRS for trining programs where it says "Upper" for upper body workout. That's an example.)
  week_number INT,
  workout_order INT --ask Michael about this when you come to it if you have questions... kinda confusing.
);

GRANT ALL ON users, admin, admin_admin_id_seq, coaches, coaches_coach_id_seq,
             trainers, trainers_trainer_id_seq, students, students_student_id_seq, 
             admin_events, admin_events_event_id_seq, coach_events, 
             coach_events_event_id_seq, injury_reports, 
             injury_reports_injury_report_id_seq,
             training_stats, training_stats_stat_id_seq,
             student_to_stats, question_answers, question_answers_answer_id_seq,
             student_to_answers, injury_report_rows, injury_report_rows_row_id_seq,
             exercises, exercises_exercise_id_seq, workouts, workouts_workout_id_seq,
             workout_exercises, training_programs, training_programs_training_program_id_seq,
             training_program_workouts to website;

\password website
--password is "umw16p91V2Hkl8m9"
