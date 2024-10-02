CREATE DATABASE IF NOT EXISTS HuaYang$HuaYang777;
USE HuaYang$HuaYang777;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    status CHAR(2) DEFAULT '0',  -- 0: normal, 1: inactive, 2: deleted
    pic VARCHAR(255),
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);




-- Categories Table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status CHAR(2) DEFAULT '0'  -- 0: active, 1: inactive
);

 -- Events Table
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    location VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    status CHAR(2) DEFAULT '0',  -- 0: active, 1: canceled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    author_id int,
    category_id INT,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
); 

-- Event Registrations Table
CREATE TABLE event_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    status CHAR(2) DEFAULT '0',  -- 0: registered, 1: canceled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Favorites Table
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
