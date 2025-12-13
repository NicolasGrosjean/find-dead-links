from find_dead_links.placeholder import add_2
from tests.conftest import generate_random_int


def test_add_2():
    input_a = generate_random_int()
    assert add_2(input_a) == input_a + 2
