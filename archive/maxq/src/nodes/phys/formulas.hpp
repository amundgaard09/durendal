
#ifndef FORMULAS.HPP
#define FORMULAS.HPP

float toDegrees(float radians);
float Torque(float moment_arm_distance, float force);
float GearRatio(int driving_gear_tc, int driven_gear_tc);
float AngularVelocityR(float rpm);
float AngularVelocityD(float rpm);
float KineticEnergy(float mass, float velocity);
float PotentialEnergy(float mass, float height, float gravity);
float EinsteinMassEnergyEquivalence(float mass);

#endif