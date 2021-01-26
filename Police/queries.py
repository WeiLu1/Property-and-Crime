create_crimes_table = """
CREATE TABLE IF NOT EXISTS crimes (
    id INTEGER NOT NULL PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    borough VARCHAR(30) NOT NULL
);
"""

insert_crime = """
INSERT INTO crimes (id, date, category, borough) VALUES (
    %(id)s,
    %(date)s,
    %(category)s,
    %(borough)s
) ON CONFLICT (id) DO NOTHING;
"""

create_crimes_index = """
CREATE INDEX borough_index ON crimes (borough);
"""

create_propertiesraw_table = """
CREATE TABLE propertiesraw (
borough VARCHAR(30) NOT NULL,
numberbeds INTEGER NOT NULL,
price INTEGER NOT NULL,
url VARCHAR(150) NOT NULL PRIMARY KEY
);
"""