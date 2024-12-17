CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    coins INT DEFAULT 0,
    level INT DEFAULT 1,
    experience INT DEFAULT 0,
    energy INT DEFAULT 100,
    energy_max INT DEFAULT 100,
    mining_power INT DEFAULT 1,
    total_trained INT DEFAULT 0,
    total_mined INT DEFAULT 0
);

CREATE TABLE battle_pass (
    user_id BIGINT PRIMARY KEY,
    level INT DEFAULT 1,
    exp INT DEFAULT 0,
    is_premium BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE farms (
    user_id BIGINT PRIMARY KEY,
    level INT DEFAULT 1,
    production_rate FLOAT DEFAULT 10.0,
    last_collection TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE inventory (
    user_id BIGINT,
    item_id INT,
    quantity INT DEFAULT 1,
    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
