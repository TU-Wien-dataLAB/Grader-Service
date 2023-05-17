from grader_service.git.evaluator import lookup
import pudb

def expect_positive():
    "A dict of query / response pairs"
    test_data = {}
    test_data.update({
        # (repo rtype *args)
        # len(*args) == 3
        "(repo lxuser l102 a1 johnny)": "/home/johnny/l102/a1",
        "(repo lxsource jaas20 1 amccartn)": "/home/amccartn/source/jaas20/1",
        "(repo lxrelease jaas20 1 amccartn)": "/home/amccartn/release/jaas20/1",
        # len(*args) == 3
        "(repo gsuser jaas20 1 amccartn)": "/var/lib/grader-service/git/jaas20/1/user/amccartn",
        # len(*args) == 2
        "(repo gssource jaas20 1)": "/var/lib/grader-service/git/jaas20/1/source",
        "(repo gsrelease jaas20 1)": "/var/lib/grader-service/git/jaas20/1/release",
        # 
        "(repo autograde jaas20 1 ewimmer)": "/var/lib/grader-service/git/jaas20/1/autograde/user/ewimmer",
        "(repo feedback jaas20 1 ewimmer)": "/var/lib/grader-service/git/jaas20/1/feedback/user/ewimmer",
        "(repo edit jaas20 1 6)":"/var/lib/grader-service/git/jaas20/1/edit/6",
        #"(prep init (repo gssource jaas20 1))": "git init --bare /var/lib/grader-service/git/jaas20/1/source",
    })
    return test_data


def test_path_constructors_successful():
    test_data = expect_positive()
    for k in test_data.keys():
        assert lookup(k) == test_data[k]
