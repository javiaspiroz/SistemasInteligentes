-- todas la peliculas
select movie.movieId from movie

-- todas las opiniones de un usuario
SELECT * FROM rating
WHERE rating.userId = 1

-- agrupar los todos los usuarios
SELECT userId 
FROM rating 
GROUP BY userId;

-- peliculas sin ninguna opinion
select movie.movieId from movie
EXCEPT
select rating.movieId from rating
GROUP  by movieId

-- peliculas que no ha valorado un usuario
select movieId from rating
WHERE rating.userId <> 1
EXCEPT
SELECT movieId FROM rating
WHERE rating.userId = 1

-- valoraciones de peliculas dadas dos
 SELECT userId, rating, movieId FROM rating WHERE movieId=1 AND userId IN (SELECT userId FROM rating WHERE movieId=3);

-- usuario con menor número de valoraciones que haya valorado 2 pelis
SELECT count(movieId), userId FROM rating WHERE userId IN (SELECT userId FROM rating WHERE movieId=1 AND userId IN (SELECT userId FROM rating WHERE movieId=3))
GROUP by userId
order by count(movieId) ASC
limit 1

-- dadas dos películas y n usuarios que la han visto, peliculas que han visto todos ellos
SELECT movieId FROM rating WHERE userId = 544 and userId IN (SELECT userId FROM rating WHERE movieId=1 AND userId IN (SELECT userId FROM rating WHERE movieId=3))
INTERSECT
SELECT movieId FROM rating WHERE userId = 1 and userId IN (SELECT userId FROM rating WHERE movieId=1 AND userId IN (SELECT userId FROM rating WHERE movieId=3))
INTERSECT
SELECT movieId FROM rating WHERE userId = 19 and userId IN (SELECT userId FROM rating WHERE movieId=1 AND userId IN (SELECT userId FROM rating WHERE movieId=3))
INTERSECT
SELECT movieId FROM rating WHERE userId = 32 and userId IN (SELECT userId FROM rating WHERE movieId=1 AND userId IN (SELECT userId FROM rating WHERE movieId=3))

-- dadas dos peliculas y un usuario, calcular la media de las valoraciones
SELECT avg(rating) from rating WHERE (movieId = 3 or movieId = 1) and userId =1

-- usuarios con menos peliculas valoradas
select count(rating), userId from rating
GROUP by userId
order by count(rating) asc