import pytest
from pytest_cases.tests.example_code import super_function_i_want_to_test

from pytest_cases import cases_data, CaseDataGetter, unfold_expected_err, get_all_cases, get_pytest_parametrize_args
from pytest_cases.tests.simple import test_main_cases


# Decorator way:
@cases_data(module=test_main_cases)
def test_with_cases_decorated(case_data  # type: CaseDataGetter
                              ):
    """ Example unit test that is automatically parametrized with @cases_data """

    # 1- Grab the test case data
    i, expected_o, expected_e = case_data.get()

    # 2- Use it
    if expected_e is None:
        # **** Nominal test ****
        outs = super_function_i_want_to_test(**i)
        assert outs == expected_o

    else:
        # **** Error test ****
        # First see what we need to assert
        err_type, err_inst, err_checker = unfold_expected_err(expected_e)

        # Run with exception capture and type check
        with pytest.raises(err_type) as err_info:
            super_function_i_want_to_test(**i)

        # Optional - Additional Exception instance check
        if err_inst is not None:
            assert err_info.value == err_inst

        # Optional - Additional exception instance check
        if err_checker is not None:
            err_checker(err_info.value)


# ----------------- Advanced: Manual way: -------------
cases = get_all_cases(module=test_main_cases)
# apply the pytest marks
marked_cases, cases_ids = get_pytest_parametrize_args(cases)


@pytest.mark.parametrize('case_data', marked_cases, ids=cases_ids)
def test_with_cases_manual(case_data  # type: CaseDataGetter
                           ):
    """ Example unit test that is automatically parametrized with @cases_data """

    # 1- Grab the test case data
    i, expected_o, expected_e = case_data.get()

    # 2- Use it
    if expected_e is None:
        # **** Nominal test ****
        outs = super_function_i_want_to_test(**i)
        assert outs == expected_o

    else:
        # **** Error test ****
        # First see what we need to assert
        err_type, err_inst, err_checker = unfold_expected_err(expected_e)

        # Run with exception capture and type check
        with pytest.raises(err_type) as err_info:
            super_function_i_want_to_test(**i)

        # Optional - Additional Exception instance check
        if err_inst is not None:
            assert err_info.value == err_inst

        # Optional - Additional exception instance check
        if err_checker is not None:
            err_checker(err_info.value)
