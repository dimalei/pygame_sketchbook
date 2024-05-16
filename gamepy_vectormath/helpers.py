import math

# thank you chat-gpt for this one!

def angle_between_vectors(v1, v2):
        """returns the angle in between v1 and v2 from 180° to -180°"""
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
        magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

        if cos_theta > 1:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1

        angle_radians = math.acos(cos_theta)
        angle_degrees = math.degrees(angle_radians)

        # Determine the sign of the angle using the cross product
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        if cross_product < 0:
            angle_degrees = -angle_degrees

        return angle_degrees