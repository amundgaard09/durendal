
#include <cmath>
#include "formulas.hpp"

#define _PI 3.14159265359
#define _C 299792458 

float toDegrees(float radians) { return (radians / _PI * 180); }

float Torque(float moment_arm_distance, float force) { return (moment_arm_distance * force); }

float GearRatio(int driving_gear_tc, int driven_gear_tc) { return (driven_gear_tc / driving_gear_tc); }

float AngularVelocityR(float rpm) { return (rpm * _PI / 30); }
float AngularVelocityD(float rpm) { return toDegrees(AngularVelocityR(rpm)); }

float KineticEnergy(float mass, float velocity) { return (0.5 * mass * velocity * velocity); }
float PotentialEnergy(float mass, float height, float gravity) { return (mass * gravity * height); }

float EinsteinMassEnergyEquivalence(float mass) { return (mass * _C * _C); }