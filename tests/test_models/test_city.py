import unittest
from models import storage
from models.city import City
from models.state import State


class TestCity(unittest.TestCase):

    def setUp(self):
        """Create a sample state"""
        self.state = State(name="California")
        self.state.save()

    def tearDown(self):
        """Clean up by deleting the state"""
        self.state.delete()

    def test_initialization(self):
        """Test initialization of City instance"""
        city = City(name="Los Angeles", state_id=self.state.id)
        self.assertIsInstance(city, City)
        self.assertEqual(city.name, "Los Angeles")
        self.assertEqual(city.state_id, self.state.id)

    def test_properties(self):
        """Test properties of City instance"""
        city = City(name="San Francisco", state_id=self.state.id)
        self.assertEqual(city.name, "San Francisco")
        self.assertEqual(city.state_id, self.state.id)

    def test_save_method(self):
        """Test save method updates updated_at attribut"""
        city = City(name="Santa Monica", state_id=self.state.id)
        original_updated_at = city.updated_at

        city.save()
        self.assertNotEqual(original_updated_at, city.updated_at)

    def test_to_dict_method(self):
        """Test to_dict method returns dictionary representation"""
        city = City(name="Palo Alto", state_id=self.state.id)
        city_dict = city.to_dict()

        self.assertIsInstance(city_dict, dict)
        self.assertEqual(city_dict['name'], "Palo Alto")
        self.assertEqual(city_dict['state_id'], self.state.id)

    def test_delete_method(self):
        """Test delete method removes instance from storage"""
        city = City(name="Mountain View", state_id=self.state.id)
        city.save()
        city_id = city.id

        city.delete()
        self.assertNotIn(f"City.{city_id}", storage.all())

    def test_string_representation(self):
        """Test string representation of City instance"""
        city = City(name="Beverly Hills", state_id=self.state.id)
        city_str = str(city)

        self.assertIn("Beverly Hills", city_str)
        self.assertIn(self.state.id, city_str)

    def test_serialization_deserialization(self):
        """Test serialization and deserialization of City instance"""
        city = City(name="Malibu", state_id=self.state.id)
        city_json = city.to_dict()

        new_city = City(**city_json)
        self.assertEqual(city.id, new_city.id)
        self.assertEqual(city.name, new_city.name)
        self.assertEqual(city.state_id, new_city.state_id)


if __name__ == "__main__":
    unittest.main()
