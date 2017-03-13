drop table if exists Restaurants;
drop table if exists Categories;
drop table if exists Reviews;

create table Restaurants(
	RestaurantID VARCHAR PRIMARY KEY,
	Name VARCHAR,
	City VARCHAR,
	Latitude FLOAT,
	Longitude FLOAT,
	Price INTEGER,
	Rating FLOAT
);

create table Categories(
	RestaurantID VARCHAR NOT NULL,
	Category VARCHAR,
	PRIMARY KEY (RestaurantID, Category),
	FOREIGN KEY(RestaurantID) REFERENCES Restaurants(RestaurantID)
);

create table Reviews(
       ReviewID VARCHAR PRIMARY KEY,
       RestaurantID VARCHAR NOT NULL,
       Text VARCHAR,
       Rating INTEGER,
       FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID)
);
