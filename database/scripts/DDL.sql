create table if not exists users (
    id int primary key auto_increment,
    username varchar(25) not null unique,
    email varchar(250) not null unique,
    password varchar(90) not null
);


create table if not exists profiles (
    id int primary key auto_increment,
    id_user int not null,
    name varchar(250) not null,
    birth date not null,
    weight decimal(5, 2),
    height decimal(3, 2),
    foreign key (id_user)
        references profiles(id)
        on delete cascade
        on update cascade
);


create table if not exists weighing (
    id_profile int not null,
    weight decimal(5, 2),
    created date not null default (curdate()),
    foreign key (id_profile)
        references profiles(id)
        on delete cascade
        on update cascade
);

delimiter $$
create trigger insert_weighing
    after insert on profiles
    for each row
    begin
        insert into weighing (id_profile, weight)
            values (new.id, new.weight);
    end ;
$$ delimiter ;

delimiter $$
create trigger set_weighing
    after update on profiles
    for each row
    begin
        insert into weighing (id_profile, weight)
            values (new.id, new.weight);
    end ;
$$ delimiter ;

delimiter $$
create procedure create_profile(
    _username varchar(25),
    _email varchar(250),
    _password varchar(90),
    _name varchar(250),
    _birth date,
    _weight decimal(5, 2),
    _height decimal(3,2)
) begin
    insert into users (username, email, password)
        values (_username, _email, _password);
    insert into profiles (id_user, name, birth, weight, height)
        values (last_insert_id(), _name, _birth, _weight, _height);
end;
$$ delimiter ;

