
#include <cmath>
#include <vector>
#include <iostream>
#include <SFML/Graphics.hpp>

float Gravity = 0.1f;

struct Particle {
    float posx, posy;
    float accelx, accely;
    float velox, veloy;
    float mass = 1.0f;
    float radius = 5.0F;

    std::vector<uint8_t> color;

    void UpdateParticlePos(float dt) {
        velox += accelx * dt;
        veloy += accely * dt;

        posx += velox;
        posy += veloy;
    }
    void UpdateParticleAcc() {
        accely = Gravity;
    }
    void CheckForWallCollision() {
        if (posx - radius < 0) {
            posx = radius;
            velox *= -0.99;
        } else if (posx + radius > 800) {
            posx = 800 - radius;
            velox *= -0.99;
        }

        if (posy - radius < 0) {
            posy = radius;
            veloy *= -0.99;
        } else if (posy + radius > 600) {
            posy = 600 - radius;
            veloy *= -0.99;
        }
    }
};

void ClearWindow(sf::RenderWindow& window) {
    window.clear(sf::Color::Black);
}

void DrawParticle(sf::RenderWindow& window, const Particle& p) {
    sf::CircleShape shape(p.radius);
    sf::Vector2f position(p.posx, p.posy);
    shape.setPosition(position);
    shape.setFillColor(sf::Color(p.color[0], p.color[1], p.color[2]));
    window.draw(shape);
}

int main() {
    std::cout << "Program started\n" << std::endl;
    sf::RenderWindow window(sf::VideoMode({800, 600}), "Particle Sim");

    std::vector<Particle> particles;
    
    // Initialize particles
    for (int i = 0; i < 25; i++) {
        Particle p;
        p.posx = 400;
        p.posy = 300;
        p.velox = (rand() % 200 - 100) / 10.0f; // Random velocity between -10 and 10
        p.veloy = (rand() % 200 - 100) / 10.0f; // Random velocity between -10 and 10
        p.color = {static_cast<uint8_t>(rand() % 256), static_cast<uint8_t>(rand() % 256), static_cast<uint8_t>(rand() % 256)}; particles.push_back(p);
    }

    while (window.isOpen()) {
        while (const std::optional event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>()) {
                window.close();
            }   
        }

        window.clear(sf::Color::Black);
        
        // Update and draw particles
        for (auto& p : particles) {
            p.UpdateParticleAcc();
            p.UpdateParticlePos(0.016f);
            p.CheckForWallCollision();
            DrawParticle(window, p);
        }
        
        window.display();
    }

    return 0;
}