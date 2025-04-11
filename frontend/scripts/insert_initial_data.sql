-- SQL script to insert initial data into the database

-- Administrator User
INSERT INTO users (
    id, 
    first_name, 
    last_name, 
    email, 
    password, 
    role, 
    is_admin, 
    created_at, 
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', -- Fixed ID for admin
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$YD1PhhClixw7Sx6j/erEY.LpKQX2zpJD.BY.hmRicIadoww49XBPC', -- Bcrypt hash for 'admin1234'
    'admin',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Initial Amenities
INSERT INTO amenities (
    id,
    name,
    created_at,
    updated_at
) VALUES (
    '3a44996f-9ead-4529-a0db-f5e840a21e9c', -- Generated UUID
    'WiFi',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (
    id,
    name,
    created_at,
    updated_at
) VALUES (
    '0daa90ac-75ff-4171-a788-75e7f9c05099', -- Generated UUID
    'Swimming Pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (
    id,
    name,
    created_at,
    updated_at
) VALUES (
    'b469df04-eab0-4b9b-b3de-2b8a03e4eb9e', -- Generated UUID
    'Air Conditioning',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
