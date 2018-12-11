drop table if exists StdSensorTypes;

create table StdSensorTypes (
 SensorCode text,
 SensorType text,
 SensorImage text
);

INSERT INTO StdSensorTypes (SensorCode, SensorType) VALUES ("s0", "Temperature and Humidity Sensor: DHT22");
INSERT INTO StdSensorTypes (SensorCode, SensorType) VALUES ("s1", "Pressure Sensor: BMP180");
INSERT INTO StdSensorTypes (SensorCode, SensorType) VALUES ("s2", "Light Sensor: LDR");
INSERT INTO StdSensorTypes (SensorCode, SensorType) VALUES ("s3", "Door-Windows Sensor");
