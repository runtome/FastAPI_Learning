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
      
def test_student_instance():
    student = Student("John", "Doe", "Computer Science", 3)
    assert isinstance(student, Student)
    assert student.name == "John" , "First name does not match"
    assert student.last_name == "Doe" , "Last name does not match"
    assert student.major == "Computer Science" , "Major does not match"
    assert student.years == 3
    
    
