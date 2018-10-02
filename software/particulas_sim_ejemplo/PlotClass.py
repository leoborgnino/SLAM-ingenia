from math import *
import matplotlib.pyplot as plt

def visualization(robot, step, p, pr, weights, world_size_x,world_size_y, obstacles):
    step = step + 1
    print step
    plt.figure("Mapa del Robot", figsize=(10., 10.))
    plt.title('Movimento del Robot ' + str(step))

    grid = [0, world_size_x, 0, world_size_y]
    plt.axis(grid)
    plt.grid(b=True, which='major', color='0.75', linestyle='--')
    plt.xticks([i for i in range(0, int(world_size_x), 5)])
    plt.yticks([i for i in range(0, int(world_size_y), 5)])

    for ind in range(len(p)):
        # Particula
        circle = plt.Circle((p[ind].x, p[ind].y), 1., facecolor='#e63900', edgecolor='#e63900', alpha=0.5)
        plt.gca().add_patch(circle)
        # Orientacion
        arrow = plt.Arrow(p[ind].x, p[ind].y, 2*cos(p[ind].orientation), 2*sin(p[ind].orientation), alpha=1., facecolor='#ff9900', edgecolor='#ff9900')
        plt.gca().add_patch(arrow)

    for ind in range(len(pr)):
        circle = plt.Circle((pr[ind].x, pr[ind].y), 1., facecolor='#0033cc', edgecolor='#0033cc', alpha=0.5)
        plt.gca().add_patch(circle)
        arrow = plt.Arrow(pr[ind].x, pr[ind].y, 2*cos(pr[ind].orientation), 2*sin(pr[ind].orientation), alpha=2., facecolor='#ffffff', edgecolor='#0033cc')
        plt.gca().add_patch(arrow)

    # Obtaculos
    for lm in obstacles:
        circle = plt.Circle((lm[0], lm[1]), 1., facecolor='#1a0500', edgecolor='#000000')
        plt.gca().add_patch(circle)

    # Robot
    circle = plt.Circle((robot.x, robot.y), 2., facecolor='#ccff33', edgecolor='#ffffff')
    plt.gca().add_patch(circle)

    # Orientacion Robot
    arrow = plt.Arrow(robot.x, robot.y, 2*cos(robot.orientation), 2*sin(robot.orientation), alpha=0.8, facecolor='#ffffff', edgecolor='#000000')
    plt.gca().add_patch(arrow)
    
    plt.savefig("output/" + str(step) + ".png")
plt.close() 
