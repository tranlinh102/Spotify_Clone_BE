-- Bảng Users: Lưu trữ thông tin người dùng, bao gồm cả người dùng thường và Admin.
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Artists: Lưu trữ thông tin về nghệ sĩ.
CREATE TABLE Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Songs: Lưu trữ thông tin bài hát hoặc podcast, hỗ trợ phát nhạc/podcast và video nếu có.
CREATE TABLE Songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    artist_id INT,
    duration INT NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    video_url VARCHAR(255),
    content_type ENUM('music', 'podcast') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- Bảng Albums: Cho phép người dùng tạo và quản lý album cá nhân.
CREATE TABLE Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES Users(user_id)
);

-- Bảng Album_Songs: Quản lý mối quan hệ nhiều-nhiều giữa album và bài hát/podcast.
CREATE TABLE Album_Songs (
    album_id INT,
    song_id INT,
    PRIMARY KEY (album_id, song_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Bảng Followers: Quản lý mối quan hệ nhiều-nhiều giữa người dùng và nghệ sĩ.
CREATE TABLE Followers (
    user_id INT,
    artist_id INT,
    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, artist_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- Bảng Favorites: Quản lý mối quan hệ nhiều-nhiều giữa người dùng và bài hát/podcast yêu thích.
CREATE TABLE Favorites (
    user_id INT,
    song_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Bảng Downloads: Quản lý mối quan hệ nhiều-nhiều giữa người dùng và bài hát/podcast được tải.
CREATE TABLE Downloads (
    user_id INT,
    song_id INT,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Bảng Messages: Hỗ trợ tích hợp tính năng chat trong giao diện web (tùy chọn).
CREATE TABLE Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    message_text TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);