class Mover(object):
    def __init__(self, m, x, y):
        self.position = PVector(x, y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.mass = m
        
    def applyForce(self, force):
        # Newton's Second Law: F = M * A
        # or A = F / M

        # divide by mass
        f = PVector.div(force, self.mass)

        # accumulate all forces in a acceleration
        self.acceleration.add(f)
    
    def update(self):
        self.velocity.add(self.acceleration)
        self.position.add(self.velocity)
        self.acceleration.mult(0)
    
    def display(self):
        stroke(0)
        strokeWeight(2)
        fill(127, 200)
        ellipse(self.position.x, self.position.y, self.mass*16, self.mass*16)
    
    def checkEdges(self):
        # Bounce off the bottom of the window.
        if (self.position.y > height):
            self.position.y = height

            # A little dampening when hitting the bottom
            self.velocity.y *= -0.9


class Liquid(object):
    def __init__(self, x, y, w,  h, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c

    def contains(self, m):
        l = m.position
        return (l.x > self.x) and (l.x < (self.x + self.w)) and \
                (l.y > self.y) and (l.y < (self.y + self.h))

    def drag(self, m):
        """
        Calculates the drag force
        """
        speed = m.velocity.mag()
        dragMagnitude = self.c * speed * speed

        dragForce = m.velocity.get()
        dragForce.mult(-1)

        # dragForce.setMag(dragMagnitude)
        dragForce.normalize()
        dragForce.mult(dragMagnitude)
        return dragForce

    def display(self):
        noStroke()
        fill(50)
        rect(self.x, self.y, self.w, self.h)
        
        
def setup():
    size(640, 360)
    reset()

    global liquid
    liquid = Liquid(0, height/2, width, height/2, 0.1)

def draw():
    background(255)

    liquid.display()

    for mover in movers:

        # Is the Mover in the liquid?
        if liquid.contains(mover):
            # Calculate the drag force
            dragForce = liquid.drag(mover)
            # Apply the drag force
            mover.applyForce(dragForce)

        # Gravity is scaled by mass here!
        gravity = PVector(0, 0.1*mover.mass)
        # Apply gravity
        mover.applyForce(gravity)

        # update and display
        mover.update()
        mover.display()
        mover.checkEdges()

    fill(0)
    text("click mouse to reset", 10, 30)

def mousePressed():
    reset()

def reset():
    # restart all movers randomly
    global movers
    movers = [Mover(random(0.5, 3), 40 + i*70, 0) for i in range(9)]
