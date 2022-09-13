USER = """CREATE TABLE USER (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    createDate datetime default CURRENT_TIMESTAMP
)"""


VIDEO = """CREATE TABLE VIDEO (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    videoUrl VARCHAR(2500) NOT NULL,
    userId INT NOT NULL,
    createDate datetime default CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES USER(id)
)"""


LIKE = """CREATE TABLE LIKES (
    videoId INT NOT NULL,
    userId INT NOT NULL,
    createDate datetime default CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES USER(id),
    FOREIGN KEY (videoId) REFERENCES VIDEO(id),
    PRIMARY KEY (videoId, userId)
)"""
