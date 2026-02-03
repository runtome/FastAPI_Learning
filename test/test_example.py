import pytest

def test_equal_or_not_equal():
    assert 1 + 1 == 2
    assert 2 * 2 != 5
    
def test_is_instance():
    assert isinstance("hello", str)
    assert not isinstance(123, str)
    
def test_boolean_conditions():
    assert True
    assert not False
    assert ('hello' == 'world') is False
    
def test_type_checks():
    assert type(3.14) is float
    assert type([1, 2, 3]) is list
    
def test_greater_less():
    assert 5 > 3
    assert 2 < 4
    assert 10 >= 10
    assert 1 <= 2
    
    

class Student:
  def __init__(self, name:str , last_name:str, major:str, years:int):
      self.name = name
      self.last_name = last_name
      self.major = major
      self.years = years
      
@pytest.fixture
def defult_student():
    return Student("Alice", "Smith", "Mathematics", 2)
      
def test_student_instance(defult_student):

    assert isinstance(defult_student, Student)
    assert defult_student.name == "Alice" , "First name does not match"
    assert defult_student.last_name == "Smith" , "Last name does not match"
    assert defult_student.major == "Mathematics" , "Major does not match"
    assert defult_student.years == 2
    
    
