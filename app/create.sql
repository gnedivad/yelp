drop table if exists Restaurants;
drop table if exists Categories;

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