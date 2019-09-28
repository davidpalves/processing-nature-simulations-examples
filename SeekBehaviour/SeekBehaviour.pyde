class Vehicle():

    def __init__(self, x, y):
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(0, -2)
        self.position = PVector(x, y)
        self.r = 6
        self.maxspeed = 8
        self.maxforce = 0.2

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.maxspeed)
        self.position.add(self.velocity)
        self.acceleration.mult(0)

    def applyForce(self, force):
        self.acceleration.add(force)

    def seek(self, target):

        # A vector pointing from the location to the target
        desired = target - self.position

        # Scale to maximum speed
        desired.setMag(self.maxspeed)

        steer = desired - self.velocity
        steer.limit(self.maxforce)  # Limit to maximum steering force

        self.applyForce(steer)

    def display(self):
        # Draw a triangle rotated in the direction of velocity
        theta = self.velocity.heading() + PI / 2
        fill(127)
        stroke(200)
        strokeWeight(1)
        with pushMatrix():
            translate(self.position.x, self.position.y)
            rotate(theta)
            beginShape()
            vertex(0, -self.r * 2)
            vertex(-self.r, self.r * 2)
            vertex(self.r, self.r * 2)
            endShape(CLOSE)
            

def setup():
    global v
    size(860, 640)
    v = Vehicle(width / 2, height / 2)


def draw():
    background(251)

    mouse = PVector(mouseX, mouseY)

    # Draw an ellipse at the mouse position
    fill(127)
    stroke(200)
    strokeWeight(2)
    ellipse(mouse.x, mouse.y, 48, 48)

    # Call the appropriate steering behaviors for our agents
    v.seek(mouse)
    v.update()
    v.display()
