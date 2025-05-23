CREATE TABLE IF NOT EXISTS urls (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE DEFAULT CURRENT_DATE
);


CREATE TABLE IF NOT EXISTS url_checks (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	url_id INT NOT NULL REFERENCES urls(id) ON DELETE CASCADE,
	status_code INTEGER,
	h1 TEXT,
    title TEXT,
    description TEXT,
    created_at DATE DEFAULT CURRENT_DATE
);