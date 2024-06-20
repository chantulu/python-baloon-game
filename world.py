import random
import tkinter as tk


class GameObject:
    def __init__(self, x: int, y: int, c) -> None:
        self.canvas = c
        self.x = x
        self.y = y
        self.velocity = (0, 0)
        self.applied_force = [0, 0]
        self.moving = False

    def move_x(self, speed):
        self.x += speed
        return self.x

    def move_y(self, speed):
        self.y += speed
        return self.y

    def apply_force_x(self, force):
        self.applied_force[0] += force
        self.moving = True

    def apply_force_y(self, force):
        self.applied_force[1] += force
        self.moving = True

    def update_velocity(self, x=None, y=None):
        self.velocity = (
            x if x is not None else self.velocity[0],
            y if y is not None else self.velocity[1],
        )

    def move(self):
        return

    def clean(self):
        self.canvas.delete(self.dot_shape)


class Arrow(GameObject):
    def __init__(self, x: int, y: int, c) -> None:
        super().__init__(x, y, c)
        self.radius = 5
        self.dot_shape = self.canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill="black",
        )

    def move(self):
        if self.moving == False:
            return
        self.canvas.move(
            self.dot_shape,
            self.velocity[0] + self.applied_force[0],
            self.velocity[1] + self.applied_force[1],
        )
        self.move_x(self.velocity[0] + self.applied_force[0])
        self.move_y(self.velocity[1] + self.applied_force[1])
        if self.applied_force[0] > 0:
            self.applied_force[0] -= 0.5
        if self.applied_force[1] > 0:
            self.applied_force[1] -= 2
        elif self.applied_force[1] < 0:
            self.applied_force[1] += 5
        self.velocity = (
            self.velocity[0] + self.applied_force[0],
            self.velocity[1] + self.applied_force[1] + 3.5,
        )


class Baloon(GameObject):
    def __init__(self, x: int, y: int, c) -> None:
        super().__init__(x, y, c)
        self.radius = 50
        self.dot_shape = self.canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill="red",
        )
        self.moving = True

    def move(self):
        self.canvas.move(
            self.dot_shape,
            self.velocity[0] + self.applied_force[0],
            self.velocity[1] - 2,
        )
        self.move_x(self.velocity[0] + self.applied_force[0])
        self.move_y(self.velocity[1] - 2)
        self.velocity = (
            self.velocity[0] + self.applied_force[0],
            self.velocity[1] + self.applied_force[1] - 0.1,
        )


class World:
    def __init__(self):
        self.running = False
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.canvas.grid()
        self.physics_started = False
        self.__start = (80, 200)
        self.arrows = [Arrow(self.__start[0], self.__start[1], self.canvas)]
        self.baloons = []
        self.baloons_popped = 0
        self.baloons_popped_var = tk.StringVar()

        self.baloons_popped_var.set("0 Baloons popped")

        tk.Button(
            self.window, text="Pause / Resume Game", bg="yellow", command=self.stop_it
        ).grid(row=2, column=0)
        tk.Button(self.window, text="Exit", bg="orange", command=self.window.quit).grid(
            row=4, column=0
        )
        tk.Button(
            self.window, text="Shoot Arrow", bg="yellow", command=self.apply_force
        ).grid(row=3, column=0)

        tk.Label(self.window, textvariable=self.baloons_popped_var).grid(
            row=1, column=0
        )
        self.window.after(25, self.start_physics)

        self.window.mainloop()

    def start_physics(self):
        if self.running:
            self.physics_started = True
            if random.random() < 0.1:
                x = random.randint(200, 800)
                y = 800
                self.baloons.append(Baloon(x, y, self.canvas))
            for baloon in self.baloons:
                baloon.move()
                if baloon.x > 800 or baloon.y > 800:
                    baloon.clean()  # this is no longer visible
            for arrow in self.arrows:
                arrow.move()
                if arrow.x > 800 or arrow.y > 800:
                    arrow.clean()  # this arrow is no longer visible
            self.arrows = list(filter(lambda a: a.x < 800 and a.y < 800, self.arrows))
            self.baloons = list(filter(lambda b: b.x < 800 and b.y < 800, self.baloons))
            if not any(arrow.moving == False for arrow in self.arrows):
                # no idle arrows, create one
                self.arrows.append(Arrow(self.__start[0], self.__start[1], self.canvas))

            self.check_colissions()
            ## check for ball hitting edges & change direction
            self.window.after(40, self.start_physics)

    def check_colissions(self):
        collided_baloons = []
        for arrow in self.arrows:
            for index, baloon in enumerate(self.baloons):
                dx = arrow.x - baloon.x
                dy = arrow.y - baloon.y
                distance = (dx**2 + dy**2) ** 0.5
                if distance < (arrow.radius + baloon.radius):
                    collided_baloons.append(index)
                    self.baloons_popped += 1
                    self.baloons_popped_var.set(f"{self.baloons_popped} Baloons popped")
        for collided_baloon in [
            baloon
            for index, baloon in enumerate(self.baloons)
            if index in collided_baloons
        ]:
            collided_baloon.clean()
        self.baloons = [
            baloon
            for index, baloon in enumerate(self.baloons)
            if index not in collided_baloons
        ]

    def stop_it(self):
        self.running = not self.running
        if self.running:
            self.start_physics()

    def apply_force(self):
        if self.physics_started != True:
            self.running = True
            self.start_physics()
        for arrow in self.arrows:
            if arrow.moving == False:
                arrow.apply_force_x(random.randint(3, 8))
                arrow.apply_force_y(0 - random.randint(13, 25))


if __name__ == "__main__":
    World()
