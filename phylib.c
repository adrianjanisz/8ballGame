#include "phylib.h"

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
    phylib_object *newStillBall = (phylib_object *)malloc(sizeof(phylib_object));

    if (newStillBall == NULL) {
        return NULL;
    }

    // Assign information 
    newStillBall->type = PHYLIB_STILL_BALL;
    
    newStillBall->obj.still_ball.number = number;
    newStillBall->obj.still_ball.pos = *pos;

    return newStillBall;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {
    phylib_object *newRollingBall = (phylib_object *)malloc(sizeof(phylib_object));

    if (newRollingBall == NULL) {
        return NULL;
    }

    // Assign information 
    newRollingBall->type = PHYLIB_ROLLING_BALL;

    newRollingBall->obj.rolling_ball.number = number;
    newRollingBall->obj.rolling_ball.pos = *pos;
    newRollingBall->obj.rolling_ball.vel = *vel;
    newRollingBall->obj.rolling_ball.acc = *acc;

    return newRollingBall;
}

phylib_object *phylib_new_hole(phylib_coord *pos) {
    phylib_object *newHole = (phylib_object *)malloc(sizeof(phylib_object));

    if (newHole == NULL) {
        return NULL;
    }

    // Assign information 
    newHole->type = PHYLIB_HOLE;

    newHole->obj.hole.pos = *pos;

    return newHole;
}

phylib_object *phylib_new_hcushion(double y) {
    phylib_object *newHCushion = (phylib_object *)malloc(sizeof(phylib_object));

    if (newHCushion == NULL) {
        return NULL;
    }

    // Assign information 
    newHCushion->type = PHYLIB_HCUSHION;

    newHCushion->obj.hcushion.y = y;

    return newHCushion;
}

phylib_object *phylib_new_vcushion(double x) {
    phylib_object *newVCushion = (phylib_object *)malloc(sizeof(phylib_object));

    if (newVCushion == NULL) {
        return NULL;
    }

    // Assign information 
    newVCushion->type = PHYLIB_VCUSHION;

    newVCushion->obj.vcushion.x = x;
    
    return newVCushion;
}

phylib_table *phylib_new_table(void) {
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

    if (newTable == NULL) {
        return NULL;
    }

    // Initial time 
    newTable->time = 0.0;

    // Cushions 
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Holes 
    phylib_coord position;
    // Top left
    position.x = 0.0;
    position.y = 0.0;
    newTable->object[4] = phylib_new_hole(&position);
    // Middle left 
    position.x = 0.0;
    position.y = PHYLIB_TABLE_LENGTH/2;
    newTable->object[5] = phylib_new_hole(&position);
    // Bottom left 
    position.x = 0.0;
    position.y = PHYLIB_TABLE_LENGTH;
    newTable->object[6] = phylib_new_hole(&position);
    // Top right 
    position.x = PHYLIB_TABLE_WIDTH;
    position.y = 0.0;
    newTable->object[7] = phylib_new_hole(&position);
    // Middle right 
    position.x = PHYLIB_TABLE_WIDTH;
    position.y = PHYLIB_TABLE_LENGTH/2;
    newTable->object[8] = phylib_new_hole(&position);
    // Bottom right 
    position.x = PHYLIB_TABLE_WIDTH;
    position.y = PHYLIB_TABLE_LENGTH;
    newTable->object[9] = phylib_new_hole(&position);

    // Rest are NULL 
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        newTable->object[i] = NULL;
    }

    return newTable;
}

void phylib_copy_object(phylib_object **dest, phylib_object **src) {
    if (*src == NULL) { 
        *dest = NULL;
        return;
    }
    
    // Create new object 
    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    memcpy(*dest, *src, sizeof(phylib_object));
}

phylib_table *phylib_copy_table(phylib_table *table) {
    phylib_table *copyTable = (phylib_table *)malloc(sizeof(phylib_table));

    if (copyTable == NULL) {
        return NULL;
    }

    memcpy(copyTable, table, sizeof(phylib_table));

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        copyTable->object[i] = NULL;
    }

    // Time 
    copyTable->time = table->time;

    // Copy loop 
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (checkIfNotNULL(table->object[i])) {
            copyTable->object[i] = (phylib_object *)malloc(sizeof(phylib_object));
            memcpy(copyTable->object[i], table->object[i], sizeof(phylib_object));
        }
    }
    
    return copyTable;
}

void phylib_add_object(phylib_table *table, phylib_object *object) {
    
    // Loop that searches for NULL index 
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            return;
        }
    }
}

void phylib_free_table(phylib_table *table) {

    // Loop that frees array of objects 
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (checkIfNotNULL(table->object[i])) {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }

    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord difference;

    // X and Y difference 
    difference.x = c1.x - c2.x;
    difference.y = c1.y - c2.y;

    return difference;
}

double phylib_length(phylib_coord c) {
    double lengthSquared;
    double length;

    // Pythagorean theorem 
    lengthSquared = (c.x * c.x) + (c.y * c.y);
    
    length = sqrt(lengthSquared);

    return length;
}

double phylib_dot_product(phylib_coord a, phylib_coord b) {
    double dotProduct;

    // Dot-product 
    dotProduct = a.x * b.x + a.y * b.y;

    return dotProduct;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    double distance;
    
    if (obj1->type != 1) {
        return -1.0;
    }

    phylib_coord obj1Pos = obj1->obj.rolling_ball.pos;
    phylib_coord obj2Pos;

    // obj2 is a still ball 
    if (obj2->type == PHYLIB_STILL_BALL) {
        obj2Pos = obj2->obj.still_ball.pos;
        distance = phylib_length(phylib_sub(obj1Pos, obj2Pos)) - PHYLIB_BALL_DIAMETER;
    }
    // obj2 is a rolling ball 
    else if (obj2->type == PHYLIB_ROLLING_BALL) {
        obj2Pos = obj2->obj.rolling_ball.pos;
        distance = phylib_length(phylib_sub(obj1Pos, obj2Pos)) - PHYLIB_BALL_DIAMETER;
    }
    // obj2 is a hole 
    else if (obj2->type == PHYLIB_HOLE) {
        obj2Pos = obj2->obj.hole.pos;
        distance = phylib_length(phylib_sub(obj1Pos, obj2Pos)) - PHYLIB_HOLE_RADIUS;
    }
    // obj2 is a horizontal cushion 
    else if (obj2->type == PHYLIB_HCUSHION) {
        obj2Pos.y = obj2->obj.hcushion.y;
        distance = fabs(obj1Pos.y - obj2Pos.y) - PHYLIB_BALL_RADIUS;
    }
    // obj2 is a vertical cushion 
    else if (obj2->type == PHYLIB_VCUSHION) {
        obj2Pos.x = obj2->obj.vcushion.x;
        distance = fabs(obj1Pos.x - obj2Pos.x) - PHYLIB_BALL_RADIUS;
    }
    // obj2 is not a valid type 
    else {  
        return -1.0;
    }

    return distance;
}

void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    // Check if new and old are rolling balls 
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    // X 
    double oldPosX = old->obj.rolling_ball.pos.x;
    double oldVelX = old->obj.rolling_ball.vel.x;
    double oldAccX = old->obj.rolling_ball.acc.x;

    // Y 
    double oldPosY = old->obj.rolling_ball.pos.y;
    double oldVelY = old->obj.rolling_ball.vel.y;
    double oldAccY = old->obj.rolling_ball.acc.y;

    // Updated X and Y pos 
    new->obj.rolling_ball.pos.x = oldPosX + (oldVelX * time) + (0.5) * (oldAccX) * (time * time);
    new->obj.rolling_ball.pos.y = oldPosY + (oldVelY * time) + (0.5) * (oldAccY) * (time * time);

    // Updated X and Y vel 
    new->obj.rolling_ball.vel.x = oldVelX + (oldAccX * time);
    new->obj.rolling_ball.vel.y = oldVelY + (oldAccY * time);

    // Check if vel changed signs 
    // X: New vel > 0, old vel < 0 
    if (new->obj.rolling_ball.vel.x > 0.0 && oldVelX < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    // X: New vel < 0, old vel > 0 
    if (new->obj.rolling_ball.vel.x < 0.0 && oldVelX > 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    // Y: New vel > 0, old vel < 0 
    if (new->obj.rolling_ball.vel.y > 0.0 && oldVelY < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
    // Y: New vel < 0, old vel > 0 
    if (new->obj.rolling_ball.vel.y < 0.0 && oldVelY > 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }

}

unsigned char phylib_stopped(phylib_object *object) {
    // Calculate object speed 
    double objectSpeed = phylib_length(object->obj.rolling_ball.vel);

    // Compare object speed 
    if (objectSpeed < PHYLIB_VEL_EPSILON) {
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
        return 1;
    } 
    
    // If ball speed is greater than or equal to 0.01 mm/s
    return 0;
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
    // Switch statement for types of b 
    switch((*b)->type) {
        case PHYLIB_HCUSHION: 
            (*a)->obj.rolling_ball.vel.y = ((*a)->obj.rolling_ball.vel.y) * -1;
            (*a)->obj.rolling_ball.acc.y = ((*a)->obj.rolling_ball.acc.y) * -1;
            break;

        case PHYLIB_VCUSHION: 
            (*a)->obj.rolling_ball.vel.x = ((*a)->obj.rolling_ball.vel.x) * -1;
            (*a)->obj.rolling_ball.acc.x = ((*a)->obj.rolling_ball.acc.x) * -1;
            break;

        case PHYLIB_HOLE: 
            free(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL: 
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

        case PHYLIB_ROLLING_BALL: {
            // Position (a - b) 
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            
            // Velocity (a - b) 
            phylib_coord v_rel;

            v_rel.x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
            v_rel.y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;

            // Normal vector 
            double r_abLength = phylib_length(r_ab);
            phylib_coord n;

            n.x = r_ab.x / r_abLength;
            n.y = r_ab.y / r_abLength;

            // Ratio of relative velocity 
            double v_rel_n = phylib_dot_product(v_rel, n);

            // Updating velocity of a 
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

            // Updating velocity of b 
            (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * n.x);
            (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * n.y);

            // Computing speeds of a and b as the lengths of their velocities 
            double speedOfA = phylib_length((*a)->obj.rolling_ball.vel);
            double speedOfB = phylib_length((*b)->obj.rolling_ball.vel);

            if (speedOfA > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / speedOfA * PHYLIB_DRAG);
                (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / speedOfA * PHYLIB_DRAG);
            }

            if (speedOfB > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x / speedOfB * PHYLIB_DRAG);
                (*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y / speedOfB * PHYLIB_DRAG);
            }

            break;
        }
    }
    
}

unsigned char phylib_rolling(phylib_table *t) {
    unsigned char rollingBallCounter = 0; 

    // Checker every item in object array if it is a rolling ball 
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (checkIfNotNULL(t->object[i]) && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            rollingBallCounter += 1;
        }
    }
    
    return rollingBallCounter;
}

phylib_table *phylib_segment(phylib_table *table) {
    // No rolling balls 
    if (phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table *copyOfTable = phylib_copy_table(table);
    if (copyOfTable == NULL) {
        return NULL;
    }
    
    double elapsedTime = copyOfTable->time;

    for (double simulationTime = PHYLIB_SIM_RATE; simulationTime <= PHYLIB_MAX_TIME; simulationTime += PHYLIB_SIM_RATE) {
        // Update table time 
        copyOfTable->time = elapsedTime + simulationTime;
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            // Simulate every rolling ball 
            if (checkIfNotNULL(copyOfTable->object[i]) && copyOfTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(copyOfTable->object[i], table->object[i], simulationTime);

                // Check if ball stopped 
                if (phylib_stopped(copyOfTable->object[i]) == 1) {
                    copyOfTable->object[i]->type = PHYLIB_STILL_BALL;
                    return copyOfTable;
                }
            }
        }
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (checkIfNotNULL(copyOfTable->object[i]) && copyOfTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (i != j && checkIfNotNULL(copyOfTable->object[j])) {
                        double distance = phylib_distance(copyOfTable->object[i], copyOfTable->object[j]);
                        // Return an updated table if a bounce occurs 
                        if (distance < 0.0) {
                            phylib_bounce(&copyOfTable->object[i], &copyOfTable->object[j]);
                            return copyOfTable;
                        }
                    }
                }
            }
        }
    }

    return copyOfTable;
}

char *phylib_object_string(phylib_object *object) {
    static char string[80];
    if (object == NULL) {
        snprintf(string, 80, "NULL");
        return string;
    }

    switch (object->type) {
        case PHYLIB_STILL_BALL:
            snprintf(string, 80, "STILL_BALL (%d,%6.1lf, %6.1lf)", 
                object->obj.still_ball.number, 
                object->obj.still_ball.pos.x, 
                object->obj.still_ball.pos.y);
            break;

        case PHYLIB_ROLLING_BALL:
            snprintf(string, 80, "ROLLING_BALL (%d, %6.1lf, %6.1lf, %6.1lf, %6.1lf, %6.1lf, %6.1lf)", 
                object->obj.rolling_ball.number, 
                object->obj.rolling_ball.pos.x, 
                object->obj.rolling_ball.pos.y, 
                object->obj.rolling_ball.vel.x, 
                object->obj.rolling_ball.vel.y, 
                object->obj.rolling_ball.acc.x, 
                object->obj.rolling_ball.acc.y);
            break;
        
        case PHYLIB_HOLE:
            snprintf(string, 80, "HOLE (%6.1lf,%6.1lf)", 
                object->obj.hole.pos.x, 
                object->obj.hole.pos.y);
            break;

        case PHYLIB_HCUSHION:
            snprintf(string, 80, "HCUSHION (%6.1lf)", 
                object->obj.hcushion.y);
            break;

        case PHYLIB_VCUSHION:
            snprintf(string, 80, "VCUSHION (%6.1lf)", 
                object->obj.vcushion.x);
            break;
    }
    return string;
}

// Checks if phylib_object != NULL 
int checkIfNotNULL(phylib_object *input) {
    if (input != NULL) {
        return 1;
    }
    
    return 0;
}
