CREATE TABLE Hotels (
    hotel_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    address_street1 VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    hotel_class DECIMAL(3,1),
    hotel_class_attribution VARCHAR(255),
    main_image_url VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(255),
    web_url VARCHAR(255),
    price_level VARCHAR(10),
    price_range VARCHAR(100),
    ranking_denominator INT,
    ranking_position INT,
    ranking_string VARCHAR(255),
    rating DECIMAL(3,2)
) ENGINE=InnoDB;

-- Create ReviewScores table
CREATE TABLE ReviewScores (
    review_score_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT UNSIGNED NOT NULL,
    category_name VARCHAR(255),
    score DECIMAL(5,2),
    category_order INT,
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create MetroStations table
CREATE TABLE MetroStations (
    metro_station_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT UNSIGNED NOT NULL,
    name VARCHAR(255),
    address VARCHAR(255),
    distance VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create MetroLines table
CREATE TABLE MetroLines (
    metro_line_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    metro_station_id INT UNSIGNED NOT NULL,
    line_id VARCHAR(50),
    line_name VARCHAR(255),
    line_symbol VARCHAR(50),
    system_symbol VARCHAR(50),
    FOREIGN KEY (metro_station_id) REFERENCES MetroStations(metro_station_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create Photos table
CREATE TABLE Photos (
    photo_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT UNSIGNED NOT NULL,
    photo_url VARCHAR(255),
    photo_order INT,
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create ReviewTags table
CREATE TABLE ReviewTags (
    review_tag_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT UNSIGNED NOT NULL,
    tag_text VARCHAR(255),
    review_count INT,
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create RoomTips table
CREATE TABLE RoomTips (
    room_tip_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT UNSIGNED NOT NULL,
    tip_text TEXT,
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE
) ENGINE=InnoDB;