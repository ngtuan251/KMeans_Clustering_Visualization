import pygame
from random import randint
import math
from sklearn.cluster import KMeans

#Define a function to calculate distance
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption('K-Means Visualization')

running = True

clock = pygame.time.Clock()

background = (214,214,214)
black = (0,0,0)
background_panel = (249, 255, 230)
white = (255,255,255)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (147,153,35)
purple = (255,0,255)
sky = (0,255,255)
orange = (255,125,25)
grape = (100,25,125)
grass = (55,155,65)

colors = [red, green, blue, yellow, purple, sky, orange, grape, grass]

font = pygame.font.SysFont('sans', 40)
small_font = pygame.font.SysFont('sans', 16)
text_plus = font.render('+', True, white)
text_minus = font.render('-', True, white)
text_run = font.render('Run', True, white)
text_random = font.render('Random', True, white)
text_algorithm = font.render('Algorithm', True, white)
text_reset = font.render('Reset', True, white)

K = 0
points = []
clusters = []
labels = []

while running:
    clock.tick(60) #Frames per second
    screen.fill(background)
    mouse_x, mouse_y =  pygame.mouse.get_pos()
    #Draw interface

    #Draw background_panel
    pygame.draw.rect(screen, black, (45,45,700,500))
    pygame.draw.rect(screen, background_panel, (50,50,690,490))
    
    #Draw button +
    pygame.draw.rect(screen, black, (850,50,50,50))
    screen.blit(text_plus, (865,50))
    
    #Draw button -
    pygame.draw.rect(screen, black, (950,50,50,50))
    screen.blit(text_minus, (970,48))
    
    #Draw K button 
    text_K = font.render('K = ' + str(K), True, black)
    screen.blit(text_K, (1050,50))
    
    #Draw button RUN
    pygame.draw.rect(screen, black, (850,150,150,50))
    screen.blit(text_run, (895,150))
    
    #Draw button RANDOM
    pygame.draw.rect(screen, black, (850,250,150,50))
    screen.blit(text_random, (865,250))
    
    #Draw button ALGORITHM
    pygame.draw.rect(screen, black, (850,450,150,50))
    screen.blit(text_algorithm, (855,450))
    
    #Draw button RESET
    pygame.draw.rect(screen, black, (850,550,150,50))
    screen.blit(text_reset, (880,550))
    
    #Draw mouse position when mouse is in the interface 
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:    
        text_mouse = small_font.render('(' + str(mouse_x-50) + ',' + str(mouse_y-50) + ')' , True, black)
        screen.blit(text_mouse, (mouse_x+10, mouse_y))

  
    #End draw interface   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            #Create points on panel
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x - 50, mouse_y - 50]
                points.append(point)
            
            #Change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if K < 9:
                    K += 1
                print('Press +')

            #Change K button -    
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if K > 0:
                    K -= 1
                print('Press K button -')
            

            #Press run    
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                labels = []
                if clusters == []:
                    continue
                #Assign points to closest clusters
                for point in points:
                    distances_to_cluster = []
                    for cluster in clusters:
                        dis = distance(point, cluster)
                        distances_to_cluster.append(dis)
                    min_dis = min(distances_to_cluster)
                    labels.append(distances_to_cluster.index(min_dis))
                
                #Update cluster    
                for k in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == k:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    if count != 0:
                        new_cluster_x = sum_x/count
                        new_cluster_y = sum_y/count
                        clusters[k] = [new_cluster_x, new_cluster_y]
                print('Press run')
            
            #Press random    
            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                clusters = []
                labels = []
                for i in range(K):
                    random_point = [randint(5,695), randint(5,495)]
                    clusters.append(random_point)
                print('Press random')
                
            #Press algorithm        
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                kmeans = KMeans(n_clusters=K).fit(points)
                labels = kmeans.predict(points)
                clusters = kmeans.cluster_centers_
                print('Press algorithm')
                
            #Press reset        
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                K = 0 
                error = 0
                points = []
                clusters = []
                labels = []
                print('Press reset')
        
    #Draw points in panel
    for i in range(len(points)):
        pygame.draw.circle(screen, black, (points[i][0]+50, points[i][1]+50), 5)
        if labels == []:
            pygame.draw.circle(screen, white, (points[i][0]+50, points[i][1]+50), 4)
        else:
            pygame.draw.circle(screen, colors[labels[i]], (points[i][0]+50, points[i][1]+50), 4)
    
    #Draw random points (clusters) in panel
    for i in range(len(clusters)):
        pygame.draw.circle(screen, colors[i], (int(clusters[i][0])+50, int(clusters[i][1])+50), 8)
     
    #Calculate error and draw error button
    error = 0
    if clusters != [] and labels != []:    
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])
    text_error = font.render('Error = ' + str(int(error)), True, black)
    screen.blit(text_error, (860, 350))
    pygame.display.flip()

pygame.quit()
        
        
    