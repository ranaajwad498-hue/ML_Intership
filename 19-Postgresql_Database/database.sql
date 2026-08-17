CREATE TABLE districts(
	d_id INT PRIMARY KEY,
	d_name VARCHAR(255) NOT NULL,
	province VARCHAR(255) NOT NULL,
	create_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO districts VALUES
(1, 'Mardan', 'KPK'),
(2, 'Rawalpindi', 'Punjab'),
(3, 'Karachi', 'Sindh');






CREATE TABLE users(
	u_id INT PRIMARY KEY,
	u_name VARCHAR(255) NOT NULL,
	email VARCHAR NOT NULL UNIQUE,
	password TEXT NOT NULL,
	u_role VARCHAR(255) NOT NULL,
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO users VALUES 
(1, 'AJWAD', 'ajwad@gmail.com', crypt('ADMIN',gen_salt('bf')),'Admin'),
(2, 'Ali', 'ali@gmail.com', crypt('USER',gen_salt('bf')), 'Health_Worker'),
(3, 'USMAN', 'usman@gmail.com', crypt('USER', gen_salt('bf')), 'Health_Worker');






CREATE TABLE health_worker(
	h_id INT PRIMARY KEY,
	user_id BIGINT REFERENCES users(u_id) NOT NULL,
	district_id BIGINT REFERENCES districts(d_id) NOT NULL,
	phone VARCHAR(20) NOT NULL,
	desgination VARCHAR(255) NOT NULL,
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO health_worker VALUES
(1, 1, 1, '+92 319 6511304', 'Employ'),
(2, 2, 2, '+92 319 6511008', 'Employ');






CREATE TABLE children(
	c_id INT PRIMARY KEY,
	c_name VARCHAR(255) NOT NULL,
	age_months INT CHECK(age_months > 0) NOT NULL,
	gender VARCHAR(255) NOT NULL,
	weight_kg INT CHECK(weight_kg > 0) NOT NULL,
	height_cm INT CHECK (height_cm > 0) NOT NULL,
	district_id BIGINT REFERENCES districts(d_id) NOT NULL,
	health_worker_id BIGINT REFERENCES health_worker(h_id) NOT NULL,
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO children VALUES
(1, 'Imran', 4, 'Male', 3, 2, 1, 2),
(2, 'Saqib', 6, 'Male', 4, 3, 2, 1),
(3, 'Noor', 3, 'Female', 3, 4, 3, 1),
(4, 'Fatima', 4, 'Female', 4, 5, 1, 2),
(5, 'Faisal', 5 ,'Male', 6, 4, 3, 2);






CREATE TABLE prediction(
	p_id INT PRIMARY KEY,
	child_id BIGINT REFERENCES children(c_id) NOT NULL,
	risk_score INT CHECK(risk_score > 0) NOT NULL,
	risk_category VARCHAR(255) NOT NULL,
	confidence VARCHAR NOT NULl,
	reasons VARCHAR (255) NOT NULL,
	model_name VARCHAR(255) NOT NULL,
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO prediction VALUES
(1, 1, 50, 'At_Risk', 0.5, 'Under_Weight, Younger_Age', 'Random Forest'),
(2, 2, 80, 'High_Risk', 0.8, 'Over_Weight, Low_BMI, Younger_Age', 'Decision Tree'),
(3, 3, 10, 'Normal', 0.1, 'High_BMI', 'Logistic Regression'),
(4, 4, 90, 'Malnourished', 0.9, 'Over_Weight, Low_BMI', 'Decison Tree'),
(5, 5, 5, 'Normal', 0.5, 'Under_Weight, Low_BMI', 'Random Forest ');

-- Runing Queries
SELECT * FROM children;
SELECT * FROM health_worker;
SELECT * FROM prediction;
SELECT * FROM children WHERE district_id= 1;
SELECT * FROM children WHERE health_worker_id= 2;
SELECT * FROM prediction WHERE child_id= 3;

SELECT 
    c.c_id AS Child_id, 
    c.c_name AS Child_Name, 
    c.age_months AS Age, 
    d.d_name AS District, 
    d.province AS Province,
    c.health_worker_id AS Health_Worker_ID
FROM children c 
INNER JOIN districts d ON c.district_id = d.d_id 
ORDER BY d.province;

