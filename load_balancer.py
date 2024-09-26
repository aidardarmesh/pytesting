"""
System requirements:
* max 10 instances
* round-robin
* random
"""


import random, unittest
from enum import Enum


class Strategy(Enum):
    RANDOM = "random"
    ROUND_ROBIN = "round_robin"


class LoadBalancer:
    MAX_INSTANCES = 10

    def __init__(self, instances, strategy=Strategy.ROUND_ROBIN):
        if len(instances) > self.MAX_INSTANCES:
            raise ValueError("Too many instances")
        self.instances = instances
        self.strategy = strategy
        self.current_idx = 0

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_random(self):
        return random.choice(self.instances)

    def get_round_robin(self):
        instance = self.instances[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.instances)
        return instance

    def get_instance(self):
        if self.strategy == Strategy.RANDOM:
            return self.get_random()
        elif self.strategy == Strategy.ROUND_ROBIN:
            return self.get_round_robin()

    def add_instance(self, instance):
        if len(self.instances) >= self.MAX_INSTANCES:
            raise ValueError("Too many instances")
        self.instances.append(instance)

    def remove_instance(self, instance):
        if not instance in self.instances:
            raise ValueError(f"Instance {instance} doesn't exist")
        self.instances.remove(instance)
        self.current_idx = self.current_idx % len(self.instances) if self.instances else 0


class TestLoadBalancer(unittest.TestCase):
    def setUp(self):
        self.instances = ["instance1", "instance2", "instance3", "instance4"]
        self.lb = LoadBalancer(self.instances)

    def test_max_instances(self):
        too_many = ["instance" + str(i) for i in range(12)]
        with self.assertRaises(ValueError):
            self.lb = LoadBalancer(too_many)

    def test_random_strategy(self):
        self.lb.set_strategy(Strategy.RANDOM)
        self.assertIn(self.lb.get_instance(), self.lb.instances)
        self.assertIn(self.lb.get_instance(), self.lb.instances)
        self.assertIn(self.lb.get_instance(), self.lb.instances)

    def test_round_robin(self):
        self.assertEqual(self.lb.get_instance(), "instance1")
        self.assertEqual(self.lb.get_instance(), "instance2")
        self.assertEqual(self.lb.get_instance(), "instance3")

    def test_add_instance(self):
        current_instances_len = len(self.instances)
        self.lb.add_instance("instance5")
        self.assertIn("instance5", self.instances)
        self.assertEqual(current_instances_len + 1, len(self.instances))

    def test_remove_instance(self):
        current_instances_len = len(self.instances)
        self.lb.remove_instance("instance2")
        self.assertNotIn("instance2", self.instances)
        self.assertEqual(current_instances_len - 1, len(self.instances))

    def test_remove_invalid_instance(self):
        with self.assertRaises(ValueError) as exc_info:
            self.lb.remove_instance("instance6")
        self.assertTrue("Instance instance6 doesn't exist" in str(exc_info.exception))

    def test_add_instance_limit(self):
        with self.assertRaises(ValueError) as exc_info:
            [self.lb.add_instance("instance" + str(i)) for i in range(self.lb.MAX_INSTANCES)]
        self.assertTrue("Too many" in str(exc_info.exception))
