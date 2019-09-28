class Sun(object):

    def __init__(self):
        self.location = PVector(0, 0)
        # Mass, tied to size
        self.mass = 20
        # Universal gravitational constant (arbitrary value).
        self.G = 0.4

    def attract(self, m):
        # Calculate direction of force.
        force = PVector.sub(self.location, m.location)
        d = force.mag()  # Distance between objects
        # Limiting the distance to eliminate "extreme" results for very close
        # or very far objects.
        d = constrain(d, 5.0, 25.0)
        # Calculate gravitional force magnitude.
        strength = (self.G * self.mass * m.mass) / (d * d)
        force.setMag(strength)  # Get force vector --> magnitude * direction
        return force

    # Draw Sun.
    def display(self):
        stroke(255)
        fill(255)
        with pushMatrix():
            translate(self.location.x, self.location.y, self.location.z)
            sphere(self.mass * 2)


class Planet(object):

    # Basic physics model (location, velocity, acceleration, mass)
    def __init__(self, m, x, y, z):
        self.mass = m
        self.location = PVector(x, y, z)
        self.velocity = PVector(1, 0)  # Arbitrary starting velocity
        self.acceleration = PVector(0, 0)

    # Newton's 2nd Law (F = M*A) applied
    def applyForce(self, force):
        f = PVector.div(force, self.mass)
        self.acceleration.add(f)

    # Our motion algorithm (aka Euler Integration)
    def update(self):
        # Velocity changes according to acceleration.
        self.velocity.add(self.acceleration)
        self.location.add(self.velocity)  # Location changes according to velocity.
        self.acceleration.mult(0)

    # Draw the Planet.
    def display(self):
        noStroke()
        fill(255)
        with pushMatrix():
            translate(self.location.x, self.location.y, self.location.z)
            sphere(self.mass * 8)


# A bunch of planets.
planets = [None] * 10
# One sun (note sun is not attracted to planets (violation of Newton's 3rd
# Law).
s = None
# An angle to rotate around the scene.
angle = 0


def setup():
    global planets, s
    size(640, 360, P3D)
    smooth()
    # Some random planets.
    for i in range(len(planets)):
        planets[i] = Planet(random(0.1, 2), random(-width / 2, width / 2),
                            random(-height / 2, height / 2), random(-100, 100))
    # A single sun.
    s = Sun()


def draw():
    global angle
    background(0)
    # Setup the scene.
    sphereDetail(8)
    lights()
    translate(width / 2, height / 2)
    rotateY(angle)
    # Display the Sun.
    s.display()
    # All the Planets
    for planet in planets:
        # Sun attracts Planets.
        force = s.attract(planet)
        planet.applyForce(force)
        # Update and draw Planets.
        planet.update()
        planet.display()
    # Rotate around the scene.
    angle += 0.003
