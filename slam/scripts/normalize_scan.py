#!/usr/bin/env python3

import math
import rclpy

from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan

BEAMS = 224
TWO_PI = 2.0 * math.pi
STEP = TWO_PI / BEAMS


class ScanNormalizer(Node):

    def __init__(self):
        super().__init__('tb3_scan_normalizer')

        self.publisher = self.create_publisher(
            LaserScan,
            '/scan_normalized',
            qos_profile_sensor_data
        )

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.process_scan,
            qos_profile_sensor_data
        )

        self.count = 0

        self.get_logger().info(
            'Scan normalizer started: /scan -> /scan_normalized'
        )

    def process_scan(self, scan):

        if not scan.ranges or scan.angle_increment <= 0.0:
            return

        output = LaserScan()

        output.header = scan.header

        output.angle_min = 0.0
        output.angle_increment = STEP
        output.angle_max = (BEAMS - 1) * STEP

        # Original beam timing does not directly map
        # to the resampled angular bins.
        output.time_increment = 0.0
        output.scan_time = scan.scan_time

        output.range_min = scan.range_min
        output.range_max = scan.range_max

        ranges = [float('inf')] * BEAMS
        errors = [float('inf')] * BEAMS

        has_intensity = (
            len(scan.intensities) == len(scan.ranges)
        )

        intensities = [0.0] * BEAMS if has_intensity else []

        for i, distance in enumerate(scan.ranges):

            if not math.isfinite(distance):
                continue

            if distance <= max(scan.range_min, 0.0):
                continue

            if distance > scan.range_max:
                continue

            angle = (
                scan.angle_min + i * scan.angle_increment
            ) % TWO_PI

            index = int(
                math.floor(angle / STEP + 0.5)
            ) % BEAMS

            target_angle = index * STEP

            error = abs(
                (angle - target_angle + math.pi)
                % TWO_PI - math.pi
            )

            if error < errors[index]:

                ranges[index] = distance
                errors[index] = error

                if has_intensity:
                    intensities[index] = scan.intensities[i]

        output.ranges = ranges
        output.intensities = intensities

        self.publisher.publish(output)

        self.count += 1

        if self.count <= 10 or self.count % 100 == 0:

            valid = sum(
                math.isfinite(value)
                for value in ranges
            )

            self.get_logger().info(
                f'Scan {self.count}: '
                f'input={len(scan.ranges)}, '
                f'output={len(output.ranges)}, '
                f'valid={valid}'
            )


def main():

    rclpy.init()

    node = ScanNormalizer()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
