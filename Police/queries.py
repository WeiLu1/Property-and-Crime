create_crimes_table = """
CREATE TABLE IF NOT EXISTS crimes (
    id INTEGER NOT NULL PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    borough VARCHAR(30) NOT NULL
);
"""

insert_crime = """
INSERT INTO crimes (id, date, borough, category) VALUES ({},{},{},{})
ON CONFLICT (id) DO NOTHING;
"""