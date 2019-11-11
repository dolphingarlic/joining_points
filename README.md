# Joining Points

“Joining points” is a single-player game. To play it, choose two integers greater than two and call
them g and r. Then draw four points at the vertices of a square making the top two points green and
the bottom two points red. Draw green points and red points inside the square taking care that no
three points, including the four initial ones, are in the same line. Continue until the total number of
green points equals g and the total number of red points equals r

After the board is drawn, start joining points. Any two points can be joined by a line segment as long
as:

- The two points to be joined are of the same color, and
- The line segment joining the points does not intersect any other previously drawn line
segment (other than at the endpoints)

Two points u and v are said to be in the same component if it is possible to traverse from point u to
point v using the line segments already drawn

You win the game if you get all the green points in one component using exactly g-1 line segments,
and all the red points in another component using exactly r-1 line segments. It can be proven that
if the points are drawn as described above, then there is always a way to win the game
