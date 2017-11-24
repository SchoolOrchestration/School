import unittest, mock
from github_release import get_repository, bump_version
from github3.null import NullObject

# python -m unittest test_github_release

class MockGithub:
    def __init__(self, tag_name=None):
        self.tag_name = tag_name

    def repository(self, user, repo):
        return (user, repo)

class GetRepositoryTestCase(unittest.TestCase):

    def setUp(self):
        self.github = MockGithub()

    def test_can_get_a_specific_repo(self):
        user, repo = get_repository(self.github, None, 'foo/bar')
        assert user == 'foo'
        assert repo == 'bar'

    def test_specific_repo_gets_precedence_over_user_repo(self):
        user, repo = get_repository(self.github, 'joe', 'foo/bar')
        assert user == 'foo'
        assert repo == 'bar'

    def test_can_get_a_repo_with_user_and_repo_name(self):
        user, repo = get_repository(self.github, 'joe', 'bar')
        assert user == 'joe'
        assert repo == 'bar'

class BumpVersionTestCase(unittest.TestCase):

    def setUp(self):
        self.test_inputs = [
            # input, expected output
            (NullObject(), '1.0.0', '0.1.0', '0.0.1'),
            (MockGithub(tag_name='1.0.0'), '2.0.0', '1.1.0', '1.0.1'),
            (MockGithub(tag_name='1.1.1'), '2.0.0', '1.2.0', '1.1.2'),
        ]

    def test_bump_major(self):

        for input_value, major, minor, patch in self.test_inputs:
            # latest_release = MockGithub(tag_name=input_value)
            major_result = bump_version(input_value, 'major')
            assert major_result == major, \
                'Expected major bump of {} to be {}. Got: {}' .format(input_value, major, major_result)

    def test_bump_minor(self):

        for input_value, major, minor, patch in self.test_inputs:
            # latest_release = MockGithub(tag_name=input_value)
            minor_result = bump_version(input_value, 'minor')
            assert minor_result == minor, \
                'Expected minor bump of {} to be {}. Got: {}' .format(input_value, minor, minor_result)


    def test_bump_patch(self):

        for input_value, major, minor, patch in self.test_inputs:
            # latest_release = MockGithub(tag_name=input_value)
            patch_result = bump_version(input_value, 'patch')
            assert patch_result == patch, \
                'Expected patch bump of {} to be {}. Got: {}' .format(input_value, patch, patch_result)
