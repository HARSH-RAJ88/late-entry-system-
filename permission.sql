use Late_entry_system;
drop table permission;
create table permission
(
    permissionID int auto_increment primary key,
    rollNumber   int,
    date         DATE NOT NULL,
    time         TIME NOT NULL,
    status       BOOLEAN DEFAULT NULL,
    w_id         INT     DEFAULT NULL,
    FOREIGN KEY (rollNumber) REFERENCES student (roll_no),
    FOREIGN KEY (w_id) REFERENCES warden (w_id)

);