import json
import pytest
import subprocess
import re
from Script import (
    input_processing_name,
    input_processing_dis,
    price_comparison)


class TestInputProcessingName:
    @pytest.mark.parametrize("input",
                    ["warszawa", "Warszawa", "WARSZAWa"])
    def test_input_processing_name_success(self, input):
        assert input_processing_name(input) == "Warszawa"

    def test_input_processing_name_fail(self):
        with pytest.raises(AttributeError):
            assert input_processing_name(None)


class TestPriceComparison:
    @pytest.mark.parametrize("input",
                             [(10, None, None), (15, None, 15),
                              (20, 19, None),(20, 18 ,22),
                              (20, 20, 20)])
    def test_price_comparison_success(self, input):
        assert price_comparison(*input)

    def test_price_comparison_fail(self):
        with pytest.raises(TypeError):
            price_comparison(None, 10, 20)

    def test_price_comparison_fail_2(self):
        assert not price_comparison(18, 13, 16)


class TestInputProcessingDis:
    def test_with_dis(self):
        assert input_processing_dis("wola") == "wola"

    @pytest.mark.parametrize("input",
                        ["none", "None", "NONE", "noNe"])
    def test_without_dis(self, input):
        assert input_processing_dis(input) is None


class TestMainFunction:
    low_price = 1000
    high_price = 4000
    result = subprocess.check_output(f"Script.py warszawa {low_price} {high_price} none 3",
                                     shell=True, text=True)
    lines = result.split('\n')
    length = len(lines)

    def test_urls(self):
        regex = re.compile(
            r'(https://www.otodom.pl|'
            r'https://www.olx.pl)'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        for line in self.lines[:-3]:
            assert re.match(regex, line)

    def test_found_results1(self):
        regex = re.compile(
            r'Found '
            r'[0-9]+ '
            r'results$')
        assert re.match(regex, self.lines[-3])

    def test_found_results2(self):
        found_slices = self.lines[-3].split(' ')
        found_counter = int(found_slices[1].strip())
        assert found_counter == self.length - 3

    def test_runtime(self):
        regex = re.compile(
            r'Runtime: '
            r'\d+\.\d+'
            r's$')
        assert re.match(regex, self.lines[-2])

    def test_price(self):
        with open('scriptFlats.json', 'r') as json_file:
            data = json.load(json_file)
            for value in data:
                assert self.low_price <= data[value] <= self.high_price