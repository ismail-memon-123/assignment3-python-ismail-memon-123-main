from cs5278_assignment_3.geo_db_factory import GeoDBFactory
from cs5278_assignment_3.geo_hash import GeoHash

class TestGeoDB:
    # Create a good set of tests for your GeoDB.

    @staticmethod
    def test_example():
        # Fix Me!
        assert True

    @staticmethod
    def test_insert_and_delete_all():
        bits_of_precision = 16
        db = GeoDBFactory.new_database(bits_of_precision)

        db.insert(9, 9)
        db.insert(0, 0)
        db.insert(18, 18)
        db.insert(-9, -9)

        assert db.contains(9, 9, bits_of_precision)
        assert db.contains(0, 0, bits_of_precision)
        assert db.contains(18, 18, bits_of_precision)
        assert db.contains(-9, -9, bits_of_precision)

        # 0 bits of p means delete all
        assert len(db.delete_all(0, 0, 0)) == 4
        assert not db.contains(9, 9, bits_of_precision)
        assert not db.contains(0, 0, bits_of_precision)
        assert not db.contains(18, 18, bits_of_precision)
        assert not db.contains(-9, -9, bits_of_precision)
    
    @staticmethod
    def test_nearby_with_zero_bop():
        bits_of_precision = 10
        db = GeoDBFactory.new_database(bits_of_precision)

        db.insert(80, 80)
        db.insert(70, 70)
        db.insert(30, 30)
        db.insert(10, 10)
        db.insert(5, 5)

        answer = db.nearby(16, 16, 0)
        assert len(answer) == 5

        sum = 0.0

        for i in range(len(answer)):
            curr_pair = answer[i]
            # will add all the coordinates and compare sum to make sure its correct
            sum += curr_pair[0] + curr_pair[1]

        # 2*80 + 2*70 + 2*30 + 2*10 + 2*5 = 390
        assert ( 385 < sum and sum < 395 )
    
    @staticmethod
    def test_contains_with_combos():
        bits_of_precision = 20
        db = GeoDBFactory.new_database(bits_of_precision)

        db.insert(-90, -80)
        db.insert(90, 80)
        db.insert(0, 0)

        assert db.contains(-90, -80, bits_of_precision)
        assert db.contains(90, 80, bits_of_precision)
        assert db.contains(0, 0, bits_of_precision)

        assert db.delete(0, 0)
        assert not db.contains(0, 0, bits_of_precision)
        assert db.contains(90, 80, bits_of_precision)
        assert db.contains(-90, -80, bits_of_precision)

        assert db.delete(90, 80)
        assert not db.contains(90, 80, bits_of_precision)
        assert db.contains(-90, -80, bits_of_precision)
        
        assert db.delete(-90, -80)
        assert not db.contains(-90, -80, bits_of_precision)
    
    @staticmethod
    def test_nearby():
        bits_of_precision = 10
        db = GeoDBFactory.new_database(bits_of_precision)

        db.insert(80, 80)
        db.insert(75, 75)
        db.insert(72, 72)
        db.insert(66, 66)
        db.insert(0, 0)

        print(GeoHash.geo_hash(80, 80, bits_of_precision))
        # cant do 79 bec it just maps to the same and then we have issues.
        print(GeoHash.geo_hash(75, 75, bits_of_precision))
        print(GeoHash.geo_hash(72, 72, bits_of_precision))
        print(GeoHash.geo_hash(66, 66, bits_of_precision))
        # The above 3 are unique enough but still close by
        print(GeoHash.geo_hash(0, 0, bits_of_precision))

        answer_1 = db.nearby(80, 80, bits_of_precision)
        assert len(answer_1) == 1

        answer_2 = db.nearby(80, 80, 0)
        assert len(answer_2) == 5

        answer_3 = db.nearby(80, 80, 2)
        assert len(answer_3) == 5

        answer_4 = db.nearby(80, 80, 3)
        assert len(answer_4) == 4

        answer = db.nearby(80, 80, 5)
        assert len(answer) == 3

        sum = 0.0
        for i in range(len(answer)):
            curr_pair = answer[i]
            sum += curr_pair[0] + curr_pair[1]

        # 2*80 + 2*75 + 2*72 = 454
        assert (abs(sum-454) < 0.1)

        # Now test nearby with one specific it should only return 1 pair
        assert (abs(answer_1[0][0] - 80) < 0.1)
    
    @staticmethod
    def test_delete_all_with_more_precision():
        bits_of_precision = 20
        db = GeoDBFactory.new_database(bits_of_precision)
    
        db.insert(80, 80)
        db.insert(79, 79)
        db.insert(72, 72)

        print(GeoHash.geo_hash(80, 80, bits_of_precision))
        print(GeoHash.geo_hash(79, 79, bits_of_precision))
        print(GeoHash.geo_hash(72, 72, bits_of_precision))

        # 72, 72 wont make cut here
        answer_1 = db.nearby(80, 80, 7)
        assert len(answer_1) == 2

        # Only 80, 80 will remain
        answer_2 = db.nearby(80, 80, 15)
        assert len(answer_2) == 1

    @staticmethod
    def test_with_zero_bop():
        bits_of_precision = 0
        db = GeoDBFactory.new_database(bits_of_precision)

        db.insert(0, 0)
        # Wont return properly and that is expected.
        assert not db.delete(0, 0)

    @staticmethod
    def test_delete_with_non_existent_value():
        bits_of_precision = 10
        db = GeoDBFactory.new_database(bits_of_precision)

        assert not db.delete(79, 79)

    @staticmethod
    def test_overlaps():
        bits_of_precision = 10
        db = GeoDBFactory.new_database(bits_of_precision)
    
        db.insert(80, 80)
        db.insert(79, 79)
        db.insert(72, 72)
        
        print(GeoHash.geo_hash(80, 80, bits_of_precision))
        print(GeoHash.geo_hash(79, 79, bits_of_precision))
        print(GeoHash.geo_hash(72, 72, bits_of_precision))

        # 80 and 79 will overlap so there will only be 2 things in trie.
        answer = db.nearby(80, 80, 0)
        assert len(answer) == 2

        # and that value will be 79 since that came last. So 79 + 72 = 151
        assert abs((answer[0][0] + answer[1][0]) - 151) < 0.1

    @staticmethod
    def test_cleaning_does_not_leave_hanging_branches():
        bits_of_precision = 10
        db = GeoDBFactory.new_database(bits_of_precision)

        db.insert(10, 10)
        db.insert(11, 11)
        db.insert(-20, -12)
        
        print(GeoHash.geo_hash(10, 10, bits_of_precision))
        print(GeoHash.geo_hash(11, 11, bits_of_precision))
        print(GeoHash.geo_hash(-20, -12, bits_of_precision))

        # delete (-20, -12) only
        assert db.delete(-20, -12)

        # make sure nothing in the false side of root remains (-20, -12) with 1 bit is just False.
        assert len(db.nearby(-20, -12, 1)) == 0
