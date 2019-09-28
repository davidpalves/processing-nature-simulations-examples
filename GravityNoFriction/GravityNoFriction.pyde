class Mover(object):
    def __init__(self, m, x, y):
        self.position = PVector(x, y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.mass = m
    
    def applyForce(self, force):
        f = PVector.div(force, self.mass)
        self.acceleration.add(f)
    
    def update(self):
        self.velocity.add(self.acceleration)
        self.position.add(self.velocity)
        self.acceleration.mult(0)
    
    def display(self):
        stroke(0)
        strokeWeight(2)
        fill(0, 127)
        ellipse(self.position.x, self.position.y, self.mass*16, self.mass*16)
    
    def checkEdges(self):
        if (self.position.x > width):
            self.position.x = width
            self.velocity.x *= -1
        elif (self.position.x < 0):
            self.position.x = 0
            self.velocity.x *= -1

        if (self.position.y > height):
            self.position.y = height
            self.velocity.y *= -1
            
def setup():
    size(383, 200)
    randomSeed(1)

    global movers
    movers = [Mover(random(1, 4), random(width), 0) for i in range(5)]

def draw():
    background(255)

    for m in movers:

        wind = PVector(0.01, 0)
        gravity = PVector(0, 0.1*m.mass)

        c = 0.05
        friction = m.velocity.get()
        friction.mult(-1)
        friction.normalize()
        friction.mult(c)

        # m.applyForce(friction)
        m.applyForce(wind)
        m.applyForce(gravity)

        m.update()
        m.display()
        m.checkEdges()
